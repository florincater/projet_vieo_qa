# backend/rag/transcription.py
import whisper
import numpy as np
from typing import List, Dict, Optional
import time
import warnings

class VideoTranscriber:
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self.model = None
        try:
            self.load_model()
        except Exception as e:
            warnings.warn(f"Impossible de charger Whisper: {e}")
            print("Utilisation d'un mode de démonstration")
    
    def load_model(self):
        """Charge le modèle Whisper"""
        try:
            print(f"Chargement du modèle Whisper '{self.model_size}'...")
            self.model = whisper.load_model(self.model_size)
            print("Modèle chargé avec succès!")
        except Exception as e:
            print(f"Erreur chargement Whisper: {e}")
            self.model = None
    
    def transcribe(self, audio_path: str, language: Optional[str] = None) -> Dict:
        """Transcrit le fichier audio"""
        if self.model is None:
            # Mode démo si Whisper n'est pas disponible
            return {
                'text': "Mode démo: Whisper n'est pas disponible. Veuillez installer openai-whisper.",
                'segments': [
                    {'text': "Ceci est une transcription de démonstration.", 'start': 0, 'end': 5},
                    {'text': "Installez openai-whisper pour la transcription réelle.", 'start': 5, 'end': 10}
                ]
            }
        
        # Code normal de transcription ici...
        start_time = time.time()
        options = {'task': 'transcribe', 'verbose': True, 'fp16': False}
        if language:
            options['language'] = language
        
        result = self.model.transcribe(audio_path, **options)
        print(f"Transcription terminée en {time.time() - start_time:.2f}s")
        return result