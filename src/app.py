# '/api/v1/details'
# '/api/v1/healthz'

from flask import Flask, jsonify
import datetime, socket

app = Flask(__name__)

@app.route('/api/v1/details')
def details():
    return jsonify({
        'hostname': socket.gethostname(),
        'timestamp': datetime.datetime.now(),
        'message': 'Hello! from Ashif app running and Docker and kates'
        })

@app.route('/api/v1/healthz')
def healthz():
    return jsonify({'status': 'Healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')