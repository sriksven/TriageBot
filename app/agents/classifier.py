from app.agents.base import BaseAgent
from app.services.llm import llm_service
from app.models.domain import GitHubIssue
from app.config.settings import get_settings
import logging
import json

logger = logging.getLogger(__name__)
settings = get_settings()

class ClassifierAgent(BaseAgent):
    def __init__(self):
        self.categories = ["bug", "feature", "question", "docs", "security"]
        
    async def process(self, issue: GitHubIssue) -> dict:
        logger.info(f"Classifying issue #{issue.number}")
        
        prompt = f"""
        You are an expert at classifying GitHub issues.
        Categories: {', '.join(self.categories)}
        
        Analyze the following issue and respond with a JSON object containing:
        1. "category": The best matching category from the list above.
        2. "confidence": A float between 0.0 and 1.0 indicating your confidence.
        3. "reasoning": A brief explanation of why you chose this category.
        
        Issue Title: {issue.title}
        
        Issue Body:
        {issue.body or "No description provided."}
        
        Respond ONLY with the valid JSON string.
        """
        
        try:
            response_text = await llm_service.generate_content(prompt)
            
            # Clean up potential markdown formatting in response (e.g. ```json ... ```)
            cleaned_response = response_text.replace("```json", "").replace("```", "").strip()
            
            result = json.loads(cleaned_response)
            
            # Validate category
            if result.get("category") not in self.categories:
                logger.warning(f"Invalid category returned: {result.get('category')}")
                result["category"] = "question" # Default fallback
                
            logger.info(f"Classified as {result['category']} (confidence: {result.get('confidence')})")
            return result
            
        except Exception as e:
            logger.error(f"Classification failed: {e}")
            return {
                "category": "question",
                "confidence": 0.0,
                "reasoning": "Classification failed due to error."
            }
