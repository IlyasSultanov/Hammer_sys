# models.py
import secrets
import uuid

from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.loader import render_to_string
from django.utils import timezone

from django.conf import settings

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    verification_code = models.CharField(max_length=6, blank=True)
    code_expires = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=64, blank=True)

    def generate_activation_code(self):
        """Генерация 6-значного кода"""
        code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
        self.activation_code = code
        self.code_expires = timezone.now() + timezone.timedelta(hours=24)
        self.save()
        return code

    def send_activation_email(self):
        """Отправка кода на email"""
        code = self.generate_activation_code()
        subject = 'Ваш код активации'
        message = f'Ваш код для активации: {code}'
        html_message = render_to_string('activation_email.html', {
            'code': code,
            'email': self.email
        })

        """Отправка кода в email для активаций"""
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            html_message=html_message,
            fail_silently=False,
        )

    def __str__(self):
        return f"{self.email or self.number} - {self.username}"