import chromadb
from chromadb.config import Settings
from app.core.config import settings

def get_chroma_client():
    """Returns the ChromaDB client"""
    client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
    return client

def get_collection():
    """Returns the ChromaDB collection"""
    client = get_chroma_client()
    collection = client.get_or_create_collection(
        name="document_chunks",
        metadata={"hnsw:space": "cosine"}
    )
    return collection
