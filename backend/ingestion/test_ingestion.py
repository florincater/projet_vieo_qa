# test_ingestion.py
from ingestion import VideoIngestion
from pathlib import Path

# Initialize the ingestor
ingestor = VideoIngestion()

# Test with a video file (adjust path to your test video)
test_video = Path("C:/Users/flori/Downloads/sample-10s (1).mp4")

if test_video.exists():
    # Validate
    is_valid, message = ingestor.validate_video(test_video)
    print(f"Validation: {message}")
    
    if is_valid:
        # Extract metadata
        metadata = ingestor.extract_metadata(test_video)
        print(f"Metadata: {metadata}")
        
        # Extract audio
        audio_path = ingestor.extract_audio(test_video)
        print(f"Audio extracted to: {audio_path}")
else:
    print(f"Test video not found at {test_video}")
    print("Create a 'data/videos' folder and add a test video")