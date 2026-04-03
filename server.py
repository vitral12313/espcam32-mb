from flask import Flask, render_template, request
from flask_socketio import SocketIO
import base64

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    data = request.data
    frame_b64 = base64.b64encode(data).decode('utf-8')
    socketio.emit('frame', frame_b64)
    return 'ok'

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
