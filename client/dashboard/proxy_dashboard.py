from flask import Flask, send_from_directory, jsonify
import requests
import os
import sys

# Stap 1: Centralisatie - Importeer de centrale configuratie
# We voegen de project root toe aan het pad om config.py te vinden
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
try:
    import config
    NODE_URL = f'http://{config.PHONE_IP}:{config.PHONE_PORT}'
except ImportError:
    NODE_URL = 'http://10.116.60.186:5000' # Fallback

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/<path:endpoint>')
def proxy_api(endpoint):
    # Stap 2: Snapshot Stabiliteit - Verhoog timeout voor foto's (5s vs 2s)
    current_timeout = 5 if 'snapshot' in endpoint else 2
    
    try:
        # De Pi fungeert als bridge: haal data op van de telefoon via USB
        resp = requests.get(f'{NODE_URL}/{endpoint}', timeout=current_timeout)
        
        # Voor afbeeldingen (zoals /snapshot) sturen we de ruwe data door
        if 'snapshot' in endpoint:
            from flask import Response
            return Response(resp.content, mimetype='image/jpeg')
            
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Luister op LAN poort 8080
    app.run(host='0.0.0.0', port=8080)
