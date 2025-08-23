#!/bin/bash

# Скрипт запуска AI Content Curator

echo "🚀 Запуск AI Content Curator..."

# Проверяем наличие .env файла
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден. Копирую из .env.example..."
    cp .env.example .env
    echo "📝 Отредактируйте файл .env с вашими настройками"
fi

# Проверяем Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Установите Docker для продолжения."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Установите Docker Compose для продолжения."
    exit 1
fi

# Загружаем переменные окружения
source .env

# Проверяем обязательные переменные
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ GEMINI_API_KEY не установлен в .env файле"
    exit 1
fi

echo "🔧 Сборка и запуск контейнеров..."

# Собираем и запускаем основное приложение
docker-compose up --build -d app

echo "⏳ Ожидание запуска приложения..."
sleep 10

# Проверяем статус
if docker-compose ps | grep -q "Up"; then
    echo "✅ Приложение успешно запущено!"
    echo "🌐 Веб-интерфейс: http://localhost:8000"
    echo "📚 API документация: http://localhost:8000/docs"
    echo "❤️  Health check: http://localhost:8000/health"
    
    # Запускаем Telegram бота если токен установлен
    if [ ! -z "$TELEGRAM_BOT_TOKEN" ]; then
        echo "🤖 Запуск Telegram бота..."
        docker-compose --profile bot-polling up -d telegram-bot
        echo "✅ Telegram бот запущен!"
    else
        echo "⚠️  TELEGRAM_BOT_TOKEN не установлен. Telegram бот не запущен."
    fi
else
    echo "❌ Ошибка при запуске приложения"
    docker-compose logs app
    exit 1
fi

echo "🎉 AI Content Curator готов к работе!"
