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

# Function to check if running as root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        print_message "Please run as root (use sudo)" "$RED"
        exit 1
    fi
}

# Function to stop and remove service
remove_service() {
    print_message "Stopping and removing systemd service..." "$YELLOW"
    
    # Stop the service if it's running
    if systemctl is-active --quiet bluetooth-scanner; then
        systemctl stop bluetooth-scanner
        print_message "Stopped bluetooth-scanner service" "$GREEN"
    fi
    
    # Disable and remove the service
    systemctl disable bluetooth-scanner
    rm -f /etc/systemd/system/bluetooth-scanner.service
    systemctl daemon-reload
    
    print_message "Removed bluetooth-scanner service" "$GREEN"
}

# Function to remove virtual environment
remove_virtual_env() {
    print_message "Removing virtual environment..." "$YELLOW"
    
    if [ -d "venv" ]; then
        rm -rf venv
        print_message "Removed virtual environment" "$GREEN"
    else
        print_message "Virtual environment not found" "$YELLOW"
    fi
}

# Function to remove database and logs
remove_data() {
    print_message "Removing database and log files..." "$YELLOW"
    
    # Remove database file
    if [ -f "bluetooth_devices.db" ]; then
        rm -f bluetooth_devices.db
        print_message "Removed database file" "$GREEN"
    else
        print_message "Database file not found" "$YELLOW"
    fi
    
    # Remove log files
    if [ -f "bluetooth_scanner.log" ]; then
        rm -f bluetooth_scanner.log
        print_message "Removed log file" "$GREEN"
    else
        print_message "Log file not found" "$YELLOW"
    fi
}

# Function to remove configuration
remove_config() {
    print_message "Removing configuration files..." "$YELLOW"
    
    # Remove .env file
    if [ -f ".env" ]; then
        rm -f .env
        print_message "Removed .env file" "$GREEN"
    else
        print_message ".env file not found" "$YELLOW"
    fi
}

# Function to remove Python package
remove_package() {
    print_message "Removing Python package..." "$YELLOW"
    
    # Activate virtual environment if it exists
    if [ -d "venv" ]; then
        source venv/bin/activate
        pip uninstall -y bluetooth_scanner
        print_message "Removed Python package" "$GREEN"
    else
        print_message "Virtual environment not found, skipping package removal" "$YELLOW"
    fi
}

# Function to remove system-wide command links
remove_commands() {
    print_message "Removing system-wide commands..." "$YELLOW"
    
    # Remove symbolic links
    rm -f /usr/local/bin/bluetooth-scanner
    rm -f /usr/local/bin/bluetooth-visualizer
    
    print_message "Removed system-wide commands" "$GREEN"
}

# Function to clean up build artifacts
cleanup_build() {
    print_message "Cleaning up build artifacts..." "$YELLOW"
    
    # Remove Python cache files
    find . -type d -name "__pycache__" -exec rm -r {} +
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete
    find . -type f -name "*.pyd" -delete
    
    # Remove build directories
    rm -rf build/ dist/ *.egg-info/
    
    print_message "Cleaned up build artifacts" "$GREEN"
}

# Main uninstallation process
main() {
    print_message "Starting Bluetooth Scanner uninstallation..." "$YELLOW"
    
    # Check if running as root
    check_root
    
    # Stop and remove service
    remove_service
    
    # Remove system-wide commands
    remove_commands
    
    # Remove Python package
    remove_package
    
    # Remove virtual environment
    remove_virtual_env
    
    # Remove database and logs
    remove_data
    
    # Remove configuration
    remove_config
    
    # Clean up build artifacts
    cleanup_build
    
    print_message "Uninstallation completed successfully!" "$GREEN"
    print_message "All Bluetooth Scanner components have been removed." "$GREEN"
}

# Run main uninstallation process
main 