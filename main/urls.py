from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('admins/data/', views.viewData, name='admins'),
    path('relations/question/', views.question, name='administration_question'),
    path('relations/nutrition/', views.nutrition, name='nutrition'),
]