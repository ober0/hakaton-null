import time

from django.test import TestCase
import requests

url = 'http://192.168.137.52:8000/api/data/set/temperature/'


request = requests.post(url=url, data={
    'place': 'floor4',
    'temperature': 20
})
response = request.json()
print(response)