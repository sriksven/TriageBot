from app.agents.base import BaseAgent
from app.models.domain import GitHubIssue
import logging

logger = logging.getLogger(__name__)

class RouterAgent(BaseAgent):
    def __init__(self):
        # Basic routing rules
        self.rules = {
            "bug": {
                "auth": "backend-team",
                "login": "backend-team",
                "ui": "frontend-team",
                "css": "frontend-team",
                "security": "security-team"
            },
            "feature": {
                "default": "product-team"
            },
            "security": {
                "default": "security-team"
            },
            "docs": {
                "default": "docs-team"
            }
        }
        
    async def process(self, issue: GitHubIssue, category: str = "question") -> dict:
        logger.info(f"Routing issue #{issue.number} (Category: {category})")
        
        # Default team
        team = "triage-team"
        
        # Check rule based routing
        text = f"{issue.title} {issue.body}".lower()
        
        if category in self.rules:
            category_rules = self.rules[category]
            
            # Check keywords for specific sub-routing
            for keyword, target_team in category_rules.items():
                if keyword != "default" and keyword in text:
                    team = target_team
                    break
            
            # Use default for category if no keyword matched
            if team == "triage-team" and "default" in category_rules:
                team = category_rules["default"]
                
        logger.info(f"Routed to: {team}")
        
        return {
            "team": team,
            "reasoning": f"Based on category '{category}' and keywords in valid rules."
        }
