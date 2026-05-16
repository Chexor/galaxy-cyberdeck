# Galaxy Cyberdeck Project Instructions

This document outlines the foundational mandates, architectural patterns, and development workflows for the `galaxy-cyberdeck` project.

## Core Mandates

### Development Strategy: Laptop First
- **Target Architecture (Phase 1):** Galaxy Phone <-> Laptop.
- **Rationale:** Faster iteration, easier debugging, and stable testing environment before moving to Raspberry Pi.
- **Constraint:** Do NOT integrate with Raspberry Pi until the Laptop-to-Phone communication is fully validated.

### Architectural Principles
- **Modularity:** Keep the Termux node and the Client decoupled.
- **Simplicity:** Prefer simple, readable Python code over complex frameworks.
- **Stability:** Prioritize working, stable implementations of basic sensor data before adding features like camera streaming or AI.

### Testing Workflow
Strict adherence to the following testing order is required for any new sensor or feature:
1. **Manual Validation:** Test the `termux-api` command directly in the Termux shell.
2. **Local Server Validation:** Test the Flask endpoint locally on the phone using `curl localhost:port`.
3. **Remote API Validation:** Test connectivity and response from the Laptop workstation.
4. **Client Validation:** Ensure the Python client correctly parses and displays the data.
5. **Deployment Validation:** Only after steps 1-4 are successful, deploy and test on the Raspberry Pi.

## Directory Structure
- `termux-node/`: Flask server running on the Android phone.
- `laptop-client/`: Python client for development and testing (later adapted to `pi-client`).
- `docs/`: Step-by-step setup guides and architectural documentation.

## Technical Stack
- **Languages:** Python 3.x
- **Server:** Flask (Termux)
- **Client:** Python `requests` library
- **APIs:** `Termux:API` (Android sensor access)
