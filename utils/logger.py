# utils/logger.py

import logging

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance with a standard format.

    Args:
        name (str): The name of the logger (usually __name__).

    Returns:
        logging.Logger: A logger instance.
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Prevent duplicate handlers
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)  # You can make this dynamic via .env later

    return logger
