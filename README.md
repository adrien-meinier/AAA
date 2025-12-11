# Challenge Triple A - Monitoring Dashboard

A real-time Linux system monitoring dashboard that generates an HTML interface displaying CPU, memory, processes, and file system statistics.

## Description

This project monitors a Linux virtual machine and generates a web dashboard every 30 seconds with:
- System information (hostname, OS, uptime, IP address)
- CPU usage and specifications
- Memory consumption
- Top 3 processes by CPU usage
- File type distribution in a specified directory

## Prerequisites

- Linux-based operating system (Ubuntu recommended)
- Python 3.x
- pip3 (Python package manager)
- Apache2 web server (or similar)
- Basic knowledge of terminal commands

## Installation

### Install Python and dependencies

```bash
# Install Python 3
sudo apt install python3 -y

# Install pip3
sudo apt install pip3 -y

# Install psutil library
sudo pip3 install psutil
```

### Required Python libraries

The monitoring script uses the following libraries:
```python
import psutil      # System and process monitoring
import platform    # System platform information
import socket      # Network information
import time        # Time management
import os          # Operating system interface
import re          # Regular expressions
from datetime import datetime, timedelta  # Date and time information
```

### Setup project directory

```bash
# Clone the repository
git clone https://github.com/adrien-meinier/AAA.git
cd AAA

# Copy files to web server directory
sudo mkdir -p /var/www/html/monitoring
sudo cp -r * /var/www/html/monitoring/

# Set proper permissions
sudo chown -R www-data:www-data /var/www/html/monitoring

```

## Usage

### Launch the monitoring script

```bash
sudo python3 /var/www/html/monitoring/monitor.py
```

The script will run continuously and regenerate `index.html` every 30 seconds.

### Open dashboard in browser

1. Find your VM's IPv4 address:
```bash
hostname -I
```

2. Open your web browser and navigate to:
```
http://[your-vm-ipv4]/monitoring/
```

Example: `http://192.168.1.100/monitoring/`

3. The dashboard will display real-time system statistics

4. Stop the monitoring script with `Ctrl+C`

## Features

- **System Overview**: Hostname, OS version, boot time, uptime, logged-in users
- **Network Info**: Local IP address
- **CPU Monitoring**: Core count, frequency, real-time usage percentage
- **Memory Tracking**: Total/used RAM with percentage
- **Process Analysis**: Top 3 CPU-intensive processes
- **File Statistics**: Distribution of .txt, .py, .pdf, .jpg files in `sample_data/` directory
- **Color-coded Status**: Green (0-50%), Orange (51-80%), Red (81-100%)
- **Automatic Updates**: Dashboard regenerates every 30 seconds

## Screenshots

<img width="501" height="100" alt="image" src="https://github.com/user-attachments/assets/de3950f5-f1c9-443c-954b-1b4af97f5d74" />

<img width="428" height="281" alt="image" src="https://github.com/user-attachments/assets/71bc118f-7f37-4574-8f90-c698d32bbe65" />

<img width="584" height="473" alt="image" src="https://github.com/user-attachments/assets/7613ccce-d402-4c79-9fee-8b1ed8a17c5d" />


## Challenges Encountered

- Understanding `psutil` library documentation for cross-platform compatibility
- Managing template variable replacement without a templating engine
- Handling file encoding issues across different operating systems
- Synchronizing dashboard refresh rate with data collection intervals
- Configuring proper permissions for web server directory access

## Possible Improvements

- Add disk usage statistics and network traffic monitoring
- Implement historical data visualization with graphs/charts
- Add export functionality for monitoring data (CSV/JSON)
- Include system alerts for critical resource thresholds
- Support for Windows and macOS monitoring
- Add authentication for remote access security

## Author

**Adrien Meinier**  
**Loick MIchel**  
**Andrés Montes Zuluaga**
- GitHub: [@adrien-meinier](https://github.com/adrien-meinier)
- Repository: [AAA](https://github.com/adrien-meinier/AAA)

*Project completed as part of the Triple A Challenge*
