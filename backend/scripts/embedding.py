# embedding.py
from sentence_transformers import SentenceTransformer

# Load once
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed(text: str):
    return model.encode(text).tolist()
