from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('admins/data/', views.viewData, name='admins'),
    path('relations/question/', views.question, name='administration_question'),
    path('relations/question/response/', views.questions_response, name='questions_response'),
    path('relations/question/response/<int:id>/', views.question_response, name='question_response'),
    path('relations/question/<int:id>/send-administrator-response/', views.admin_response, name='question_response'),
    path('relations/nutrition/', views.nutrition, name='nutrition'),
]