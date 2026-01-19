import pytest
from app.agents.classifier import ClassifierAgent
from app.models.domain import GitHubIssue, GitHubUser
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_classifier_success():
    issue = GitHubIssue(
        url="", repository_url="", labels_url="", comments_url="", events_url="", html_url="",
        id=1, node_id="1", number=1, title="Login failed",
        user=GitHubUser(login="user", id=1, type="User"),
        state="open", locked=False, comments=0,
        created_at="2023-01-01T00:00:00Z", updated_at="2023-01-01T00:00:00Z",
        author_association="OWNER",
        body="I cannot login"
    )
    
    with patch("app.services.llm.LLMService.generate_content", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = '{"category": "bug", "confidence": 0.9}'
        
        agent = ClassifierAgent()
        result = await agent.process(issue)
        
        assert result["category"] == "bug"
        assert result["confidence"] == 0.9

@pytest.mark.asyncio
async def test_classifier_fallback():
    issue = GitHubIssue(
        url="", repository_url="", labels_url="", comments_url="", events_url="", html_url="",
        id=1, node_id="1", number=1, title="Login failed",
        user=GitHubUser(login="user", id=1, type="User"),
        state="open", locked=False, comments=0,
        created_at="2023-01-01T00:00:00Z", updated_at="2023-01-01T00:00:00Z",
        author_association="OWNER",
        body="I cannot login"
    )
    
    with patch("app.services.llm.LLMService.generate_content", new_callable=AsyncMock) as mock_llm:
        mock_llm.side_effect = Exception("API Error")
        
        agent = ClassifierAgent()
        result = await agent.process(issue)
        
        assert result["category"] == "question"
        assert result["confidence"] == 0.0
