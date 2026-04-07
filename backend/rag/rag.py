# backend/rag/rag.py
# backend/rag/rag.py
from typing import Dict, List, Any
import numpy as np
from .vector_store import VideoVectorStore  # Ajouter le point pour import relatif

class VideoRAG:
    """Système RAG pour répondre aux questions sur les vidéos"""
    
    def __init__(self, vector_store: VideoVectorStore):
        self.vector_store = vector_store
        self.conversation_history = []  # Pour le contexte conversationnel
    
    def answer(self, question: str, top_k: int = 3, use_conversation: bool = False) -> Dict:
        """
        Répond à une question basée sur le contenu de la vidéo
        
        Args:
            question: Question de l'utilisateur
            top_k: Nombre de sources à récupérer
            use_conversation: Inclure l'historique de conversation
        
        Returns:
            Dictionnaire avec réponse et sources
        """
        # Améliorer la question avec le contexte conversationnel
        enhanced_question = question
        if use_conversation and self.conversation_history:
            context = "\n".join(self.conversation_history[-3:])  # Derniers 3 échanges
            enhanced_question = f"Contexte: {context}\nQuestion: {question}"
        
        # Rechercher les passages pertinents
        sources = self.vector_store.search(enhanced_question, top_k=top_k)
        
        if not sources:
            return {
                'answer': "Désolé, je n'ai pas trouvé d'information pertinente dans la vidéo pour répondre à cette question.",
                'sources': [],
                'confidence': 0
            }
        
        # Construire le contexte à partir des sources
        context = self._build_context(sources)
        
        # Générer la réponse (version simplifiée sans LLM)
        answer = self._generate_answer(question, context, sources)
        
        # Sauvegarder dans l'historique
        self.conversation_history.append(f"Q: {question}")
        self.conversation_history.append(f"A: {answer[:100]}...")
        
        return {
            'answer': answer,
            'sources': sources,
            'confidence': self._calculate_confidence(sources)
        }
    
    def _build_context(self, sources: List[Dict]) -> str:
        """Construit le contexte à partir des sources"""
        context_parts = []
        for i, source in enumerate(sources, 1):
            timestamp = f"[{source['start']:.1f}s - {source['end']:.1f}s]"
            context_parts.append(f"{timestamp} {source['text']}")
        
        return "\n".join(context_parts)
    
    def _generate_answer(self, question: str, context: str, sources: List[Dict]) -> str:
        """
        Génère une réponse basée sur le contexte.
        Version simplifiée - vous pouvez intégrer un LLM ici.
        """
        if not sources:
            return "Aucune information trouvée."
        
        # Extraire le passage le plus pertinent
        best_source = sources[0]
        confidence = best_source.get('score', 0)
        
        # Réponse basée sur la similarité
        if confidence < 0.5:
            return f"Je ne suis pas très sûr, mais voici ce que j'ai trouvé: {best_source['text']}"
        else:
            return f"D'après la vidéo: {best_source['text']}"
    
    def _calculate_confidence(self, sources: List[Dict]) -> float:
        """Calcule un score de confiance pour la réponse"""
        if not sources:
            return 0.0
        
        # Moyenne des scores de similarité
        scores = [s.get('score', 0) for s in sources if s.get('score') is not None]
        if scores:
            return float(np.mean(scores))
        
        # Si pas de scores, confiance basée sur le nombre de sources
        return min(1.0, len(sources) / 5.0)
    
    def clear_history(self):
        """Efface l'historique de conversation"""
        self.conversation_history = []
    
    def get_stats(self) -> Dict:
        """Retourne des statistiques sur le système RAG"""
        return {
            'conversation_length': len(self.conversation_history),
            'total_queries': len([h for h in self.conversation_history if h.startswith('Q:')])
        }