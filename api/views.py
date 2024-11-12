import json
import os
from datetime import datetime
import cv2
import pytz

from .models import Temperature, Noice, Humidity
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .tasks import count_people
from django.conf import settings


@csrf_exempt
def setTemperature(request):
    if request.method == 'POST':
        try:
            temperature_val = request.POST.get('temperature')
            place = request.POST.get('place')
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

        try:
            temperature = Temperature(place=place, temperature=temperature_val, datetime=datetime.now(pytz.timezone('Europe/Moscow')))
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
            humidity_val = request.POST.get('humidity')
            place = request.POST.get('place')
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

        try:
            humidity = Humidity(place=place, humidity=humidity_val, datetime=datetime.now(pytz.timezone('Europe/Moscow')))
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
            place = request.POST.get('place')
            noice_val = request.POST.get('noice')
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

        try:
            noice = Noice(place=place, noice=noice_val, datetime=datetime.now(pytz.timezone('Europe/Moscow')))
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
