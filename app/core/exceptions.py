class TriageBotException(Exception):
    """Base exception for TriageBot"""
    pass

class ConfigurationError(TriageBotException):
    """Raised when configuration is missing or invalid"""
    pass

class LLMError(TriageBotException):
    """Raised when LLM service fails"""
    pass

class GitHubAPIError(TriageBotException):
    """Raised when GitHub API fails"""
    pass
