import subprocess
import json
import os
from flask import Flask, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # This allows the laptop dashboard to talk to the phone

# Paths
SNAPSHOT_PATH = "/data/data/com.termux/files/home/snapshot.jpg"

def run_termux_command(command):
    """Executes a Termux:API command and returns JSON or raw text."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        output = result.stdout.strip()
        
        if result.returncode != 0:
            return {"error": "Command failed", "details": result.stderr}

        # Try to find and parse JSON
        start = output.find('{')
        end = output.rfind('}')
        if start == -1 or end == -1:
            start = output.find('[')
            end = output.rfind(']')
            
        if start != -1 and end != -1:
            try:
                return json.loads(output[start:end+1])
            except:
                pass # Not valid JSON, return raw
        
        return output
    except Exception as e:
        return {"error": "Execution failed", "details": str(e)}

@app.route('/')
def status():
    return jsonify({"status": "online", "message": "Galaxy Cyberdeck Sensor Server"})

@app.route('/battery')
def battery():
    return jsonify(run_termux_command("termux-battery-status"))

@app.route('/location')
def location():
    # Use -p last to get the last known location quickly
    return jsonify(run_termux_command("termux-location -p last"))

@app.route('/accelerometer')
def accelerometer():
    # We take 1 sample now that we've confirmed the sensor is responsive.
    data = run_termux_command("termux-sensor -n 1 -s Accelerometer")
    try:
        # The key name can vary (e.g., "LSM6DSOTR Accelerometer")
        # We search for the first key that contains "Accelerometer"
        accel_key = next((k for k in data.keys() if "Accelerometer" in k), None)
        
        if not accel_key:
             return jsonify({"error": "Accelerometer not found in data", "raw": data})
        
        accel_data = data[accel_key]
        
        # Some versions return a list, some a dict
        if isinstance(accel_data, list):
            accel_data = accel_data[0]
            
        return jsonify({
            "x": accel_data.get("values", [0,0,0])[0],
            "y": accel_data.get("values", [0,0,0])[1],
            "z": accel_data.get("values", [0,0,0])[2],
            "sensor_name": accel_key
        })
    except Exception as e:
        return jsonify({"error": "Parsing failed", "details": str(e), "raw": data})

@app.route('/snapshot')
def snapshot():
    """Takes a photo and returns the image."""
    try:
        # -c 0 uses the main back camera
        if os.path.exists(SNAPSHOT_PATH):
            os.remove(SNAPSHOT_PATH)
            
        subprocess.run(f"termux-camera-photo -c 0 {SNAPSHOT_PATH}", shell=True, check=True)
        return send_file(SNAPSHOT_PATH, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({"error": "Camera failed", "details": str(e)})

@app.route('/torch/<state>')
def torch(state):
    """Turns the flashlight on or off."""
    mode = "on" if state.lower() == "on" else "off"
    subprocess.run(f"termux-torch {mode}", shell=True)
    return jsonify({"torch": mode})

# Device Identity (Change this to whatever you want your Cyberdeck to be named)
DEVICE_NAME = "Galaxy Cyberdeck Alpha (S16)"

...

@app.route('/info')
def info():
    # We now return a static string. 
    # This prevents the server from 'poking' the Android system 
    # and triggering unwanted sync popups.
    return jsonify({
        "model": DEVICE_NAME,
        "android_version": "16"
    })

if __name__ == '__main__':
    # Listen on all interfaces so the laptop can connect
    app.run(host='0.0.0.0', port=5000)
