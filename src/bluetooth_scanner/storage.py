"""
Data storage management for the Bluetooth Scanner.
"""
from datetime import datetime
from typing import List, Optional, Dict
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from .config import ConfigManager
from .logger import Logger

Base = declarative_base()

class Device(Base):
    """Database model for Bluetooth devices."""
    __tablename__ = 'devices'
    
    mac_address = Column(String, primary_key=True)
    device_name = Column(String)
    device_class = Column(String)
    manufacturer = Column(String)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    scan_results = relationship("ScanResult", back_populates="device")

class ScanResult(Base):
    """Database model for scan results."""
    __tablename__ = 'scan_results'
    
    id = Column(Integer, primary_key=True)
    device_mac = Column(String, ForeignKey('devices.mac_address'))
    scan_time = Column(DateTime, default=datetime.utcnow)
    signal_strength = Column(Integer)
    device_type = Column(String)
    is_mobile = Column(Boolean)
    
    device = relationship("Device", back_populates="scan_results")
    properties = relationship("DeviceProperty", back_populates="scan_result")

class DeviceProperty(Base):
    """Database model for device properties."""
    __tablename__ = 'device_properties'
    
    id = Column(Integer, primary_key=True)
    scan_result_id = Column(Integer, ForeignKey('scan_results.id'))
    property_name = Column(String)
    property_value = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    scan_result = relationship("ScanResult", back_populates="properties")

class StorageManager:
    """Manages data storage operations."""
    
    def __init__(self, config_manager: ConfigManager, logger: Logger):
        self.config = config_manager.get_config()
        self.logger = logger
        self.engine = create_engine(f"sqlite:///{self.config.db_path}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def store_device(self, device_info: Dict) -> None:
        """Store or update device information."""
        session = self.Session()
        try:
            device = session.query(Device).filter_by(
                mac_address=device_info['mac_address']
            ).first()
            
            if device:
                device.device_name = device_info.get('device_name', device.device_name)
                device.device_class = device_info.get('device_class', device.device_class)
                device.manufacturer = device_info.get('manufacturer', device.manufacturer)
                device.last_seen = datetime.utcnow()
            else:
                device = Device(**device_info)
                session.add(device)
            
            session.commit()
            self.logger.log_storage_operation("store_device", f"Stored device: {device_info['mac_address']}")
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error storing device: {str(e)}")
        finally:
            session.close()
    
    def store_scan_result(self, scan_result: Dict) -> None:
        """Store scan result information."""
        session = self.Session()
        try:
            result = ScanResult(**scan_result)
            session.add(result)
            session.commit()
            self.logger.log_storage_operation("store_scan_result", f"Stored scan result for device: {scan_result['device_mac']}")
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error storing scan result: {str(e)}")
        finally:
            session.close()
    
    def get_device_history(self, mac_address: str, days: Optional[int] = None) -> List[Dict]:
        """Retrieve device history."""
        session = self.Session()
        try:
            query = session.query(ScanResult).filter_by(device_mac=mac_address)
            if days:
                cutoff_date = datetime.utcnow() - timedelta(days=days)
                query = query.filter(ScanResult.scan_time >= cutoff_date)
            
            results = query.order_by(ScanResult.scan_time.desc()).all()
            return [self._scan_result_to_dict(result) for result in results]
        finally:
            session.close()
    
    def cleanup_old_data(self) -> None:
        """Remove data older than retention period."""
        session = self.Session()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=self.config.retention_days)
            session.query(ScanResult).filter(ScanResult.scan_time < cutoff_date).delete()
            session.commit()
            self.logger.log_storage_operation("cleanup", f"Removed data older than {self.config.retention_days} days")
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error cleaning up old data: {str(e)}")
        finally:
            session.close()
    
    def _scan_result_to_dict(self, result: ScanResult) -> Dict:
        """Convert scan result to dictionary."""
        return {
            'scan_time': result.scan_time,
            'signal_strength': result.signal_strength,
            'device_type': result.device_type,
            'is_mobile': result.is_mobile,
            'properties': {
                prop.property_name: prop.property_value
                for prop in result.properties
            }
        } 