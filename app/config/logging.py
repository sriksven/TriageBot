import logging
import sys
from app.config.settings import get_settings

def setup_logging():
    settings = get_settings()
    
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
