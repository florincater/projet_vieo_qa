import subprocess
import os
import shutil

def extract_audio(video_path, output_audio_path=None):
    """Extract audio from video using ffmpeg"""
    
    # Find ffmpeg executable
    ffmpeg_path = shutil.which('ffmpeg')
    if not ffmpeg_path:
        # Try common Windows paths
        common_paths = [
            'C:\\ffmpeg\\bin\\ffmpeg.exe',
            'C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe',
        ]
        for path in common_paths:
            if os.path.exists(path):
                ffmpeg_path = path
                break
        
        if not ffmpeg_path:
            raise Exception("FFmpeg not found. Please install ffmpeg and add it to PATH")
    
    if output_audio_path is None:
        output_audio_path = video_path.replace('.mp4', '.mp3').replace('.avi', '.mp3')
    
    # FFmpeg command
    cmd = [
        ffmpeg_path,
        '-i', video_path,
        '-vn',  # No video
        '-acodec', 'mp3',
        '-q:a', '2',
        '-y',  # Overwrite output file
        output_audio_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            raise Exception(f"FFmpeg error: {result.stderr}")
        return output_audio_path
    except subprocess.TimeoutExpired:
        raise Exception("Audio extraction timed out after 5 minutes")
    except Exception as e:
        raise Exception(f"Failed to extract audio: {e}")