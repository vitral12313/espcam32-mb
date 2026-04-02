from flask import Flask, request, send_file, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Папка для хранения изображений
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

LAST_IMAGE = os.path.join(UPLOAD_FOLDER, "last.jpg")


# 🔼 Загрузка изображения с ESP32
@app.route("/upload", methods=["POST"])
def upload():
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "No image field"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"status": "error", "message": "Empty filename"}), 400

    # Сохраняем последнее изображение
    file.save(LAST_IMAGE)

    return jsonify({"status": "ok"})


# 🖼 Получить последнее изображение
@app.route("/image")
def get_image():
    if os.path.exists(LAST_IMAGE):
        return send_file(LAST_IMAGE, mimetype='image/jpeg')
    return "No image yet", 404


# 🌐 Простая веб-страница (автообновление)
@app.route("/")
def index():
    return f"""
    <html>
    <head>
        <title>ESP32-CAM</title>
    </head>
    <body style="text-align:center;">
        <h2>📷 ESP32-CAM Live</h2>
        <img src="/image" width="90%" id="cam">
        
        <script>
            setInterval(() => {{
                document.getElementById("cam").src = "/image?t=" + new Date().getTime();
            }}, 3000);
        </script>
    </body>
    </html>
    """


# ❤️ Проверка сервера (для Render)
@app.route("/health")
def health():
    return "OK", 200


# 🚀 Запуск (для локального теста)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
