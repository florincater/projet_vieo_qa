# test_basic.py
try:
    import cv2
    print(f"✅ OpenCV version: {cv2.__version__}")
except ImportError as e:
    print(f"❌ OpenCV not installed: {e}")

try:
    import moviepy.editor as mp
    print(f"✅ MoviePy imported successfully")
except ImportError as e:
    print(f"❌ MoviePy not installed: {e}")

try:
    from ingestion import VideoIngestion
    print(f"✅ VideoIngestion class imported successfully")
    ingestor = VideoIngestion()
    print(f"✅ VideoIngestion initialized: {ingestor.upload_folder}")
except Exception as e:
    print(f"❌ Error: {e}")