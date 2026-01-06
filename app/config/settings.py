import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "TriageBot"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # GitHub
    GITHUB_TOKEN: str = ""
    GITHUB_WEBHOOK_SECRET: str = ""
    
    # Gemini API
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"
    GEMINI_TEMPERATURE: float = 0.1
    
    # Database
    DATABASE_URL: str = "sqlite:///./triagebot.db"
    
    # ChromaDB
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    
    # Embeddings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # Agent Configuration
    CLASSIFICATION_CONFIDENCE_THRESHOLD: float = 0.7
    SIMILARITY_THRESHOLD: float = 0.85

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
