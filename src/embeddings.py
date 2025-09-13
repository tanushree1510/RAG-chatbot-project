from sentence_transformers import SentenceTransformer
from typing import List

# Load a small, fast local model
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts_local(texts: List[str]):
    """
    Creates embeddings locally without OpenAI.
    Returns a list of lists (vectors).
    """
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings.tolist()
