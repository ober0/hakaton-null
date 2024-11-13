import base64
import matplotlib
import pytz
from django.http import JsonResponse
from .models import Question
matplotlib.use('Agg')
from datetime import timezone, timedelta
import matplotlib.pyplot as plt
import numpy as np
import io
import matplotlib.dates as mdates
from datetime import timedelta
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from api.models import PeopleData, Humidity, Temperature
from django.utils import timezone
from django.conf import settings
import requests

def home(request):
    return redirect('administration_question')


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def viewData(request):
    if request.method == 'GET':
        place = request.GET.get('place')
        if not place:
            place = 'floor4'
        now = timezone.now()

        url = settings.ADRESS + 'api/model/' + place + '/'

        my_request = requests.post(url)
        if my_request.status_code == 200:
            response = my_request.json()
            task_id = response['task_id']
        else:
            return JsonResponse({'error': 'prediction failed'})
        # Фильтруем данные за последний час
        one_hour_ago = now - timedelta(hours=1)
        people_data_hour = PeopleData.objects.filter(place=place, datetime__gte=one_hour_ago).order_by('datetime')

        # Фильтруем данные за последний день
        one_day_ago = now - timedelta(days=1)
        people_data_day = PeopleData.objects.filter(place=place, datetime__gte=one_day_ago).order_by('datetime')

        # Для последнего часа
        times_hour = [entry.datetime for entry in people_data_hour]
        people_counts_hour = [entry.people_count for entry in people_data_hour]

        # Для последнего дня
        times_day = [entry.datetime for entry in people_data_day]
        people_counts_day = [entry.people_count for entry in people_data_day]

        # Проверка на пустые данные
        if not times_hour and not times_day:
            # Если нет данных, строим пустой график
            fig, ax = plt.subplots(2, 1, figsize=(10, 12))

            # Графики без данных
            ax[0].plot([], [], marker='o', linestyle='-', color='b', label='Нет данных (час)')
            ax[1].plot([], [], marker='o', linestyle='-', color='r', label='Нет данных (сутки)')

            ax[0].set(xlabel='Время (часы:минуты)', ylabel='Число людей', title=f'Количество людей за час в ({place})')
            ax[1].set(xlabel='Время (часы:минуты)', ylabel='Число людей', title=f'Количетво людей за сутки в ({place})')

            ax[0].legend()
            ax[1].legend()

        else:
            # Интерполяция данных до 1-минутных шагов (если необходимо)
            def interpolate_data(times, counts, step_seconds=60):
                # Преобразуем время в секунды для интерполяции
                start_time = min(times)
                times_in_seconds = [(time - start_time).total_seconds() for time in times]

                # Интерполяция значений
                time_step = step_seconds
                interpolated_times = np.arange(times_in_seconds[0], times_in_seconds[-1], time_step)
                interpolated_counts = np.interp(interpolated_times, times_in_seconds, counts)

                # Приводим к целым числам
                interpolated_counts = np.round(interpolated_counts).astype(int)

                return interpolated_times, interpolated_counts

            # Интерполируем данные для графиков (по 1 минуте)
            interpolated_times_hour, interpolated_counts_hour = interpolate_data(times_hour, people_counts_hour,
                                                                                 step_seconds=60)
            interpolated_times_day, interpolated_counts_day = interpolate_data(times_day, people_counts_day,
                                                                               step_seconds=60)

            # Преобразуем данные времени в datetime объекты для правильного отображения
            time_dt_hour = [min(times_hour) + timedelta(seconds=t) for t in interpolated_times_hour]
            time_dt_day = [min(times_day) + timedelta(seconds=t) for t in interpolated_times_day]

            # Строим график за последний час
            fig, ax = plt.subplots(2, 1, figsize=(10, 12))

            # График за последний час
            ax[0].plot(time_dt_hour, interpolated_counts_hour, marker='o', linestyle='-', color='b',
                       label='График кол-ва людей (час)')
            ax[0].set(xlabel='Время (часы:минуты)', ylabel='Число людей', title=f'Количество людей за час в ({place})')
            ax[0].legend()

            # График за последний день
            ax[1].plot(time_dt_day, interpolated_counts_day, marker='o', linestyle='-', color='r',
                       label='График кол-ва людей (сутки)')
            ax[1].set(xlabel='Время (часы:минуты)', ylabel='Число людей', title=f'Количетво людей за сутки в ({place})')
            ax[1].legend()

            # Настроим формат времени на оси X в московском часовом поясе
            msk_tz = pytz.timezone('Europe/Moscow')

            # Для графика за час
            ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            step_hour = max(1, int(len(time_dt_hour) / 6))
            ax[0].set_xticks(time_dt_hour[::step_hour])
            ax[0].set_xticklabels(
                [time.astimezone(msk_tz).strftime('%H:%M') for time in time_dt_hour[::step_hour]],
                rotation=45)

            # Для графика за сутки
            ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            step_day = max(1, int(len(time_dt_day) / 6))  # calculate step for day data
            ax[1].set_xticks(time_dt_day[::step_day])
            ax[1].set_xticklabels(
                [time.astimezone(msk_tz).strftime('%H:%M') for time in time_dt_day[::step_day]],
                rotation=45)

        # Сохранение графика в памяти (в формате PNG)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Преобразуем изображение в base64 строку
        image_data = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        people = PeopleData.objects.filter(place=place).latest('datetime')
        humidity = Humidity.objects.filter(place=place).latest('datetime')
        temperature = Temperature.objects.filter(place=place).latest('datetime')
        # Передаем данные в шаблон
        context = {
            'image_data': image_data,
            'task_id': task_id,
            'people_count':people,
            'humidity':humidity,
            'temperature': temperature
        }


        return render(request, 'main/index.html', context)

def question(request):
    if request.method == 'GET':
        return render(request, 'main/question.html')
    else:
        data = request.POST

        name = data['name']
        email = data['email']
        subject = data['rating']
        message = data['message']

        try:
            question = Question(name=name, email=email, subject=subject, message=message)
            question.save()
        except:
            pass

        return redirect('/')
def nutrition(request):
    if request.method == 'GET':
        return render(request, 'main/nutrition.html')
    else:
        return JsonResponse({})