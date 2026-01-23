import chromadb
from chromadb.config import Settings as ChromaSettings
from app.config.settings import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class VectorStoreService:
    def __init__(self):
        try:
            self.client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
            self.collection = self.client.get_or_create_collection(name="issues")
            self.available = True
        except Exception as e:
            logger.warning(f"Failed to initialize ChromaDB: {e}")
            self.available = False

    def add_issue(self, issue_id: str, embedding: list[float], metadata: dict, text: str):
        if not self.available or not embedding:
            return

        try:
            self.collection.add(
                ids=[str(issue_id)],
                embeddings=[embedding],
                metadatas=[metadata],
                documents=[text]
            )
        except Exception as e:
            logger.error(f"Error adding issue to vector store: {e}")

    def search(self, embedding: list[float], n_results: int = 5):
        if not self.available or not embedding:
            return []

        try:
            results = self.collection.query(
                query_embeddings=[embedding],
                n_results=n_results
            )
            return results
        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            return []

# Singleton instance
vector_store = VectorStoreService()
