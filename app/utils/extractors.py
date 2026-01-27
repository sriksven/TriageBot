import re

class ContextExtractor:
    @staticmethod
    def extract_error_logs(text: str) -> list[str]:
        """
        Extract code blocks that look like error logs or stack traces.
        """
        if not text:
            return []
            
        # Look for triple backticks
        code_blocks = re.findall(r'```(?:[\w\s]*\n)(.*?)```', text, re.DOTALL)
        
        # Heuristic: assume blocks with "Exception", "Error", "Traceback" are logs
        error_blocks = []
        for block in code_blocks:
            if any(keyword in block for keyword in ["Exception", "Error", "Traceback", "at "]):
                error_blocks.append(block)
                
        return error_blocks
        
    @staticmethod
    def extract_urls(text: str) -> list[str]:
        """Extract URLs from text"""
        if not text:
            return []
        
        # Simple URL regex
        return re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)

    @staticmethod
    def extract_mentions(text: str) -> list[str]:
        """Extract GitHub username mentions"""
        if not text:
            return []
            
        return re.findall(r'@([a-zA-Z0-9-]+)', text)
