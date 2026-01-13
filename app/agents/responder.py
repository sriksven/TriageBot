from app.agents.base import BaseAgent
from app.services.llm import llm_service
from app.models.domain import GitHubIssue
from app.config.settings import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class ResponderAgent(BaseAgent):
    def __init__(self):
        self.templates = {
            "bug": """
            Thanks for reporting this bug! Our {team} will investigate.
            Priority: {priority}

            To help us resolve this faster, please ensure you have provided:
            - Version information
            - Steps to reproduce
            - Expected vs actual behavior
            """,
            "feature": """
            Thanks for the suggestion! We've added this to our backlog for review.
            The product team will evaluate it in the next planning session.
            """,
            "question": """
            Thanks for asking! A member of our {team} will get back to you shortly.
            In the meantime, please check our documentation.
            """,
            "security": """
            SECURITY ACKNOWLEDGEMENT: We have received your report.
            Our security team has been notified immediately. Please do NOT disclose this issue publicly until resolved.
            """
        }

    async def process(self, issue: GitHubIssue, category: str = "question", team: str = "triage-team") -> dict:
        logger.info(f"Generating response for issue #{issue.number} (Category: {category})")
        
        # 1. Try to generate a custom response using LLM
        prompt = f"""
        You are a helpful GitHub bot assistant.
        Issue Title: {issue.title}
        Issue Body: {issue.body}
        Category: {category}
        Assigned Team: {team}
        
        Generate a polite, helpful response to the user. 
        - Acknowledge the issue type ({category}).
        - Mention it has been routed to the {team}.
        - Be concise and professional.
        - Do not promise a specific timeline, but say someone will look at it.
        """
        
        try:
            response_text = await llm_service.generate_content(prompt)
            if not response_text or "Unavailable" in response_text:
                raise Exception("LLM unavailable")
                
        except Exception as e:
            logger.warning(f"Error generating LLM response: {e}. Falling back to template.")
            # Fallback to template
            template = self.templates.get(category, self.templates["question"])
            response_text = template.replace("{team}", team).replace("{priority}", "Normal")
            
        return {
            "response": response_text.strip(),
            "generated_by": "llm" if "Unavailable" not in response_text else "template"
        }
