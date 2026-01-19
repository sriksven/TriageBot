import pytest
from app.agents.router import RouterAgent
from app.models.domain import GitHubIssue, GitHubUser

@pytest.mark.asyncio
async def test_router_bug_auth():
    issue = GitHubIssue(
        url="", repository_url="", labels_url="", comments_url="", events_url="", html_url="",
        id=1, node_id="1", number=1, title="Login failed",
        user=GitHubUser(login="user", id=1, type="User"),
        state="open", locked=False, comments=0,
        created_at="2023-01-01T00:00:00Z", updated_at="2023-01-01T00:00:00Z",
        author_association="OWNER",
        body="Authentication issue"
    )
    
    agent = RouterAgent()
    result = await agent.process(issue, category="bug")
    
    assert result["team"] == "backend-team"

@pytest.mark.asyncio
async def test_router_feature_default():
    issue = GitHubIssue(
        url="", repository_url="", labels_url="", comments_url="", events_url="", html_url="",
        id=1, node_id="1", number=1, title="New detailed view",
        user=GitHubUser(login="user", id=1, type="User"),
        state="open", locked=False, comments=0,
        created_at="2023-01-01T00:00:00Z", updated_at="2023-01-01T00:00:00Z",
        author_association="OWNER",
        body="Add a new view"
    )
    
    agent = RouterAgent()
    result = await agent.process(issue, category="feature")
    
    assert result["team"] == "product-team"
