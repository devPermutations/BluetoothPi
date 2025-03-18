#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    echo -e "${2}${1}${NC}"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if running as root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        print_message "Please run as root (use sudo)" "$RED"
        exit 1
    fi
}

# Function to check system requirements
check_requirements() {
    print_message "Checking system requirements..." "$YELLOW"
    
    # Check Python version
    if ! command_exists python3; then
        print_message "Python 3 is not installed. Installing..." "$YELLOW"
        apt-get update && apt-get install -y python3 python3-pip python3-venv
    fi
    
    # Check BlueZ
    if ! command_exists bluetoothctl; then
        print_message "BlueZ is not installed. Installing..." "$YELLOW"
        apt-get update && apt-get install -y bluetooth bluez
    fi
    
    # Check D-Bus
    if ! command_exists dbus-daemon; then
        print_message "D-Bus is not installed. Installing..." "$YELLOW"
        apt-get update && apt-get install -y dbus
    fi
    
    print_message "System requirements check completed." "$GREEN"
}

# Function to create virtual environment
setup_virtual_env() {
    print_message "Setting up Python virtual environment..." "$YELLOW"
    
    # Create virtual environment
    python3 -m venv venv
    
    # Activate virtual environment and install dependencies
    source venv/bin/activate
    pip install --upgrade pip
    pip install -e .
    
    print_message "Virtual environment setup completed." "$GREEN"
}

# Function to create configuration file
setup_config() {
    print_message "Setting up configuration..." "$YELLOW"
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        cat > .env << EOL
SCAN_INTERVAL=10
SCAN_DURATION=5
DB_PATH=bluetooth_devices.db
LOG_LEVEL=INFO
RETENTION_DAYS=30
MIN_SIGNAL_STRENGTH=-90
EOL
        print_message "Created .env file with default configuration." "$GREEN"
    else
        print_message ".env file already exists. Skipping..." "$YELLOW"
    fi
}

# Function to setup systemd service
setup_service() {
    print_message "Setting up systemd service..." "$YELLOW"
    
    # Create systemd service file
    cat > /etc/systemd/system/bluetooth-scanner.service << EOL
[Unit]
Description=Bluetooth Device Scanner
After=bluetooth.target

[Service]
Type=simple
User=pi
WorkingDirectory=$(pwd)
Environment=PYTHONPATH=$(pwd)/src
ExecStart=$(pwd)/venv/bin/bluetooth-scanner
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL
    
    # Reload systemd and enable service
    systemctl daemon-reload
    systemctl enable bluetooth-scanner
    systemctl start bluetooth-scanner
    
    print_message "Systemd service setup completed." "$GREEN"
}

# Function to check Bluetooth permissions
setup_bluetooth_permissions() {
    print_message "Setting up Bluetooth permissions..." "$YELLOW"
    
    # Add user to bluetooth group
    usermod -a -G bluetooth pi
    
    # Ensure Bluetooth service is running
    systemctl enable bluetooth
    systemctl start bluetooth
    
    print_message "Bluetooth permissions setup completed." "$GREEN"
}

# Main installation process
main() {
    print_message "Starting Bluetooth Scanner installation..." "$YELLOW"
    
    # Check if running as root
    check_root
    
    # Check and install requirements
    check_requirements
    
    # Setup virtual environment
    setup_virtual_env
    
    # Setup configuration
    setup_config
    
    # Setup Bluetooth permissions
    setup_bluetooth_permissions
    
    # Setup systemd service
    setup_service
    
    print_message "Installation completed successfully!" "$GREEN"
    print_message "The Bluetooth Scanner service has been started." "$GREEN"
    print_message "You can check its status with: sudo systemctl status bluetooth-scanner" "$YELLOW"
    print_message "To view logs: sudo journalctl -u bluetooth-scanner" "$YELLOW"
    print_message "To run the scanner manually: bluetooth-scanner" "$YELLOW"
}

# Run main installation process
main 