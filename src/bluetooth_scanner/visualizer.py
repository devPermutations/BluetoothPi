"""
Console visualizer for Bluetooth device data.
"""
import time
import signal
import sys
from datetime import datetime
from typing import Dict, List
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich import box
from sqlalchemy import desc
from .storage import StorageManager, Device, ScanResult
from .config import ConfigManager
from .logger import Logger

class BluetoothVisualizer:
    """Console visualizer for Bluetooth device data."""
    
    def __init__(self):
        self.console = Console()
        self.config_manager = ConfigManager()
        self.logger = Logger(self.config_manager)
        self.storage = StorageManager(self.config_manager, self.logger)
        self.running = True
    
    def create_device_table(self, devices: List[Dict]) -> Table:
        """Create a rich table for device data."""
        table = Table(
            title="Bluetooth Devices",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta",
            title_style="bold cyan"
        )
        
        # Add columns
        table.add_column("Name", style="cyan")
        table.add_column("MAC", style="green")
        table.add_column("Type", style="yellow")
        table.add_column("Signal", style="blue")
        table.add_column("Last Seen", style="magenta")
        table.add_column("First Seen", style="magenta")
        
        # Add rows
        for device in devices:
            table.add_row(
                device.get('device_name', 'Unknown'),
                device.get('mac_address', 'Unknown'),
                '📱 Mobile' if device.get('is_mobile') else '📶 Other',
                f"{device.get('signal_strength', 0)} dBm",
                device.get('last_seen', 'Never'),
                device.get('first_seen', 'Never')
            )
        
        return table
    
    def create_stats_panel(self, total_devices: int, mobile_devices: int) -> Panel:
        """Create a statistics panel."""
        stats_text = Text()
        stats_text.append(f"Total Devices: {total_devices}\n", style="bold cyan")
        stats_text.append(f"Mobile Devices: {mobile_devices}\n", style="bold green")
        stats_text.append(f"Other Devices: {total_devices - mobile_devices}\n", style="bold yellow")
        stats_text.append(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="bold magenta")
        
        return Panel(
            stats_text,
            title="Statistics",
            border_style="cyan",
            box=box.ROUNDED
        )
    
    def get_recent_devices(self) -> List[Dict]:
        """Get recent device data from the database."""
        session = self.storage.Session()
        try:
            # Get the most recent scan result for each device
            recent_results = session.query(
                Device,
                ScanResult
            ).join(
                ScanResult,
                Device.mac_address == ScanResult.device_mac
            ).order_by(
                desc(ScanResult.scan_time)
            ).distinct(
                Device.mac_address
            ).all()
            
            devices = []
            for device, result in recent_results:
                devices.append({
                    'mac_address': device.mac_address,
                    'device_name': device.device_name,
                    'device_class': device.device_class,
                    'manufacturer': device.manufacturer,
                    'first_seen': device.first_seen.strftime('%Y-%m-%d %H:%M:%S'),
                    'last_seen': device.last_seen.strftime('%Y-%m-%d %H:%M:%S'),
                    'signal_strength': result.signal_strength,
                    'is_mobile': result.is_mobile
                })
            
            return devices
        finally:
            session.close()
    
    def get_device_counts(self) -> tuple:
        """Get total and mobile device counts."""
        session = self.storage.Session()
        try:
            total = session.query(Device).count()
            mobile = session.query(ScanResult).filter_by(is_mobile=True).distinct(
                ScanResult.device_mac
            ).count()
            return total, mobile
        finally:
            session.close()
    
    def create_layout(self) -> Layout:
        """Create the main layout."""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        return layout
    
    def update_display(self) -> Layout:
        """Update the display with current data."""
        layout = self.create_layout()
        
        # Get current data
        devices = self.get_recent_devices()
        total_devices, mobile_devices = self.get_device_counts()
        
        # Create header
        header_text = Text("Bluetooth Device Scanner - Real-time Monitor", style="bold cyan")
        layout["header"].update(Panel(header_text, style="cyan"))
        
        # Create body with device table
        layout["body"].update(self.create_device_table(devices))
        
        # Create footer with stats
        layout["footer"].update(self.create_stats_panel(total_devices, mobile_devices))
        
        return layout
    
    def run(self) -> None:
        """Run the visualizer."""
        def signal_handler(signum, frame):
            """Handle system signals."""
            self.running = False
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            with Live(self.update_display(), refresh_per_second=1) as live:
                while self.running:
                    live.update(self.update_display())
                    time.sleep(1)
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Stopping visualizer...[/yellow]")
        finally:
            self.console.print("[green]Visualizer stopped.[/green]")

def main():
    """Main entry point for the visualizer."""
    visualizer = BluetoothVisualizer()
    visualizer.run()

if __name__ == "__main__":
    main() 