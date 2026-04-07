# backend/transcription.py
from faster_whisper import WhisperModel
import json

class VideoTranscriber:
    def __init__(self, model_size="base", device="cpu", compute_type="float32"):
        """
        Modèles disponibles: tiny, base, small, medium, large-v2
        Sur CPU, "base" ou "small" sont recommandés
        compute_type: "float32", "float16", "int8"
        """
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
    
    def transcribe(self, audio_path):
        """Transcrit l'audio avec timestamps"""
        segments, info = self.model.transcribe(
            audio_path, 
            beam_size=5,
            word_timestamps=True
        )
        
        transcription = []
        for segment in segments:
            transcription.append({
                'text': segment.text,
                'start': segment.start,
                'end': segment.end,
                'words': [
                    {'word': word.word, 'start': word.start, 'end': word.end}
                    for word in segment.words
                ] if segment.words else []
            })
        
        return {
            'language': info.language,
            'language_probability': info.language_probability,
            'segments': transcription
        }
    
    def chunk_transcription(self, transcription, strategy="sentence"):
        """Découpe la transcription en chunks sémantiques"""
        chunks = []
        
        if strategy == "sentence":
            for i, segment in enumerate(transcription['segments']):
                chunks.append({
                    'chunk_id': i,
                    'text': segment['text'],
                    'start': segment['start'],
                    'end': segment['end'],
                    'words': segment.get('words', [])
                })
        
        elif strategy == "temporal":
            window_size = 30
            current_chunk = {'text': '', 'start': 0, 'end': 0, 'segments': []}
            
            for segment in transcription['segments']:
                if not current_chunk['text']:
                    current_chunk['start'] = segment['start']
                
                if segment['end'] - current_chunk['start'] <= window_size:
                    current_chunk['text'] += ' ' + segment['text']
                    current_chunk['end'] = segment['end']
                    current_chunk['segments'].append(segment)
                else:
                    if current_chunk['text']:
                        chunks.append(current_chunk)
                    current_chunk = {
                        'text': segment['text'],
                        'start': segment['start'],
                        'end': segment['end'],
                        'segments': [segment]
                    }
            
            if current_chunk['text']:
                chunks.append(current_chunk)
        
        return chunks

# For direct testing
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        transcriber = VideoTranscriber(model_size="tiny", device="cpu")
        result = transcriber.transcribe(sys.argv[1])
        print(json.dumps(result, indent=2, ensure_ascii=False))