from django.contrib import admin
from .models import Temperature, Humidity, Noice, PeopleData

class TemperatureAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'place', 'temperature')
    search_fields = ('datetime', 'place', 'temperature')

admin.site.register(Temperature, TemperatureAdmin)


class HumidityAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'place', 'humidity')
    search_fields = ('datetime', 'place', 'humidity')

admin.site.register(Humidity, HumidityAdmin)


class NoiceAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'place', 'noice')
    search_fields = ('datetime', 'place', 'noice')

admin.site.register(Noice, NoiceAdmin)


class PeopleDataAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'place', 'people_count')
    search_fields = ('datetime', 'place', 'people_count')

admin.site.register(PeopleData, PeopleDataAdmin)