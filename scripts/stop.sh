#!/bin/bash

# Скрипт остановки AI Content Curator

echo "🛑 Остановка AI Content Curator..."

# Останавливаем все сервисы
docker-compose down

echo "🧹 Очистка неиспользуемых ресурсов..."
docker system prune -f

echo "✅ AI Content Curator остановлен!"
