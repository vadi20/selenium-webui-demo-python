import logging
import logging.config
import os
from pathlib import Path

def setup_logging():
    """Setup logging configuration"""
    logs_dir = Path('logs')
    if not logs_dir.exists():
        os.makedirs(logs_dir)
    
    logging.config.fileConfig('config/logging.conf')
    logging.captureWarnings(True)

def get_logger(name):
    """Get a logger instance with the given name"""
    # Ensure logging is configured
    if not logging.getLogger().handlers:
        setup_logging()
    
    return logging.getLogger(name)