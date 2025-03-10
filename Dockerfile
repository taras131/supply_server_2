# Используем базовый образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

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
EXPOSE 8000

# Указываем команду запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]