"""
Configuration management for the Bluetooth Scanner.
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

@dataclass
class ScannerConfig:
    """Configuration settings for the Bluetooth scanner."""
    scan_interval: int = 10  # seconds between scans
    scan_duration: int = 5   # seconds to scan
    db_path: str = "bluetooth_devices.db"
    log_level: str = "INFO"
    retention_days: int = 30
    min_signal_strength: int = -90  # dBm

class ConfigManager:
    """Manages configuration loading and access."""
    
    def __init__(self):
        load_dotenv()
        self.config = ScannerConfig(
            scan_interval=int(os.getenv("SCAN_INTERVAL", "10")),
            scan_duration=int(os.getenv("SCAN_DURATION", "5")),
            db_path=os.getenv("DB_PATH", "bluetooth_devices.db"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            retention_days=int(os.getenv("RETENTION_DAYS", "30")),
            min_signal_strength=int(os.getenv("MIN_SIGNAL_STRENGTH", "-90"))
        )
    
    def get_config(self) -> ScannerConfig:
        """Get the current configuration."""
        return self.config
    
    def update_config(self, **kwargs) -> None:
        """Update configuration values."""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value) 