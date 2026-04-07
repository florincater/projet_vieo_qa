# test_imports.py
import sys
print(f"Python: {sys.version}")

import numpy as np
print(f"NumPy: {np.__version__}")

import chromadb
print(f"ChromaDB: {chromadb.__version__}")

from sentence_transformers import SentenceTransformer
print("SentenceTransformers: OK")

import whisper
print("Whisper: OK")

import streamlit as st
print("Streamlit: OK")

print("\n✅ Tous les imports sont réussis!")