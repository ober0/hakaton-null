from datetime import timezone, timedelta
import matplotlib.pyplot as plt
import numpy as np
import io
import urllib
from datetime import timedelta

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from api.models import PeopleData
from django.utils import timezone

def home(request):
    return redirect('administration_question')

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def viewData(request):
    if request.method == 'GET':
        place = request.GET.get('place')
        if not place:
            place = 'floor4'
        now = timezone.now()

        # Фильтруем данные за последний час
        one_hour_ago = now - timedelta(hours=1)
        people_data_hour = PeopleData.objects.filter(place=place, datetime__gte=one_hour_ago).order_by('datetime')
        print(people_data_hour)
        # Фильтруем данные за последний день
        one_day_ago = now - timedelta(days=1)
        people_data_day = PeopleData.objects.filter(place=place, datetime__gte=one_day_ago).order_by('datetime')
        print(people_data_day)
        # Для последнего часа
        times_hour = [entry.datetime for entry in people_data_hour]
        people_counts_hour = [entry.people_count for entry in people_data_hour]

        # Для последнего дня
        times_day = [entry.datetime for entry in people_data_day]
        people_counts_day = [entry.people_count for entry in people_data_day]

        # Интерполяция данных до 10-секундных шагов (если необходимо)
        def interpolate_data(times, counts, step_seconds=10):
            # Преобразуем время в секунды для интерполяции
            start_time = min(times)
            times_in_seconds = [(time - start_time).total_seconds() for time in times]

            # Интерполяция значений
            time_step = step_seconds
            interpolated_times = np.arange(times_in_seconds[0], times_in_seconds[-1], time_step)
            interpolated_counts = np.interp(interpolated_times, times_in_seconds, counts)

            return interpolated_times, interpolated_counts

        # Интерполируем данные для графиков (по 10 секунд)
        interpolated_times_hour, interpolated_counts_hour = interpolate_data(times_hour, people_counts_hour)
        interpolated_times_day, interpolated_counts_day = interpolate_data(times_day, people_counts_day)

        # Строим график за последний час
        fig, ax = plt.subplots(2, 1, figsize=(10, 12))

        # График за последний час
        ax[0].plot(interpolated_times_hour, interpolated_counts_hour, marker='o', linestyle='-', color='b',
                   label='People Count (Last Hour)')
        ax[0].set(xlabel='Time (seconds)', ylabel='People Count', title=f'People Count in the Last Hour ({place})')
        ax[0].legend()

        # График за последний день
        ax[1].plot(interpolated_times_day, interpolated_counts_day, marker='o', linestyle='-', color='r',
                   label='People Count (Last Day)')
        ax[1].set(xlabel='Time (seconds)', ylabel='People Count', title=f'People Count in the Last Day ({place})')
        ax[1].legend()

        # Сохранение графика в памяти (в формате PNG)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Преобразуем изображение в base64 строку, чтобы использовать его в шаблоне
        image_data = urllib.parse.quote(buf.read())
        buf.close()

        # Передаем данные в шаблон
        context = {
            'image_data': image_data,
        }

        return render(request, 'main/index.html', context)

def question(request):
    return render(request, 'main/question.html')

def nutrition(request):
    return render(request, 'main/nutrition.html')
