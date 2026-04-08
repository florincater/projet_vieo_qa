# backend/api/app.py - Fixed version
import streamlit as st
import sys
import os
import json
from pathlib import Path
###
# app.py in your project root
import streamlit as st

#st.title("Video Transcription App")
# Your existing code here


# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

st.set_page_config(page_title="Video QA System", layout="wide")

st.title("🎥 Video Question Answering System")
st.markdown("Upload a video or audio file to transcribe and ask questions")

# Sidebar
with st.sidebar:
    st.header("Settings")
    model_size = st.selectbox("Whisper Model", ["tiny", "base", "small", "medium"], index=1)
    st.info("Larger models are more accurate but slower")

# Main content
uploaded_file = st.file_uploader(
    "Choose a video or audio file",
    type=['mp4', 'avi', 'mov', 'mkv', 'mp3', 'wav', 'm4a']
)

if uploaded_file:
    # Save file
    temp_file = f"temp_{uploaded_file.name}"
    with open(temp_file, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Display video or audio (FIXED: separate statements)
    if uploaded_file.name.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        st.video(temp_file)
    else:
        st.audio(temp_file)
    
    # Process button
    if st.button("Transcribe"):
        with st.spinner("Processing..."):
            try:
                # Import transcription module
                from transcription import VideoTranscriber
                
                # Determine if we need to extract audio
                if uploaded_file.name.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                    st.info("Extracting audio from video...")
                    # For now, use the video file directly (Whisper can handle video files)
                    audio_file = temp_file
                else:
                    audio_file = temp_file
                
                # Transcribe
                st.info(f"Transcribing with {model_size} model...")
                transcriber = VideoTranscriber(model_size=model_size, device="cpu")
                result = transcriber.transcribe(audio_file)
                
                # Display results
                st.success("✅ Transcription complete!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Language", result['language'])
                with col2:
                    st.metric("Confidence", f"{result['language_probability']:.1%}")
                
                st.subheader("📝 Transcription")
                
                # Display transcription with expandable sections
                for i, segment in enumerate(result['segments']):
                    with st.expander(f"Segment {i+1} ({segment['start']:.1f}s - {segment['end']:.1f}s)"):
                        st.write(segment['text'])
                        if segment.get('words'):
                            st.caption(f"Words: {len(segment['words'])}")
                
                # Save and download
                output_file = f"transcription_{uploaded_file.name}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                
                with open(output_file, 'rb') as f:
                    st.download_button(
                        label="📥 Download Transcription (JSON)",
                        data=f,
                        file_name=output_file,
                        mime="application/json"
                    )
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Make sure ffmpeg is installed for video processing")
            
            finally:
                # Cleanup (optional - uncomment if you want to delete temp files)
                # if os.path.exists(temp_file):
                #     os.remove(temp_file)
                pass