import logging
from app.models.domain import WebhookPayload

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    def __init__(self):
        pass
        
    async def process_issue(self, payload: WebhookPayload):
        """
        Orchestrate the processing of a new issue.
        For now, just log the event.
        """
        if not payload.issue:
            logger.warning("Payload received but no issue data found")
            return
            
        issue = payload.issue
        logger.info(f"Processing issue #{issue.number}: {issue.title}")
        
        # Call classification agent
        from app.agents.classifier import ClassifierAgent
        classifier = ClassifierAgent()
        classification_result = await classifier.process(issue)
        
        logger.info(f"Issue #{issue.number} classified as: {classification_result['category']}")

        # Call similarity agent (Phase 2)
        from app.agents.similarity import SimilarityAgent
        similarity_agent = SimilarityAgent()
        similarity_result = await similarity_agent.process(issue)
        
        if similarity_result["is_duplicate"]:
            duplicates = [d['number'] for d in similarity_result['duplicates']]
            logger.info(f"Issue #{issue.number} is a potential duplicate of: {duplicates}")
            # Add context to routing/response if needed

        
        # Call routing agent
        from app.agents.router import RouterAgent
        router = RouterAgent()
        routing_result = await router.process(issue, category=classification_result.get("category", "question"))
        
        logger.info(f"Issue #{issue.number} routed to: {routing_result['team']}")

        # Apply label via GitHub API
        from app.services.github import github_service
        category = classification_result.get("category", "question")
        await github_service.add_labels(issue, [f"triage/{category}"])

        # Call response agent
        from app.agents.responder import ResponderAgent
        responder = ResponderAgent()
        
        # Add duplicates context if available
        context = {}
        if 'similarity_result' in locals() and similarity_result['is_duplicate']:
             context['duplicates'] = similarity_result['duplicates']

        response_result = await responder.process(
            issue, 
            category=classification_result.get("category", "question"),
            team=routing_result.get("team", "triage-team")
        )
        
        # Post comment via GitHub API
        if response_result.get("response"):
            await github_service.post_comment(issue, response_result["response"])
        
        logger.info(f"Finished processing issue #{issue.number}")

# Global instance for now
orchestrator = AgentOrchestrator()
