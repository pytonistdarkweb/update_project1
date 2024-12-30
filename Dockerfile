FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка poetry
RUN pip install --no-cache-dir poetry

# Копирование только файлов зависимостей
COPY pyproject.toml poetry.lock ./

# Отключение создания виртуального окружения
RUN poetry config virtualenvs.create false

# Установка зависимостей проекта
RUN poetry install --no-dev --no-interaction --no-ansi

# Копирование кода приложения
COPY . .

# Команда запуска
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]