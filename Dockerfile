# Используем официальный slim-образ Python 3.12
FROM python:3.12-slim
# Устанавливаем рабочую директорию в контейнере
WORKDIR /app
# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
ENV POETRY_VERSION=2.2.1
ENV POETRY_REQUESTS_TIMEOUT=120
# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version 2.2.1 \
&& ln -s /root/.local/bin/poetry /usr/local/bin/poetry
COPY pyproject.toml poetry.lock ./
# Устанавливаем зависимости Python с помощью Poetry
RUN poetry config virtualenvs.create false \
&& poetry install --no-root
# Копируем исходный код приложения в контейнер
COPY . .
# Создаем директорию для медиафайлов
RUN mkdir -p /app/media
# Пробрасываем порт, который будет использовать Django
EXPOSE 8000
# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
