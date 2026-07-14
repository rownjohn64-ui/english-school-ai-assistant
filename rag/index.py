from pathlib import Path

from rag.store import get_collection
from rag.loader import load_documents, split_text

DATA_DIR = Path("data")

def index_documents() -> dict[str, int]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    documents = load_documents(DATA_DIR)

    collection = get_collection()
    existing = collection.get()
    if existing.get("ids"):
        collection.delete(ids=existing["ids"])

    ids: list[str] = []
    texts: list[str] = []
    metadatas: list[dict] = []

    for doc in documents:
        chunks = split_text(doc["text"])
        for index, chunk in enumerate(chunks):
            ids.append(f"{doc['source']}::{index}")
            texts.append(chunk)
            metadatas.append(
                {
                    "source": doc["source"],
                    "chunk": index,
                }
            )

    if texts:
        collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
        )

    return {
        "documents": len(documents),
        "chunks": len(texts),
    }
