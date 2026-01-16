from fastapi import APIRouter, Depends, Header, HTTPException, Request, BackgroundTasks
from app.core.security import verify_github_signature
from app.models.domain import WebhookPayload
from app.agents.orchestrator import orchestrator
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/webhooks/github")
async def github_webhook(
    background_tasks: BackgroundTasks,
    payload: WebhookPayload,
    request: Request,
    _: None = Depends(verify_github_signature)
):
    """
    Handle GitHub webhooks.
    """
    if payload.action not in ["opened", "reopened"]:
        logger.info(f"Ignoring action {payload.action}")
        return {"status": "ignored", "reason": f"Action {payload.action} not supported"}
    
    if not payload.issue:
        return {"status": "ignored", "reason": "Not an issue event"}
        
    logger.info(f"Received webhook for issue #{payload.issue.number}: {payload.issue.title}")
    
    # Process in background to respond quickly to GitHub
    background_tasks.add_task(orchestrator.process_issue, payload)
    
    return {"status": "accepted", "message": "Issue processing started"}
