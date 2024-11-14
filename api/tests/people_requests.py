from datetime import datetime

import pytz
import requests

url = 'http://127.0.0.1:8000/api/data/set/peopleData/'

# Открываем файл для отправки
with open('photo.jpg', 'rb') as f:
    # Подготовка данных для отправки
    files = {'file': f}
    data = {
        'place': 'floor4',
        'time': datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S')
    }

    # Отправляем POST-запрос
    response = requests.post(url, data=data, files=files)

# Проверка ответа
print(response.status_code)
if response.status_code == 200:
    print(response.json())
else:
    print("Ошибка:", response.text)
