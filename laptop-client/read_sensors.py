import requests
import time
import argparse
import sys

def get_sensor_data(ip, port, endpoint):
    url = f"http://{ip}:{port}/{endpoint}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {endpoint}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Galaxy Cyberdeck Laptop Client")
    parser.add_argument("--ip", required=True, help="IP address of the Galaxy phone")
    parser.add_argument("--port", default=5000, type=int, help="Port of the Termux server (default: 5000)")
    parser.add_argument("--interval", default=2, type=int, help="Polling interval in seconds (default: 2)")
    
    args = parser.parse_args()

    print(f"Connecting to Galaxy Cyberdeck at {args.ip}:{args.port}...")
    
    # Test connection
    status = get_sensor_data(args.ip, args.port, "")
    if status:
        print(f"Server Status: {status.get('status')} - {status.get('message')}")
    else:
        print("Could not connect to server. Check IP and ensure server is running.")
        sys.exit(1)

    try:
        while True:
            battery = get_sensor_data(args.ip, args.port, "battery")
            if battery:
                print(f"\n--- Battery Status ---")
                print(f"Level: {battery.get('percentage')}%")
                print(f"Status: {battery.get('status')}")
                print(f"Health: {battery.get('health')}")
            
            # Fetch Accelerometer
            accel = get_sensor_data(args.ip, args.port, "accelerometer")
            if accel and "error" not in accel:
                x, y, z = accel.get("x", 0), accel.get("y", 0), accel.get("z", 0)
                print(f"--- Orientation ---")
                print(f"X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}")
                
                # Simple orientation logic
                if abs(z) > 8 and abs(x) < 2 and abs(y) < 2:
                    orientation = "Flat on Table"
                elif abs(x) > 5 or abs(y) > 5:
                    orientation = "Tilted / Handheld"
                else:
                    orientation = "Moving..."
                print(f"Mode: {orientation}")

            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()
