import httpx
from app.config.settings import get_settings
from app.models.domain import GitHubIssue
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class GitHubService:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    
    async def add_labels(self, issue: GitHubIssue, labels: list[str]):
        """
        Add labels to an issue.
        """
        if not settings.GITHUB_TOKEN:
            logger.warning("GITHUB_TOKEN not set. Skipping label application.")
            return

        url = f"{issue.url}/labels"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, 
                    json={"labels": labels},
                    headers=self.headers
                )
                response.raise_for_status()
                logger.info(f"Added labels {labels} to issue #{issue.number}")
        except Exception as e:
            logger.error(f"Failed to add labels to issue #{issue.number}: {e}")

    async def post_comment(self, issue: GitHubIssue, body: str):
        """
        Post a comment on an issue.
        """
        if not settings.GITHUB_TOKEN:
            logger.warning("GITHUB_TOKEN not set. Skipping comment.")
            return

        url = f"{issue.url}/comments"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, 
                    json={"body": body},
                    headers=self.headers
                )
                response.raise_for_status()
                logger.info(f"Posted comment on issue #{issue.number}")
        except Exception as e:
            logger.error(f"Failed to post comment on issue #{issue.number}: {e}")

# Singleton instance
github_service = GitHubService()
