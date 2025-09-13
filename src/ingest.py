from pathlib import Path
from src.db import get_client, get_or_create_collection

# Function to chunk text for semantic search
def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def ingest(source_dir: str):
    client = get_client()
    collection = get_or_create_collection(client)

    source_path = Path(source_dir)
    files = list(source_path.glob("*.txt"))

    if not files:
        print("No text files found in source directory.")
        return

    documents = []
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            chunks = chunk_text(text)
            for i, chunk in enumerate(chunks):
                documents.append({
                    "id": f"{file_path.stem}_{i}",  # unique ID per chunk
                    "document": chunk,
                    "metadata": {"source": str(file_path)}
                })

    # Insert all documents into Chroma collection
    for doc in documents:
        collection.add(
            ids=[doc["id"]],
            documents=[doc["document"]],
            metadatas=[doc["metadata"]]
        )

    print(f"Ingested {len(documents)} documents into ChromaDB successfully.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Directory containing text files")
    args = parser.parse_args()
    ingest(args.source)
