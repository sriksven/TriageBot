import google.generativeai as genai
from app.config.settings import get_settings
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
            self.available = True
        else:
            logger.warning("GEMINI_API_KEY not set. LLM service unavailable.")
            self.available = False
            
    async def generate_content(self, prompt: str) -> str:
        if not self.available:
            return "LLM Service Unavailable"
            
        try:
            # Gemini execution is synchronous, wrapping if needed or just calling directly
            # For high throughput, we might want to run this in a threadpool
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=settings.GEMINI_TEMPERATURE
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            raise

# Singleton instance
llm_service = LLMService()
