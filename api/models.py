from django.db import models
import pytz
from datetime import datetime


# Указываем Московскую временную зону
moscow_time = pytz.timezone('Europe/Moscow')

class Temperature(models.Model):
    datetime = models.DateTimeField(null=False)
    place = models.CharField(max_length=50, null=False)
    temperature = models.FloatField(null=False)

    def __str__(self):
        # Конвертируем время в Московское перед выводом
        moscow_datetime = self.datetime.astimezone(moscow_time)
        return f"{moscow_datetime.strftime('%H:%M')} - {self.temperature}°C"

    class Meta:
        ordering = ['-datetime']
        verbose_name = "Температура"
        verbose_name_plural = "Температура"


class Humidity(models.Model):
    datetime = models.DateTimeField(null=False)
    place = models.CharField(max_length=50, null=False)
    humidity = models.FloatField(null=False)

    def __str__(self):
        moscow_datetime = self.datetime.astimezone(moscow_time)
        return f"{moscow_datetime.strftime('%H:%M')} - {self.humidity}"

    class Meta:
        ordering = ['-datetime']
        verbose_name = "Влажность"
        verbose_name_plural = "Влажность"


class Noice(models.Model):
    datetime = models.DateTimeField(null=False)
    place = models.CharField(max_length=50, null=False)
    noice = models.FloatField(null=False)

    def __str__(self):
        moscow_datetime = self.datetime.astimezone(moscow_time)
        return f"{moscow_datetime.strftime('%H:%M')} - {self.noice}Дц"

    class Meta:
        ordering = ['-datetime']
        verbose_name = "Уровень шума"
        verbose_name_plural = "Уровень шума"


class PeopleData(models.Model):
    datetime = models.DateTimeField(null=False, default=datetime.now(moscow_time))
    place = models.CharField(max_length=50, null=False)
    people_count = models.IntegerField(null=False)

    def __str__(self):
        moscow_datetime = self.datetime.astimezone(moscow_time)
        return f"{moscow_datetime.strftime('%H:%M')} - {self.people_count}чел."

    class Meta:
        ordering = ['-datetime']
        verbose_name = "Кол-во людей"
        verbose_name_plural = "Кол-во людей"
