from django.db import models
from datetime import datetime
import pytz

moscow_time = pytz.timezone('Europe/Moscow')

class Temperature(models.Model):
    datetime = models.DateTimeField(null=False)
    place = models.CharField(max_length=50, null=False)
    temperature = models.FloatField(null=False)

    def __str__(self):
        return f"{self.datetime.strftime('%H:%M')} - {self.temperature}°C"

    class Meta:
        ordering = ['-datetime']
        verbose_name = "Температура"
        verbose_name_plural = "Температура"


class Humidity(models.Model):
    datetime = models.DateTimeField(null=False)
    place = models.CharField(max_length=50, null=False)
    humidity = models.FloatField(null=False)

    def __str__(self):
        return f"{self.datetime.strftime('%H:%M')} - {self.humidity}"

    class Meta:
        ordering = ['-datetime']
        verbose_name = "Влажность"
        verbose_name_plural = "Влажность"


class Noice(models.Model):
    datetime = models.DateTimeField(null=False)
    place = models.CharField(max_length=50, null=False)
    noice = models.FloatField(null=False)

    def __str__(self):
        return f"{self.datetime.strftime('%H:%M')} - {self.noice}Дц"

    class Meta:
        ordering = ['-datetime']
        verbose_name = "Уровень шума"
        verbose_name_plural = "Уровень шума"


class PeopleData(models.Model):
    datetime = models.DateTimeField(null=False)
    place = models.CharField(max_length=50, null=False)
    people_count = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.datetime.strftime('%H:%M')} - {self.people_count}чел."

    class Meta:
        ordering = ['-datetime']
        verbose_name = "Кол-во людей"
        verbose_name_plural = "Кол-во людей"
