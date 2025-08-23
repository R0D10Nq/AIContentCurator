# Многоэтапная сборка для оптимизации размера образа

# Этап 1: Сборка фронтенда
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Копируем package.json и устанавливаем зависимости
COPY frontend/package*.json ./
RUN npm ci --only=production

# Копируем исходники и собираем проект
COPY frontend/ ./
RUN npm run build

# Этап 2: Основной образ с Python
FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Создаем пользователя для безопасности
RUN useradd --create-home --shell /bin/bash app

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements и устанавливаем Python зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY backend/ ./backend/
COPY telegram_bot/ ./telegram_bot/
COPY .env.example .env

# Копируем собранный фронтенд
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Создаем директорию для базы данных
RUN mkdir -p /app/data && chown app:app /app/data

# Переключаемся на непривилегированного пользователя
USER app

# Открываем порт
EXPOSE 8000

# Переменные окружения
ENV PYTHONPATH=/app
ENV DATABASE_URL=sqlite:///./data/ai_content_curator.db

# Команда запуска
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
