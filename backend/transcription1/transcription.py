# transcription.py - UPDATED VERSION
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
            # Par phrase (déjà fait par Whisper)
            for i, segment in enumerate(transcription['segments']):
                chunks.append({
                    'chunk_id': i,
                    'text': segment['text'],
                    'start': segment['start'],
                    'end': segment['end'],
                    'words': segment.get('words', [])
                })
        
        elif strategy == "temporal":
            # Par fenêtre temporelle (ex: 30 secondes)
            window_size = 30  # secondes
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


# Add main block for testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: py transcription.py <audio_file>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    
    print(f"🎤 Transcribing {audio_file}...")
    transcriber = VideoTranscriber(model_size="tiny", device="cpu")
    result = transcriber.transcribe(audio_file)
    
    print(f"✅ Language: {result['language']} (confidence: {result['language_probability']:.2%})")
    print(f"📝 Segments found: {len(result['segments'])}")
    
    for segment in result['segments']:
        print(f"  [{segment['start']:.1f}s -> {segment['end']:.1f}s] {segment['text']}")
    
    # Save to JSON
    output_file = audio_file.replace('.wav', '_transcription.json').replace('.mp3', '_transcription.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"💾 Saved to {output_file}")