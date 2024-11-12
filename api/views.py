import json
from .models import Temperature, Noice, Humidity, PeopleData
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


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


def setPeopleData(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            place = data['place']
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
