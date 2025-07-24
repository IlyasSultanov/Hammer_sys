# Hammer Sys - Система аутентификации

Проект реализует регистрацию и верификацию пользователей через email или SMS.

## 📌 Функционал

- Регистрация новых пользователей
- Отправка кода подтверждения на email/SMS
- Верификация аккаунта

## 🛠 Технологии

- Python 3.11
- Django 5.0
- Django REST Framework
- SMTP (Gmail) / SMS-сервис

## ⚙️ Установка

1. Клонировать репозиторий:
```bash
https://github.com/IlyasSultanov/Hammer_sys.git
cd hammer-sys

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install poetry 
poetry install

python manage.py migrate

python manage.py runserver

📡 API Endpoints
Регистрация
POST register/

json
{
    "email": "user@example.com",
    "password": "securepassword123",
    "phone": "+79161234567"  
}

Верификация
POST verify/

json
{
    "phone": "+79161234567",
    "code": "123456"
}

🔐 Настройки SMTP
В settings.py:

python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ваш@gmail.com'
EMAIL_HOST_PASSWORD = 'пароль-приложений'  # 16-значный

🚀 Развертывание
Production-сервер:

bash
gunicorn hammer_sys.wsgi:application

Для Nginx добавьте:

nginx
location / {
    proxy_pass http://localhost:8000;
    proxy_set_header Host $host;
}
📄 Лицензия
MIT License

👨‍💻 Разработчик
[Ильяс] - [SultanovIlyas0@gmail.com]
```

# Данные для .env
# PostgreSQL
POSTGRES_DB=test_db
POSTGRES_USER=test_user
POSTGRES_PASSWORD=test_pw
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Redis
REDIS_PASSWORD=2066

# TWILL если отправка по смс
AC_SID=...
AUTH_TOKEN=...
TWILL_NUM=...

Если отпрвака по email
EMAIL_HOST=smtp.gmail.com 
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
DEFAULT_FROM_EMAIL=...
