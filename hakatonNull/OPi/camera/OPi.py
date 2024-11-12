import cv2
import time
import requests
from io import BytesIO
import random
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URL для отправки данных
url_temperature = "http://192.168.137.52:8000/api/data/set/temperature/"
url_humidity = "http://192.168.137.52:8000/api/data/set/humidity/"
url_noise = "http://192.168.137.52:8000/api/data/set/noice/"
url_people_data = "http://192.168.137.52:8000/api/data/set/peopleData/"
place_name = 'floor4'

# Интервалы отправки данных
capture_interval = 5  # Интервал захвата изображения в секундах

def send_data(url, data, files=None):
    """Функция для отправки данных на сервер."""
    try:
        response = requests.post(url, data=data, files=files)
        if response.status_code == 200:
            logging.info(f"Данные успешно отправлены на {url}.")
        else:
            logging.error(f"Ошибка: Не удалось отправить данные на {url} - Статус код {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка запроса к {url}: {e}")

    print(response.json())
# Главный цикл для отправки данных
start_time_img = time.time()
start_time_sensors = time.time()

while True:
    # Симуляция данных от сенсоров
    temperature = round(random.uniform(20.0, 30.0), 1)
    humidity = round(random.uniform(30.0, 70.0), 1)
    noice = round(random.uniform(40.0, 80.0), 1)

    # Формируем JSON данные для каждого датчика и отправляем
    data_temperature = {'place': place_name, 'temperature': temperature}
    send_data(url_temperature, data_temperature)

    data_humidity = {'place': place_name, 'humidity': humidity}
    send_data(url_humidity, data_humidity)

    data_noise = {'place': place_name, 'noice': noice}
    send_data(url_noise, data_noise)

    # Открытие изображения и отправка его
    with open('photo_2024-11-12_14-08-11.jpg', 'rb') as f:
        files = {'file': f}
        data_img = {'place': place_name}
        send_data(url_people_data, data_img, files=files)


    # Задержка между кадрами
    time.sleep(capture_interval)
