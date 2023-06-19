import subprocess
import json
import time
from flask import Flask, request, jsonify
from I2C_Function import analyze_data, read_data
from flask_cors import CORS
from threading import Lock

app = Flask(__name__)
CORS(app)

initialized = False
lock = Lock()  # Sperre (Lock) für die analyze_data-Methode

def create_response(status_code, description):
    return jsonify({
        'status': status_code,
        'description': description
    })

@app.route('/trng/randomNum/init', methods=['GET'])
def initialize_generator():
    global initialized
    
    if initialized:
            return create_response(200, 'System is already initialised, random numbers can be requested')
    
    start_time = time.time()
    with lock:  # Sperre (Lock) verwenden, um sicherzustellen, dass nur ein Thread die Methode ausführt
        result = analyze_data(int(1), int(1), startup=True)
        
    end_time = time.time()    
    duration = end_time - start_time
    
    if duration > 60:
        return create_response(555, 'Unable to initialize the random number generator within a timeout of 60 seconds')
    else:
        if result is True:
            initialized = True
            return create_response(200, 'Successful operation; random number generator is ready and random numbers can be requested')
        if result == 400:
            return create_response(543, 'Tests failed, try again')
        if result is False:
            return create_response(500, 'Unable to generate random numbers. Restart/Reset System')
        else:
            return create_response(555, 'Unable to initialize the random number generator within a timeout of 60 seconds')


@app.route('/trng/randomNum/getRandom', methods=['GET'])
def get_random_numbers():
    global initialized
    quantity = request.args.get('quantity', default=1)
    bits = request.args.get('numBits', default=1)
    
    try:
        quantity = int(quantity)
        bits = int(bits)
    except ValueError:
        return create_response(400, 'Invalid input. Quantity and bits must be numeric')

    if quantity <= 0 or bits <= 0:
        return create_response(400, 'Invalid input. Quantity and bits must be positive integers')
    
    if not initialized:
        return create_response(432, 'System not ready; try init')
    
    with lock:  # Sperre (Lock) verwenden, um sicherzustellen, dass nur ein Thread die Methode ausführt
        random_numbers = analyze_data(quantity, bits, startup=False)    
            
        if random_numbers == 400:
            return create_response(543, 'Tests failed, try again')
        if random_numbers is False:
            return create_response(500, 'Unable to generate random numbers. Restart/Reset System')
        if random_numbers:        
            data = {
                'status': 200,
                'description': 'Successful operation; HEX-encoded bit arrays (with leading zeros if required)',
                'randomNumbers': random_numbers
            }
            return jsonify(data)
        else:
            return create_response(500, 'Unable to generate random numbers.')
    
@app.route('/trng/randomNum/shutdown', methods=['GET'])
def shutdown_generator(): 
    global initialized

    initialized = False

    return create_response(200, "Successful operation; random number generator has been set to 'standby mode'")
    
# Fehlerbehandlungsroutine für nicht übereinstimmende Routen
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def handle_invalid_routes(path):
    return create_response(404, 'Route not found')

if __name__ == '__main__':
    
    # Pfade zu den SSL-Zertifikat- und Schlüsseldateien    
    cert_path = '/etc/nginx/ssl/cert-gmtrom.pem'
    key_path = '/etc/nginx/ssl/cert-gmtrom-key.pem'
    
    #alte Zertifikate self signed
    #cert_path = '/etc/nginx/ssl/server.crt'
    #key_path = '/etc/nginx/ssl/server.key'
    
    # Starte die Flask-Anwendung mit SSL-Konfiguration
    app.run(host='0.0.0.0', ssl_context=(cert_path, key_path))
    #app.run(host='172.16.78.57', port=5000, ssl_context=(cert_path, key_path))    
    #app.run(host='0.0.0.0', ssl_context=adhoc)
    #app.run(ssl_context=(cert_path, key_path))