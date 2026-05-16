# Galaxy Cyberdeck 🌌📱

Turn your Samsung Galaxy phone into a portable smart terminal and sensor node for your homelab and robotics projects.

## Project Goal
Create a bridge between Android's powerful hardware sensors (GPS, Accelerometer, Battery) and a central controller (initially a Laptop, later a Raspberry Pi).

## Quick Start (Phase 1)
This project is currently in **Phase 1: Laptop First**. We validate everything on a laptop before deploying to a Pi.

### 1. Setup the Phone
- Install **Termux** and **Termux:API**.
- Clone this repo in Termux.
- Run `python termux-node/sensor_server.py`.
- See [Termux Setup Guide](docs/setup-termux.md) for details.

### 2. Setup the Laptop
- Clone this repo on your laptop.
- Run `python laptop-client/read_sensors.py --ip <PHONE_IP>`.
- See [Laptop Setup Guide](docs/setup-laptop.md) for details.

## API Endpoints (Phase 1)
- `GET /battery`: Battery level, health, and charging status.
- `GET /accelerometer`: Real-time X, Y, Z motion data.
- `GET /snapshot`: Captures and returns a JPEG photo from the back camera.
- `GET /torch/on` / `GET /torch/off`: Controls the phone's flashlight.
- `GET /info`: Device model and OS version.

## Usage
### Taking a Photo from your Laptop:
```bash
curl -o capture.jpg http://<PHONE_IP>:5000/snapshot
```

### Controlling the Torch:
```bash
curl http://<PHONE_IP>:5000/torch/on
```

## Why Laptop First?
Iterating directly on a Raspberry Pi can be slow due to network constraints or hardware access. Developing on a laptop allows for:
- Immediate feedback.
- Robust debugging tools.
- Faster code deployment.

## Future Plans
- **Phase 2:** Raspberry Pi deployment.
- **Phase 3:** Camera streaming (MJPEG/WebRTC).
- **Phase 4:** Integration with ErikaHQ AI backend.
