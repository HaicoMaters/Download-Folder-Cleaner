"""Module providing global access to the change logger."""

from change_logger import ChangeLogger

_logger_instance = None

def initialize_logger(base_path: str) -> None:
    """Initialize the global logger."""
    global _logger_instance
    _logger_instance = ChangeLogger(base_path)

def set_base_path(base_path: str) -> None:
    """Set the base path for the logger."""
    if _logger_instance is None:
        raise RuntimeError("Logger not initialized. Call initialize_logger first.")
    _logger_instance.base_path = base_path

def get_logger() -> ChangeLogger:
    """Get the global logger instance."""
    if _logger_instance is None:
        raise RuntimeError("Logger not initialized. Call initialize_logger first.")
    return _logger_instance
