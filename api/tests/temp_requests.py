import time

from django.test import TestCase
import requests

url = 'http://127.0.0.1:8000/api/data/set/temperature/'

for i in range(1000):
    request = requests.post(url=url, json={
        'place': 'floor4',
        'temperature': 20
    })
    time.sleep(0.2)
    response = request.json()
    print(response)