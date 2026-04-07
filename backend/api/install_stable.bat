@echo off
echo ========================================
echo Installation stable des dépendances
echo ========================================
echo.

cd /d C:\Users\flori\projet_video_qa
call venv\Scripts\activate.bat

echo [1/8] Desinstallation des packages conflictuels...
pip uninstall -y numpy chromadb sentence-transformers torch transformers tokenizers huggingface-hub safetensors openai-whisper streamlit opencv-python moviepy

echo [2/8] Installation de NumPy 1.24.3...
pip install numpy==1.24.3

echo [3/8] Installation de PyTorch...
pip install torch==2.1.0 --index-url https://download.pytorch.org/whl/cpu

echo [4/8] Installation de HuggingFace Hub compatible...
pip install huggingface-hub==0.19.4

echo [5/8] Installation de Tokenizers compatible...
pip install tokenizers==0.19.1

echo [6/8] Installation de Transformers...
pip install transformers==4.40.2 safetensors==0.4.1

echo [7/8] Installation de ChromaDB et Sentence-Transformers...
pip install chromadb==0.4.22 sentence-transformers==2.2.2

echo [8/8] Installation des autres dependances...
pip install openai-whisper streamlit==1.28.1 opencv-python==4.8.1.78 moviepy==1.0.3

echo.
echo ========================================
echo Verification des installations...
echo ========================================
python -c "import numpy; print('[OK] NumPy', numpy.__version__)"
python -c "import torch; print('[OK] PyTorch', torch.__version__)"
python -c "import transformers; print('[OK] Transformers', transformers.__version__)"
python -c "import tokenizers; print('[OK] Tokenizers', tokenizers.__version__)"
python -c "import huggingface_hub; print('[OK] HuggingFace Hub', huggingface_hub.__version__)"
python -c "import chromadb; print('[OK] ChromaDB', chromadb.__version__)"
python -c "from sentence_transformers import SentenceTransformer; print('[OK] Sentence-Transformers')"
python -c "import whisper; print('[OK] Whisper')"

echo.
echo Installation terminee avec succes!
echo Lancez l'application: streamlit run backend/api/app.py
pause