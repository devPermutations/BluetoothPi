# Bluetooth Device Scanner

A Python-based Bluetooth device scanner that identifies and categorizes mobile phones in a room using the BlueZ D-Bus API.

## Features

- Real-time Bluetooth device scanning
- Mobile phone detection and classification
- Device property tracking and storage
- Configurable scanning parameters
- Comprehensive logging
- Data retention management

## Prerequisites

- Python 3.7 or higher
- BlueZ installed on your system
- D-Bus system service
- SQLite3 (included with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bluetooth-scanner.git
cd bluetooth-scanner
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following options:

```env
SCAN_INTERVAL=10
SCAN_DURATION=5
DB_PATH=bluetooth_devices.db
LOG_LEVEL=INFO
RETENTION_DAYS=30
MIN_SIGNAL_STRENGTH=-90
```

## Usage

Run the scanner:
```bash
python -m bluetooth_scanner
```

The scanner will:
1. Initialize the Bluetooth adapter
2. Start scanning for devices
3. Classify discovered devices
4. Store results in the database
5. Log all activities

To stop the scanner, press Ctrl+C.

## Project Structure

```
bluetooth_scanner/
├── src/
│   └── bluetooth_scanner/
│       ├── __init__.py
│       ├── __main__.py
│       ├── scanner.py
│       ├── classifier.py
│       ├── storage.py
│       ├── config.py
│       └── logger.py
├── docs/
│   ├── architecture.md
│   └── dataflow.md
├── requirements.txt
└── README.md
```

## Development

### Running Tests
```bash
pytest
```

### Code Style
```bash
black src/
pylint src/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
