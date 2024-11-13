from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('data/set/temperature/', views.setTemperature, name='setTemperature'),
    path('data/set/humidity/', views.setHumidity, name='setWetness'),
    path('data/set/noice/', views.setNoice, name='setNoice'),
    path('data/set/peopleData/', views.setPeopleData, name='setPeopleData'),
    path('model/<str:place>/', views.model, name='model'),
    path('result/get/model/<str:taskIdd>', views.resultPredict)
]



