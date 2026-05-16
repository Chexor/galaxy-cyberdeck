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
        return {"error": str(e)}

def clear_screen():
    # ANSI escape code to clear screen and move cursor to (0,0)
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()

def main():
    banner_art = r"""
   _____       _                                  
  / ____|     | |                                 
 | |  __  __ _| | __ ___  ___   _                 
 | | |_ |/ _` | |/ _` \ \/ / | | |                
 | |__| | (_| | | (_| |>  <| |_| |                
  \_____|\__,_|_|\__,_/_/\_\\__, |                
   _____      _              __/ |           _    
  / ____|    | |            |___/ |         | |   
 | |    _   _| |__   ___ _ __ __| | ___  ___| | __
 | |   | | | | '_ \ / _ \ '__/ _` |/ _ \/ __| |/ /
 | |___| |_| | |_) |  __/ | | (_| |  __/ (__|   < 
  \_____\__, |_.__/ \___|_|  \__,_|\___|\___|_|\_\
         __/ |                                    
        |___/                                     
    """
    
    parser = argparse.ArgumentParser(description="Galaxy Cyberdeck Universal Client")
    parser.add_argument("--ip", default=config.PHONE_IP, help=f"IP address of the Galaxy phone (default: {config.PHONE_IP})")
    parser.add_argument("--port", default=config.PHONE_PORT, type=int, help=f"Port of the Termux server (default: {config.PHONE_PORT})")
    parser.add_argument("--interval", default=config.POLL_INTERVAL, type=int, help=f"Polling interval in seconds (default: {config.POLL_INTERVAL})")
    
    args = parser.parse_args()

    # Fetch Static Info Once
    info = get_sensor_data(args.ip, args.port, "info")
    model = info.get("model", "Unknown") if info and "error" not in info else "Searching..."

    try:
        while True:
            # Gather live data
            battery = get_sensor_data(args.ip, args.port, "battery")
            accel = get_sensor_data(args.ip, args.port, "accelerometer")

            # Update Display
            clear_screen()
            print(f"\033[95m{banner_art}\033[0m")
            print(f"\033[92m[CONNECTED]\033[0m Phone IP: {args.ip}:{args.port}")
            print(f"Device: {model}")

            if battery and "error" not in battery:
                level = battery.get("percentage", 0)
                status = battery.get("status", "Unknown")
                # Simple progress bar for battery
                bar_len = 20
                filled = int(level / 100 * bar_len)
                bar = "█" * filled + "-" * (bar_len - filled)
                print(f"\n--- Power ---")
                print(f"[{bar}] {level}% ({status})")
            
            if accel and "error" not in accel:
                x, y, z = accel.get("x", 0), accel.get("y", 0), accel.get("z", 0)
                print(f"\n--- Orientation ---")
                print(f"X: {x:6.2f} | Y: {y:6.2f} | Z: {z:6.2f}")
                
                if abs(z) > 8 and abs(x) < 2 and abs(y) < 2:
                    orientation = "Flat on Table"
                elif abs(x) > 5 or abs(y) > 5:
                    orientation = "Tilted / Handheld"
                else:
                    orientation = "Sensing..."
                print(f"Status: {orientation}")

            print(f"\n\033[90mPress Ctrl+C to exit. Refreshing every {args.interval}s...\033[0m")
            time.sleep(args.interval)
            
    except KeyboardInterrupt:
        print("\n\033[93m[DISCONNECTED]\033[0m Cyberdeck Client Stopped.")

if __name__ == "__main__":
    main()
