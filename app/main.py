from fastapi import FastAPI
from app.config.settings import get_settings
from app.config.logging import setup_logging
from app.api.v1.endpoints import health, webhooks

# Setup logging
setup_logging()
settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered GitHub issue triaging system",
    version="0.1.0"
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(webhooks.router, prefix="/api/v1", tags=["webhooks"])


@app.get("/")
async def root():
    return {"message": "TriageBot is running"}
