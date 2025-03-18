"""
Main Bluetooth scanner service.
"""
import time
from typing import Dict, List, Optional
from pydbus import SystemBus
from .config import ConfigManager
from .logger import Logger
from .storage import StorageManager
from .classifier import DeviceClassifier

class BluetoothScanner:
    """Main Bluetooth scanner service."""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.logger = Logger(self.config_manager)
        self.storage = StorageManager(self.config_manager, self.logger)
        self.classifier = DeviceClassifier(self.logger)
        self.bus = SystemBus()
        self.adapter = None
        self.scanning = False
    
    def initialize(self) -> bool:
        """Initialize the Bluetooth scanner."""
        try:
            # Get the default adapter
            self.adapter = self.bus.get('org.bluez', '/org/bluez/hci0')
            self.logger.info("Bluetooth adapter initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Bluetooth adapter: {str(e)}")
            return False
    
    def start_scanning(self) -> None:
        """Start the Bluetooth scanning process."""
        if not self.adapter:
            if not self.initialize():
                return
        
        self.scanning = True
        self.logger.info("Starting Bluetooth scanning")
        
        try:
            while self.scanning:
                # Start discovery
                self.adapter.StartDiscovery()
                time.sleep(self.config_manager.get_config().scan_duration)
                
                # Stop discovery
                self.adapter.StopDiscovery()
                
                # Process discovered devices
                self._process_discovered_devices()
                
                # Wait before next scan
                time.sleep(self.config_manager.get_config().scan_interval)
                
        except Exception as e:
            self.logger.error(f"Error during scanning: {str(e)}")
        finally:
            self.stop_scanning()
    
    def stop_scanning(self) -> None:
        """Stop the Bluetooth scanning process."""
        if self.scanning:
            try:
                if self.adapter:
                    self.adapter.StopDiscovery()
                self.scanning = False
                self.logger.info("Stopped Bluetooth scanning")
            except Exception as e:
                self.logger.error(f"Error stopping scan: {str(e)}")
    
    def _process_discovered_devices(self) -> None:
        """Process discovered Bluetooth devices."""
        try:
            # Get discovered devices
            devices = self._get_discovered_devices()
            
            for device in devices:
                # Get device properties
                device_info = self._get_device_properties(device)
                
                # Classify device
                classification = self.classifier.classify_device(device_info)
                
                # Store device information
                self.storage.store_device(device_info)
                
                # Store scan result
                scan_result = {
                    'device_mac': device_info['mac_address'],
                    'signal_strength': device_info.get('signal_strength', 0),
                    'device_type': classification['device_type'],
                    'is_mobile': classification['is_mobile']
                }
                self.storage.store_scan_result(scan_result)
                
        except Exception as e:
            self.logger.error(f"Error processing discovered devices: {str(e)}")
    
    def _get_discovered_devices(self) -> List[str]:
        """Get list of discovered device paths."""
        try:
            objects = self.bus.get('org.bluez', '/').GetManagedObjects()
            devices = []
            
            for path, interfaces in objects.items():
                if 'org.bluez.Device1' in interfaces:
                    devices.append(path)
            
            return devices
        except Exception as e:
            self.logger.error(f"Error getting discovered devices: {str(e)}")
            return []
    
    def _get_device_properties(self, device_path: str) -> Dict:
        """Get properties for a specific device."""
        try:
            device = self.bus.get('org.bluez', device_path)
            properties = device.GetAll('org.bluez.Device1')
            
            return {
                'mac_address': properties.get('Address', ''),
                'device_name': properties.get('Name', ''),
                'device_class': properties.get('Class', ''),
                'manufacturer': properties.get('ManufacturerData', {}).get('0x0000', ''),
                'signal_strength': properties.get('RSSI', 0),
                'last_seen': time.time()
            }
        except Exception as e:
            self.logger.error(f"Error getting device properties: {str(e)}")
            return {}
    
    def get_mobile_device_count(self) -> int:
        """Get the current count of mobile devices."""
        try:
            session = self.storage.Session()
            count = session.query(self.storage.ScanResult).filter_by(
                is_mobile=True
            ).distinct(self.storage.ScanResult.device_mac).count()
            session.close()
            return count
        except Exception as e:
            self.logger.error(f"Error getting mobile device count: {str(e)}")
            return 0 