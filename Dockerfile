# Базовый образ Python
FROM python:3.11-slim as builder

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
ENV POETRY_VERSION=1.7.1
RUN pip install "poetry==$POETRY_VERSION"

# Создаем и переходим в рабочую директорию
WORKDIR .

# Копируем только файлы зависимостей сначала
COPY pyproject.toml poetry.lock* /./

# Копируем остальные файлы проекта
COPY . /

# Финальный образ
FROM python:3.11-slim

# Установка runtime зависимостей
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Копируем установленные зависимости
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /. /.

# Настройки окружения
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=hammer_sys.settings

WORKDIR .

# Команда для запуска
CMD ["gunicorn", "hammer_sys.wsgi:application", "--bind", "0.0.0.0:8000"]