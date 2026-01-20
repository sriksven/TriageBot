import pytest
from app.agents.orchestrator import orchestrator
from app.models.domain import WebhookPayload, GitHubIssue, GitHubUser, GitHubRepository
from app.config.settings import get_settings

# Mock LLM service to avoid API calls and key errors
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_full_workflow():
    payload = WebhookPayload(
        action="opened",
        repository=GitHubRepository(
            id=1, name="test-repo", full_name="user/test-repo", 
            private=False, owner=GitHubUser(login="user", id=1, type="User"), html_url="http://github.com/user/test-repo"
        ),
        sender=GitHubUser(login="user", id=1, type="User"),
        issue=GitHubIssue(
            url="http://api.github.com/repos/user/test-repo/issues/1",
            repository_url="http://api.github.com/repos/user/test-repo",
            labels_url="", comments_url="", events_url="", html_url="",
            id=1, node_id="1", number=1, title="Login page is broken",
            user=GitHubUser(login="user", id=1, type="User"),
            state="open", locked=False, comments=0,
            created_at="2023-01-01T00:00:00Z", updated_at="2023-01-01T00:00:00Z",
            author_association="OWNER",
            body="I cannot login when I click the button."
        )
    )
    
    # We mock the generate_content to return a predictable JSON
    with patch("app.services.llm.LLMService.generate_content", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = '{"category": "bug", "confidence": 0.95, "reasoning": "It mentions login broken"}'
        
        # Run the orchestrator
        # We can't easily assert on internal logs without a complex setup, 
        # but running this ensures no exceptions are raised and covers the code paths.
        await orchestrator.process_issue(payload)
        
        # Verify LLM was called
        mock_llm.assert_called_once()
