import json
from .models import Temperature, Noice, Humidity
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def setTemperature(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            temperature = data['temperature']
            place = data['place']
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

        try:
            temperature = Temperature(place=place, temperature=temperature)
            temperature.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })


def setHumidity(request):
    pass


def setNoice(request):
    pass


def setPeopleData(request):
    pass