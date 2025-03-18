"""
Logging system for the Bluetooth Scanner.
"""
import logging
import sys
from datetime import datetime
from typing import Optional
from .config import ConfigManager

class Logger:
    """Manages logging for the Bluetooth Scanner."""
    
    def __init__(self, config_manager: ConfigManager):
        self.logger = logging.getLogger("bluetooth_scanner")
        self.logger.setLevel(config_manager.get_config().log_level)
        
        # Create handlers
        console_handler = logging.StreamHandler(sys.stdout)
        file_handler = logging.FileHandler("bluetooth_scanner.log")
        
        # Create formatters and add it to handlers
        log_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(log_format)
        file_handler.setFormatter(log_format)
        
        # Add handlers to the logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def info(self, message: str) -> None:
        """Log an info message."""
        self.logger.info(message)
    
    def error(self, message: str) -> None:
        """Log an error message."""
        self.logger.error(message)
    
    def debug(self, message: str) -> None:
        """Log a debug message."""
        self.logger.debug(message)
    
    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(message)
    
    def log_device_discovery(self, device_info: dict) -> None:
        """Log device discovery information."""
        self.info(f"Device discovered: {device_info}")
    
    def log_classification(self, device_info: dict, classification: str) -> None:
        """Log device classification information."""
        self.info(f"Device classified: {device_info} as {classification}")
    
    def log_storage_operation(self, operation: str, details: str) -> None:
        """Log storage operation information."""
        self.debug(f"Storage operation: {operation} - {details}") 