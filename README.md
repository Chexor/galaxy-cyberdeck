# Galaxy Cyberdeck 🌌📱

Turn your Samsung Galaxy phone into a portable smart terminal and sensor node for your homelab and robotics projects.

## Project Goal
Create a bridge between Android's powerful hardware sensors (GPS, Accelerometer, Battery) and a central controller (initially a Laptop, later a Raspberry Pi).

## Quick Start (Phase 2)
This project is now in **Phase 2: Pi Deployment**. We are moving the "Brain" to a Raspberry Pi.

### 1. Setup the Phone
- Install **Termux**, **Termux:API**, and **Termux:Boot**.
- Clone this repo in Termux.
- Run `python termux-node/sensor_server.py`.
- See [Termux Setup Guide](docs/setup-termux.md) for details.

### 2. Setup the Pi
- Clone this repo on your Raspberry Pi.
- Update `config.py` with your phone's IP address.
- Run `python pi-client/read_sensors.py`.
- See [Pi Setup Guide](docs/setup-raspberry-pi.md) for details.

## Project Structure
- `termux-node/`: Flask server for the Android phone.
- `pi-client/`: Polling client for the Raspberry Pi.
- `config.py`: Central configuration for device IPs and ports.
- `docs/`: Setup and architectural documentation.

## API Endpoints (Phase 1)
- `GET /battery`: Battery level, health, and charging status.
- `GET /accelerometer`: Real-time X, Y, Z motion data.
- `GET /snapshot`: Captures and returns a JPEG photo from the back camera.
- `GET /torch/on` / `GET /torch/off`: Controls the phone's flashlight.
- `GET /info`: Device model and OS version.

## Usage
### Taking a Photo:
```bash
curl -o capture.jpg http://<PHONE_IP>:5000/snapshot
```

### Controlling the Torch:
```bash
curl http://<PHONE_IP>:5000/torch/on
```

## Why Laptop First? (Phase 1)
We used the laptop for initial prototyping to allow for:
- Immediate feedback.
- Robust debugging tools.
- Faster code deployment.

## Future Plans
- **Phase 3:** Camera streaming (MJPEG/WebRTC).
- **Phase 4:** Integration with ErikaHQ AI backend.
