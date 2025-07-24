# views.py
import logging
import secrets
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.db.models import Q
from .models import User
from hammer_sys.settings import EMAIL_HOST_USER

logger = logging.getLogger(__name__)


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.send_activation_email()

        verification_code = self.generate_verification_code()
        user.verification_code = verification_code
        user.code_expires = timezone.now() + timedelta(hours=24)
        user.save()

        self.send_verification(user, verification_code)

    def generate_verification_code(self):
        """Генерация 6-значного кода"""
        return ''.join([str(secrets.randbelow(10)) for _ in range(6)])

    def send_verification(self, user, code):
        """Отправка кода верификации"""
        if user.email:
            self.send_verification_email(user, code)
        if user.number:
            self.send_verification_sms(user, code)

    def send_verification_email(self, user, code):
        """Отправка кода по email"""
        logger.info(f"Код подтверждения для {user.email}: {code}")
        print(f"Код подтверждения (для теста): {code}")
        subject = 'Код подтверждения регистрации'
        html_message = render_to_string(r'hammer_sys\app\templates\activation_email.html', {
            'user': user,
            'code': code
        })
        plain_message = strip_tags(html_message)

        try:
            send_mail(
                subject,
                plain_message,
                EMAIL_HOST_USER,
                [user.email],
                html_message=html_message,
                fail_silently=False,
            )

            logger.info(f"Verification email sent to {user.email}")
        except Exception as e:
            logger.error(f"Failed to send verification email to {user.email}: {str(e)}")

    def send_verification_sms(self, user, code):
        """Заглушка для SMS-верификации"""
        logger.info(f"SMS verification code for {user.number}: {code}")


class VerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        number = request.data.get("number")
        code = request.data.get("code")

        if not code:
            return Response(
                {"status": "error", "message": "Код подтверждения обязателен"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not email and not number:
            return Response(
                {"status": "error", "message": "Укажите email или номер телефона"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(
                Q(email=email) | Q(number=number),
                verification_code=code,
                code_expires__gte=timezone.now()
            )
            user.is_verified = True
            user.verification_code = ''
            user.save()

            return Response(
                {"status": "success", "message": "Аккаунт подтвержден!"},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"status": "error", "message": "Неверный код или истек срок действия"},
                status=status.HTTP_400_BAD_REQUEST
            )


class ActivationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)

            if user.code_expires < timezone.now():
                return Response(
                    {"status": "error", "message": "Срок действия кода истёк"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if user.is_active:
                return Response(
                    {"status": "info", "message": "Аккаунт уже активирован"},
                    status=status.HTTP_200_OK
                )

            user.is_active = True
            user.activation_code = None
            user.save()

            return Response(
                {
                    "status": "success",
                    "message": "Аккаунт успешно активирован!",
                    "email": user.email
                },
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {"status": "error", "message": "Неверный код активации"},
                status=status.HTTP_400_BAD_REQUEST
            )
