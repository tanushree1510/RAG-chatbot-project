from src.db import get_client, get_or_create_collection
from sentence_transformers import SentenceTransformer

# Initialize embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

client = get_client()
collection = get_or_create_collection(client)

def embed_texts(texts):
    # Convert texts to embeddings
    return embed_model.encode(texts, convert_to_numpy=True)

def retrieve(query: str, k: int = 13):
    # Embed the query
    q_emb = embed_texts([query])[0]  # numpy array

    # Convert to nested list for Chroma
    q_emb_list = [q_emb.tolist()]

    # Query Chroma collection
    res = collection.query(
        query_embeddings=q_emb_list,
        n_results=k,
        include=["documents", "metadatas"]
    )

    hits = []
    for i in range(len(res["ids"][0])):
        hits.append({
            "document": res["documents"][0][i],
            "metadata": res["metadatas"][0][i]
        })
    return hits
