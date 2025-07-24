import os
from twilio.rest import Client
from django.core.mail import send_mail
from dotenv import load_dotenv


load_dotenv()

"""Twill можно использовать для отпрваки кода через SMS"""
# def send_sms_via_service(phone_number, message):
#     account_sid = os.getenv("AC_SID")
#     auth_token = os.getenv("AUTH_TOKEN")
#     twilio_number = os.getenv("TWILL_NUM")
#
#     client = Client(account_sid, auth_token)
#
#     client.messages.create(
#         body=message,
#         from_=twilio_number,
#         to=phone_number
#     )



"""Отправка кода подверждение в email"""
def send_email(email, code):
    send_mail(
        'Код подтверждения',
        f'Ваш код: {code}',
        'noreply@example.com',
        [email],
        fail_silently=False,
    )