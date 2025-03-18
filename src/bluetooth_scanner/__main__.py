"""
Main entry point for the Bluetooth scanner.
"""
import signal
import sys
from .scanner import BluetoothScanner
from .logger import Logger
from .config import ConfigManager

def signal_handler(signum, frame):
    """Handle system signals."""
    print("\nStopping Bluetooth scanner...")
    sys.exit(0)

def main():
    """Main entry point."""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Initialize components
    config_manager = ConfigManager()
    logger = Logger(config_manager)
    
    try:
        # Create and initialize scanner
        scanner = BluetoothScanner()
        
        if not scanner.initialize():
            logger.error("Failed to initialize Bluetooth scanner")
            sys.exit(1)
        
        # Start scanning
        logger.info("Starting Bluetooth scanner...")
        scanner.start_scanning()
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 