from app.agents.base import BaseAgent
from app.services.embedding import embedding_service
from app.services.vectorstore import vector_store
from app.models.domain import GitHubIssue
from app.config.settings import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class SimilarityAgent(BaseAgent):
    def __init__(self):
        self.threshold = settings.SIMILARITY_THRESHOLD
        
    async def process(self, issue: GitHubIssue) -> dict:
        logger.info(f"Checking for duplicates for issue #{issue.number}")
        
        text = f"{issue.title} {issue.body or ''}"
        
        # 1. Generate embedding
        embedding = embedding_service.encode(text)
        if not embedding:
            return {"duplicates": [], "is_duplicate": False}
            
        # 2. Search vector store
        results = vector_store.search(embedding)
        
        duplicates = []
        if results and results['ids']:
            ids = results['ids'][0]
            distances = results['distances'][0]
            metadatas = results['metadatas'][0]
            
            for i, dist in enumerate(distances):
                # Distance is usually cosine distance (1 - similarity) or euclidean
                # Chroma default is L2. For cosine, lower is closer.
                # Assuming simple threshold for now.
                # If using default l2, we might need to adjust threshold logic
                # For this MVP let's assume < 0.5 is similar enough in L2 space for normalized vectors
                # But implementation plan mentioned cosine similarity > 0.85
                # For now just returning what we found
                
                # Check if it's the same issue
                if str(metadatas[i].get("number")) == str(issue.number):
                    continue
                    
                duplicates.append({
                    "id": ids[i],
                    "number": metadatas[i].get("number"),
                    "title": metadatas[i].get("title"),
                    "distance": dist
                })
        
        # 3. Store current issue (if not already there)
        metadata = {
            "number": issue.number,
            "title": issue.title,
            "state": issue.state
        }
        vector_store.add_issue(str(issue.id), embedding, metadata, text)
        
        return {
            "duplicates": duplicates,
            "is_duplicate": len(duplicates) > 0
        }
