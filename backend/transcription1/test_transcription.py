from transcription import VideoTranscriber
import json
import sys

print("🎤 Starting transcription test...")

# Initialize transcriber
print("Loading model...")
transcriber = VideoTranscriber(model_size="tiny", device="cpu", compute_type="float32")
print("✓ Model loaded")

# Transcribe
audio_file = "test.wav"
print(f"Transcribing {audio_file}...")
result = transcriber.transcribe(audio_file)

# Display results
print(f"\n✅ Transcription completed!")
print(f"📊 Detected language: {result['language']}")
print(f"📈 Confidence: {result['language_probability']:.2%}")
print(f"📝 Number of segments: {len(result['segments'])}")

if result['segments']:
    print(f"\n📄 Transcription result:")
    for i, segment in enumerate(result['segments']):
        print(f"  {i+1}. [{segment['start']:.1f}s - {segment['end']:.1f}s] {segment['text']}")
else:
    print("⚠️ No segments found - audio might be silent or too short")

# Save to file
output_file = "transcription_result.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"\n💾 Full results saved to {output_file}")

# Show file size
import os
size = os.path.getsize(output_file)
print(f"📁 Output file size: {size} bytes")