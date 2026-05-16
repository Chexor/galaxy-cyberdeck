# Architecture Overview

The `galaxy-cyberdeck` project follows a modular, phased approach to building a portable smart terminal.

## Phase 1: Phone + Laptop (Current)
In this phase, we use the Laptop as a "proxy" for the Raspberry Pi. This allows for faster debugging and code iteration.

- **Galaxy Phone:** Acts as the sensor node. It runs a Flask server that wraps `Termux:API` calls into a RESTful interface.
- **Laptop:** Runs the Python client that polls the phone for data.

## Phase 2: Raspberry Pi Integration (Future)
Once the communication is stable, the Laptop client code is migrated to a Raspberry Pi. The Pi then becomes the central brain of the cyberdeck, using the phone as a dedicated sensor and display module.

## Data Flow
1. **Client** (Laptop/Pi) sends HTTP GET request to **Server** (Phone).
2. **Server** executes local `termux-*` command.
3. **Server** parses command output and returns JSON.
4. **Client** parses JSON and processes the data for AI/Robotics logic.
