import cv2
import time
import requests
import json
from io import BytesIO

# Настройки для видеопотока
capture_interval = 5  # Интервал между кадрами в секундах
url = "http://127.0.0.1:8000/api/data/set/peopleData/"
place_name = "floor4"  # Название места, передается в JSON

# Инициализация камеры
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Frame capture failed.")
        break

    # Сохранение кадра в памяти как изображение JPEG
    _, img_encoded = cv2.imencode('.jpg', frame)
    img_bytes = BytesIO(img_encoded)

    # Формирование данных для отправки
    files = {'file': ('frame.jpg', img_bytes, 'image/jpeg')}
    data = {'place': place_name}

    try:
        # Отправка данных на сервер
        response = requests.post(url, data=data, files=files)
        if response.status_code == 200:
            print("Frame sent successfully.")
        else:
            print(f"Error: Failed to send frame - Status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

    # Задержка перед следующим кадром
    time.sleep(capture_interval)

# Освобождение камеры
cap.release()
