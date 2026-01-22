from sentence_transformers import SentenceTransformer
from app.config.settings import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class EmbeddingService:
    def __init__(self):
        self.model_name = settings.EMBEDDING_MODEL
        try:
            # Load model (this might take time on first run)
            self.model = SentenceTransformer(self.model_name)
            self.available = True
        except Exception as e:
            logger.warning(f"Failed to load embedding model: {e}")
            self.available = False

    def encode(self, text: str) -> list[float]:
        if not self.available:
            return []
        
        try:
            embedding = self.model.encode(text)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error encoding text: {e}")
            return []

# Singleton instance
# We initialize it lazily or here. For now, here.
# Warning: This makes startup slower.
try:
    embedding_service = EmbeddingService()
except Exception:
    embedding_service = None
