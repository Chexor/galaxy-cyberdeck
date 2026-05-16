# Raspberry Pi Setup Guide

This guide explains how to set up your Raspberry Pi as the "Brain" of the Galaxy Cyberdeck.

## 1. Operating System
- Use **Raspberry Pi OS Lite (64-bit)**.
- Flash the SD card using the Raspberry Pi Imager.
- Enable **SSH** in the advanced settings (cogwheel icon).

## 2. Initial Setup
Once the Pi is booted and you are logged in via SSH:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3-pip
```

## 3. Clone the Project
```bash
git clone https://github.com/Chexor/galaxy-cyberdeck.git
cd galaxy-cyberdeck
```

## 4. Install Dependencies
```bash
pip install -r pi-client/requirements.txt
```

## 5. Configuration
Edit `config.py` to match your phone's current IP address:
```bash
nano config.py
```
Change `PHONE_IP` to your phone's address (e.g., `192.168.0.137` for Wi-Fi or `192.168.42.129` for USB Tethering).

## 6. Run the Client
```bash
python3 pi-client/read_sensors.py
```

## 7. USB Tethering (Permanent Link)
For a hardwired connection:
1. Connect the phone to the Pi via USB.
2. On the phone: **Settings > Connections > Mobile Hotspot and Tethering > USB Tethering (ON)**.
3. The Pi will see a new network interface (usually `usb0`).
4. Update `config.py` with the phone's tethering IP (check `ip route` on the Pi to find the gateway).
