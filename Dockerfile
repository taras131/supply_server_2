# Используем базовый образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

COPY certificate.key /ssl/
COPY certificate_ca /ssl/
COPY certificate /ssl/
# Устанавливаем системные инструменты
RUN apt-get update && apt-get install -y build-essential

# Устанавливаем Poetry
RUN pip install "poetry>=1.6.1"

# Копируем только файлы Poetry для этапа установки зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false && poetry install --no-root --only main

# Копируем проект
COPY . .

# Указываем порт приложения
EXPOSE 443

# Указываем команду запуска
# Замените существующий CMD на:
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "/app/ssl/certificate.key", "--ssl-certfile", "/app/ssl/certificate"]
