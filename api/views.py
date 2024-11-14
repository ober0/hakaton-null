import json
import os
from datetime import datetime
import cv2
import pytz
from celery.result import AsyncResult
from .models import Temperature, Noice, Humidity, PeopleData
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .tasks import count_people, doModel
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
            time = request.POST.get('time')
            if file:
                # Сохраняем файл на диск
                with open("image.jpg", 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)

                # Перемещаем курсор в начало файла для его чтения
                file.seek(0)
                # Передаем имя файла и его содержимое (в виде байтов) в Celery задачу
                count_people.delay(place, file.name, file.read(), time)

                return JsonResponse({'success': True})

            else:
                return JsonResponse({'success': False, 'error': 'No file uploaded'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def model(request, place):
    people_data = PeopleData.objects.filter(place=place).all()
    data = {
        'time': [entry.datetime for entry in people_data],
        'people': [entry.people_count for entry in people_data]
    }
    task = doModel.delay(place, data)
    model_task_id = task.id
    return JsonResponse({'task_id': model_task_id})

@csrf_exempt
def resultPredict(request, taskId):
    result = AsyncResult(taskId)

    status = result.status

    if status == 'SUCCESS':
        data = result.result
        print(data)
    return JsonResponse(data)


def getActualData(request, place):
    if request.method == 'POST':
        try:
            people = PeopleData.objects.filter(place=place).latest('datetime')
            humidity = Humidity.objects.filter(place=place).latest('datetime')
            temperature = Temperature.objects.filter(place=place).latest('datetime')

            context = {
                'success': True,
                'people_count': str(people),
                'humidity': str(humidity),
                'temperature': str(temperature)
            }

            return JsonResponse(context)
        except:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })