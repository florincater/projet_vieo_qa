# ingestion.py
import cv2
from moviepy import VideoFileClip, AudioFileClip  # Changed this line!
import os
from pathlib import Path

class VideoIngestion:
    def __init__(self, upload_folder="data/videos", max_size_mb=500):
        self.upload_folder = Path(upload_folder)
        self.upload_folder.mkdir(parents=True, exist_ok=True)
        self.max_size_mb = max_size_mb
        self.supported_formats = ['.mp4', '.mkv', '.mov', '.webm']
    
    def validate_video(self, file_path):
        """Valide le format et la taille de la vidéo"""
        file_path = Path(file_path)
        # Vérification du format
        if file_path.suffix.lower() not in self.supported_formats:
            return False, "Format non supporté"
        # Vérification de la taille
        size_mb = file_path.stat().st_size / (1024 * 1024)
        if size_mb > self.max_size_mb:
            return False, f"Taille trop grande ({size_mb:.1f}MB > {self.max_size_mb}MB)"
        return True, "OK"
    
    def extract_metadata(self, video_path):
        """Extrait les métadonnées techniques"""
        cap = cv2.VideoCapture(str(video_path))
        metadata = {
            'duration': cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS),
            'fps': cap.get(cv2.CAP_PROP_FPS),
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'total_frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'has_audio': self._check_audio(video_path)
        }
        cap.release()
        return metadata
    
    def extract_audio(self, video_path, output_path=None):
        """Extrait l'audio de la vidéo"""
        if output_path is None:
            output_path = self.upload_folder / f"{video_path.stem}_audio.wav"
        
        # Updated for MoviePy 2.x
        video = VideoFileClip(str(video_path))  # No more .editor!
        audio = video.audio
        if audio:
            audio.write_audiofile(str(output_path))
        video.close()
        return output_path
    
    def _check_audio(self, video_path):
        """Check if video has audio track"""
        try:
            video = VideoFileClip(str(video_path))  # Updated here too
            has_audio = video.audio is not None
            video.close()
            return has_audio
        except:
            return False

# Test block
if __name__ == "__main__":
    print("VideoIngestion module loaded successfully!")
    ingestor = VideoIngestion()
    print(f"Upload folder: {ingestor.upload_folder}")
    print(f"Supported formats: {ingestor.supported_formats}")
    print(f"Max size: {ingestor.max_size_mb}MB")