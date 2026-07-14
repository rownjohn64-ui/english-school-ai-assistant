from pathlib import Path
import chromadb
from chromadb.api.models.Collection import Collection

from config import settings
from services.openai_client import sync_client

COLLECTION_NAME = "english_school_docs"
CHROMA_PATH = Path("storage/chroma")

class OpenAIEmbeddingFunction:
    def __call__(self, input: list[str]) -> list[list[float]]:
        response = sync_client.embeddings.create(
            model=settings.embedding_model,
            input=input,
        )
        return [item.embedding for item in response.data]

def get_collection() -> Collection:
    CHROMA_PATH.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=OpenAIEmbeddingFunction(),
        metadata={"hnsw:space": "cosine"},
    )
