from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask import request
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# ESP32 отправляет кадр сюда
@app.route('/upload', methods=['POST'])
def upload_frame():
    data = request.data
    # конвертируем в base64
    frame_b64 = base64.b64encode(data).decode('utf-8')
    # отправляем всем подключенным клиентам
    socketio.emit('frame', frame_b64)
    return 'ok'

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
