from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime

class GitHubUser(BaseModel):
    login: str
    id: int
    avatar_url: Optional[str] = None
    type: str

class GitHubRepository(BaseModel):
    id: int
    name: str
    full_name: str
    private: bool
    owner: GitHubUser
    html_url: str
    description: Optional[str] = None

class GitHubIssue(BaseModel):
    url: str
    repository_url: str
    labels_url: str
    comments_url: str
    events_url: str
    html_url: str
    id: int
    node_id: str
    number: int
    title: str
    user: GitHubUser
    labels: List[Any] = []
    state: str
    locked: bool
    assignee: Optional[GitHubUser] = None
    assignees: List[GitHubUser] = []
    milestone: Optional[Any] = None
    comments: int
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime] = None
    author_association: str
    active_lock_reason: Optional[str] = None
    body: Optional[str] = None

class WebhookPayload(BaseModel):
    action: str
    issue: Optional[GitHubIssue] = None
    repository: Optional[GitHubRepository] = None
    sender: Optional[GitHubUser] = None
    
    # Allow extra fields since GitHub sends a lot of data
    class Config:
        extra = "allow"
