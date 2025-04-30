import logging
from typing import Optional

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Return a configured logger for the given module name.
    Console output includes timestamp, level, and module name.
    Args:
        name (Optional[str]): Logger name/module. Defaults to root logger.
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
