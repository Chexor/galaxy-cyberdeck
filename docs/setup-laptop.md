# Laptop Setup Guide

This guide explains how to set up your laptop as the primary development and testing workstation for Phase 1.

## 1. Prerequisites
- Python 3.x installed.
- Access to the same Wi-Fi network as the Galaxy phone.

## 2. Install Dependencies
Navigate to the `laptop-client` directory and install the requirements:
```bash
pip install -r requirements.txt
```

## 3. Identify Phone IP
Find your Galaxy phone's IP address (usually found in Settings > About Phone > Status or via Termux using `ifconfig`).

## 4. Run the Client
Run the polling client, replacing `PHONE_IP` with your phone's address:
```bash
python read_sensors.py --ip PHONE_IP
```

## 5. Troubleshooting
- **Connection Refused:** Ensure the Flask server is running on the phone and the IP is correct.
- **Timeout:** Check if your laptop and phone can ping each other. Android's battery saver or firewall might block connections.
