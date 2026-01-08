import hashlib
import hmac
from fastapi import HTTPException, Request, status
from app.config.settings import get_settings

settings = get_settings()

async def verify_github_signature(request: Request):
    """
    Verify that the request came from GitHub.
    """
    if not settings.GITHUB_WEBHOOK_SECRET:
        # If no secret is configured, skip verification (development mode only)
        if settings.DEBUG:
            return
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Webhook secret not configured"
        )
        
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing signature headers"
        )
        
    # Read the raw body
    body = await request.body()
    
    # Calculate the expected signature
    secret = settings.GITHUB_WEBHOOK_SECRET.encode()
    expected_signature = "sha256=" + hmac.new(
        secret,
        body,
        hashlib.sha256
    ).hexdigest()
    
    # Compare signatures
    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid signature"
        )
