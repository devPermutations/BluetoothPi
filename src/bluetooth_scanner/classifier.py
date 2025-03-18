"""
Device classification for the Bluetooth Scanner.
"""
from typing import Dict, Optional
from .logger import Logger

class DeviceClassifier:
    """Classifies Bluetooth devices based on their properties."""
    
    # Common mobile phone device classes
    MOBILE_PHONE_CLASSES = {
        '0x000500',  # Phone
        '0x000504',  # Smartphone
        '0x000508',  # Mobile phone
    }
    
    # Common mobile phone manufacturers
    MOBILE_MANUFACTURERS = {
        'Apple',
        'Samsung',
        'Google',
        'Xiaomi',
        'Huawei',
        'OnePlus',
        'Sony',
        'LG',
        'Motorola',
        'Nokia',
    }
    
    def __init__(self, logger: Logger):
        self.logger = logger
    
    def classify_device(self, device_info: Dict) -> Dict:
        """
        Classify a device based on its properties.
        Returns a dictionary with classification results.
        """
        classification = {
            'is_mobile': False,
            'device_type': 'unknown',
            'confidence': 0.0
        }
        
        # Check device class
        device_class = device_info.get('device_class', '')
        if device_class in self.MOBILE_PHONE_CLASSES:
            classification['is_mobile'] = True
            classification['device_type'] = 'mobile_phone'
            classification['confidence'] = 0.8
        
        # Check manufacturer
        manufacturer = device_info.get('manufacturer', '').lower()
        if any(m.lower() in manufacturer for m in self.MOBILE_MANUFACTURERS):
            if not classification['is_mobile']:
                classification['is_mobile'] = True
                classification['device_type'] = 'mobile_phone'
                classification['confidence'] = 0.7
            else:
                classification['confidence'] = 0.9
        
        # Check device name patterns
        device_name = device_info.get('device_name', '').lower()
        mobile_patterns = {'iphone', 'samsung', 'galaxy', 'pixel', 'xiaomi', 'huawei'}
        if any(pattern in device_name for pattern in mobile_patterns):
            if not classification['is_mobile']:
                classification['is_mobile'] = True
                classification['device_type'] = 'mobile_phone'
                classification['confidence'] = 0.6
            else:
                classification['confidence'] = min(1.0, classification['confidence'] + 0.2)
        
        # Log classification
        self.logger.log_classification(
            device_info,
            f"{'mobile phone' if classification['is_mobile'] else 'other device'} "
            f"(confidence: {classification['confidence']:.2f})"
        )
        
        return classification
    
    def get_device_properties(self, device_info: Dict) -> Dict:
        """
        Extract and normalize device properties.
        Returns a dictionary of normalized properties.
        """
        properties = {
            'device_name': device_info.get('device_name', ''),
            'device_class': device_info.get('device_class', ''),
            'manufacturer': device_info.get('manufacturer', ''),
            'signal_strength': device_info.get('signal_strength', 0),
            'address': device_info.get('mac_address', ''),
            'last_seen': device_info.get('last_seen', ''),
        }
        
        # Normalize values
        if properties['device_name']:
            properties['device_name'] = properties['device_name'].strip()
        if properties['manufacturer']:
            properties['manufacturer'] = properties['manufacturer'].strip()
        
        return properties 