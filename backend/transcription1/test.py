from gtts import gTTS

text = """Hello DeepSeek! This is a test of my video transcription project. 
The system is working correctly and can transcribe audio with timestamps.
This will help me process videos for my AI project."""

tts = gTTS(text=text, lang='en')
tts.save("test_audio.mp3")
print("✅ Created test_audio.mp3")