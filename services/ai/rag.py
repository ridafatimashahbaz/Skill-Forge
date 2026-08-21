import os
import chromadb
from chromadb.utils import embedding_functions

CHROMA_HOST = os.getenv("CHROMA_HOST", "chroma")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
COLLECTION_NAME = "skillforge_knowledge"

# Free, local sentence-transformer embedding model -- no external API key required
_embedding_fn = embedding_functions.DefaultEmbeddingFunction()


def get_client():
    return chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)


def get_collection():
    client = get_client()
    return client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=_embedding_fn)


def add_documents(docs: list[dict]):
    """docs: [{"id": str, "text": str, "metadata": {...}}]"""
    collection = get_collection()
    collection.upsert(
        ids=[d["id"] for d in docs],
        documents=[d["text"] for d in docs],
        metadatas=[d.get("metadata", {}) for d in docs],
    )


def search(query: str, n_results: int = 4, topic_filter: str | None = None):
    collection = get_collection()
    where = {"topic": topic_filter} if topic_filter else None
    results = collection.query(query_texts=[query], n_results=n_results, where=where)
    hits = []
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    for text, meta in zip(docs, metas):
        hits.append({"text": text, "metadata": meta})
    return hits
