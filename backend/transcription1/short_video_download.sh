bash
# Using yt-dlp to download audio from a short video (optional)
py -m pip install yt-dlp
yt-dlp -x --audio-format mp3 -o "sample_audio.%(ext)s" "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Just an example