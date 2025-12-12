"""
Logging utilities
"""

import sys
from loguru import logger
from app.config import settings


def setup_logger():
    """Configure logger with file and console output"""
    
    logger.remove()
    
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=settings.log_level
    )
    
    logger.add(
        settings.log_file,
        rotation="500 MB",
        retention="10 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
        level=settings.log_level
    )
    
    return logger


log = setup_logger()
