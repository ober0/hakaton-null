import json
import os

import cv2

from .models import Temperature, Noice, Humidity, PeopleData
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .tasks import count_people
from django.conf import settings


@csrf_exempt
def setTemperature(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            temperature_val = data['temperature']
            place = data['place']
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

        try:
            temperature = Temperature(place=place, temperature=temperature_val)
            temperature.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

@csrf_exempt
def setHumidity(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            humidity_val = data['humidity']
            place = data['place']
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

        try:
            humidity = Humidity(place=place, humidity=humidity_val)
            humidity.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

@csrf_exempt
def setNoice(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            place = data['place']
            noice_val = data['noice']
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

        try:
            noice = Temperature(place=place, noice=noice_val)
            noice.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })


@csrf_exempt
def setPeopleData(request):
    if request.method == 'POST':
        try:
            # Получаем данные формы
            place = request.POST.get('place')
            file = request.FILES.get('file')

            if file:
                # yolov3_weights = 'yolov3.weights'
                # yolov3_cfg = 'yolov3.cfg'
                # yolo_net = cv2.dnn.readNet(yolov3_weights, yolov3_cfg)
                count_people.delay(place, file.name, file.read())  # передаем имя файла и содержимое

                return JsonResponse({'success': True})

            else:
                return JsonResponse({'success': False, 'error': 'No file uploaded'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})
