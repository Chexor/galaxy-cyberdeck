# Termux Setup Guide

Follow these steps to prepare your Galaxy phone for the `galaxy-cyberdeck` project.

## 1. Install Prerequisites
On your Android phone, install the following from F-Droid (preferred):
- **Termux**: The terminal emulator.
- **Termux:API**: Allows Termux to access Android hardware sensors.

## 2. Update and Install Packages
Open Termux and run:
```bash
pkg update && pkg upgrade
pkg install python termux-api
```

## 3. Install Python dependencies
Navigate to the `termux-node` directory (you can use `git clone` to get this repo on your phone):
```bash
pip install -r requirements.txt
```

## 4. Grant Permissions
For the sensors to work, you may need to grant "Appear on top" or "Background execution" permissions to Termux in Android settings.
Also, run a test command to trigger the permission prompt:
```bash
termux-battery-status
```

## 5. Start the Server
Run the Flask server:
```bash
python sensor_server.py
```
Note the IP address of your phone on your local Wi-Fi.
