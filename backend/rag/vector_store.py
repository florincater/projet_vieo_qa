# vector_store.py
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np

# Petit correctif pour éviter les warnings
import warnings
warnings.filterwarnings('ignore')

class VideoVectorStore:
    def __init__(self, collection_name="video_chunks"):
        # Utiliser PersistentClient avec un chemin absolu
        import os
        db_path = os.path.join(os.path.dirname(__file__), "chroma_db")
        self.client = chromadb.PersistentClient(path=db_path)
        
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Modèle d'embedding avec gestion d'erreur
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-V2')
        except Exception as e:
            print(f"Erreur chargement modèle: {e}")
            # Fallback vers un modèle plus petit si besoin
            self.embedding_model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
    
    def add_chunks(self, video_id, chunks):
        """Ajoute des chunks à la base vectorielle"""
        ids = []
        embeddings = []
        metadatas = []
        documents = []
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"{video_id}_{i}"
            ids.append(chunk_id)
            
            # Générer l'embedding
            embedding = self.embedding_model.encode(chunk['text']).tolist()
            embeddings.append(embedding)
            
            # Métadonnées temporelles
            metadatas.append({
                'video_id': video_id,
                'start_time': chunk['start'],
                'end_time': chunk['end'],
                'type': 'audio'
            })
            
            documents.append(chunk['text'])
        
        # Ajout à ChromaDB par lots de 100 pour éviter les problèmes
        batch_size = 100
        for i in range(0, len(ids), batch_size):
            batch_ids = ids[i:i+batch_size]
            batch_embeddings = embeddings[i:i+batch_size]
            batch_metadatas = metadatas[i:i+batch_size]
            batch_documents = documents[i:i+batch_size]
            
            self.collection.add(
                ids=batch_ids,
                embeddings=batch_embeddings,
                metadatas=batch_metadatas,
                documents=batch_documents
            )
        
        return len(chunks)
    
    def search(self, query, top_k=5):
        #Recherche les chunks pertinents pour une question"""
        # Embedding de la question
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Recherche
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Formatage des résultats
        passages = []
        if results['ids'] and results['ids'][0]:
            for i in range(len(results['ids'][0])):
                passage = {
                    'text': results['documents'][0][i],
                    'start': results['metadatas'][0][i]['start_time'],
                    'end': results['metadatas'][0][i]['end_time'],
                    'score': results['distances'][0][i] if 'distances' in results else None
                }
                passages.append(passage)
        
        return passages

# Test
if __name__ == "__main__":
    print("Testing VideoVectorStore...")
    store = VideoVectorStore()
    print("✓ Vector store initialized")
    
    # Test avec des données factices
    test_chunks = [
        {'text': 'Test de transcription vidéo', 'start': 0.0, 'end': 5.0}
    ]
    store.add_chunks("test", test_chunks)
    print("✓ Test chunks added")
    
    results = store.search("test")
    print(f"✓ Search returned {len(results)} results")