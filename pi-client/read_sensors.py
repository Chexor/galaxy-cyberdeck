import requests
import time
import argparse
import sys
import os

# Add parent directory to path so we can import config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    import config
except ImportError:
    # Fallback if config.py is missing
    class config:
        PHONE_IP = "YOUR_PHONE_IP_HERE"
        PHONE_PORT = 5000
        POLL_INTERVAL = 1

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
    print("""
    \033[95m
     ________  ________  ___       ________     ___ ___  ___      ___ 
    |\   ____\|\   __  \|\  \     |\   __  \   |\  \|\  \|\  \    /  /|
    \ \  \___|\ \  \|\  \ \  \    \ \  \|\  \  \ \  \ \  \ \  \  /  / /
     \ \  \  __\ \   __  \ \  \    \ \   __  \  \ \  \ \  \ \  \/  / / 
      \ \  \|\  \ \  \ \  \ \  \____\ \  \ \  \  \ \  \ \  \ \    / /  
       \ \_______\ \__\ \__\ \_______\ \__\ \__\  \ \__\ \__\ \__/ /   
        \|_______|\|__|\|__|\|_______|\|__|\|__|   \|__|\|__|\|__|/    
                                                                      
     ________  ___  ___  ________  _______   ________  ________  ________  ___  __   
    |\   ____\|\  \|\  \|\   __  \|\  ___ \ |\   __  \|\   ____\|\   ___  \|\  \|\  \ 
    \ \  \___|\ \  \\\  \ \  \|\ /\ \   __/|\ \  \|\  \ \  \___|\ \  \__\ \ \  \/  /|_
     \ \  \    \ \  \\\  \ \   __  \ \  \_|/_\ \   _  _\\ \  \    \ \  \__\ \ \   ___  \
      \ \  \____\ \  \\\  \ \  \|\  \ \  \_|\ \ \  \\  \\ \  \____\ \  \__\ \ \  \\ \  \
       \ \_______\ \_______\ \_______\ \_______\ \__\\ _\\ \_______\ \_______\ \__\\ \__\
        \|_______|\|_______|\|_______|\|_______|\|__|\|__|\|_______|\|_______|\|__| \|__|
    \033[0m
    \033[92m[SYSTEM READY]\033[0m Initializing Galaxy-Cyberdeck Node...
    """)
    parser = argparse.ArgumentParser(description="Galaxy Cyberdeck Pi Client")
    parser.add_argument("--ip", default=config.PHONE_IP, help=f"IP address of the Galaxy phone (default: {config.PHONE_IP})")
    parser.add_argument("--port", default=config.PHONE_PORT, type=int, help=f"Port of the Termux server (default: {config.PHONE_PORT})")
    parser.add_argument("--interval", default=config.POLL_INTERVAL, type=int, help=f"Polling interval in seconds (default: {config.POLL_INTERVAL})")
    
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
