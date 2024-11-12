import requests

url_temperature = "http://192.168.137.52:8000/api/data/set/peopleData/"

with open('photo_2024-11-12_14-08-11.jpg', 'rb') as f:
    request = requests.post(url_temperature, data={'place': 'floor4'}, files={'file': f})

print(request.status_code)
if request.status_code == 200:
    response = request.json()
    print(response)
