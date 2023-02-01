__all__ = ["get_logger"]

import logging


def get_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)

    if not logger.handlers:
        # Create handlers
        handler = logging.StreamHandler()
        # Create formatters and add it to handlers
        format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(format)
        # Add handlers to the logger
        logger.addHandler(handler)
        logger.setLevel(level or logging.INFO)

    return logger
