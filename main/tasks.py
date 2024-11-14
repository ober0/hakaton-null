from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings
from .models import Question
@shared_task
def send_email(email, text, header):
    subject = header
    message = text
    from_email = settings.DEFAULT_FROM_EMAIL  # Берется из настроек
    recipient_list = [email]  # Адреса получателей

    try:
        send_mail(subject, message, from_email, recipient_list)

    except:
        return {'success': False}