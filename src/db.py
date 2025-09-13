import chromadb

CHROMA_DB_DIR = "chroma_db_data"

def get_client():
    # Persistent client (stores vectors on disk)
    return chromadb.PersistentClient(path=CHROMA_DB_DIR)

def get_or_create_collection(client, name="college_info"):
    return client.get_or_create_collection(name=name)
