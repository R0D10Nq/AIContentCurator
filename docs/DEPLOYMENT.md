# 🚀 Руководство по деплою

## Обзор

AI Content Curator поддерживает несколько способов деплоя: от простого запуска в Docker до полноценного продакшен окружения с Nginx и SSL.

## 🐳 Docker Деплой (рекомендуется)

### Быстрый запуск

```bash
# Клонируем репозиторий
git clone <repository-url>
cd ai-content-curator

# Настраиваем переменные окружения
cp .env.example .env
# Отредактируйте .env файл

# Запускаем приложение
docker-compose up --build -d
```

### Продакшен конфигурация

```bash
# Запуск с Nginx и SSL
docker-compose --profile production up --build -d
```

## ⚙️ Конфигурация окружения

### Обязательные переменные

```env
# Google Gemini AI API ключ
GEMINI_API_KEY=your-gemini-api-key-here

# Секретный ключ для JWT (генерируйте случайный)
SECRET_KEY=your-super-secret-key-change-this-in-production
```

### Опциональные переменные

```env
# Telegram Bot (если нужен бот)
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here
TELEGRAM_WEBHOOK_URL=https://your-domain.com

# База данных (по умолчанию SQLite)
DATABASE_URL=sqlite:///./data/ai_content_curator.db

# CORS настройки
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com

# Режим отладки (только для разработки)
DEBUG=False
```

## 🌐 Продакшен деплой

### 1. Подготовка сервера

```bash
# Обновляем систему
sudo apt update && sudo apt upgrade -y

# Устанавливаем Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Устанавливаем Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Добавляем пользователя в группу docker
sudo usermod -aG docker $USER
```

### 2. Настройка SSL сертификатов

```bash
# Создаем директорию для SSL
mkdir -p ssl

# Получаем сертификаты через Let's Encrypt
sudo apt install certbot
sudo certbot certonly --standalone -d your-domain.com

# Копируем сертификаты
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/
sudo chown $USER:$USER ssl/*
```

### 3. Настройка Nginx

Отредактируйте `nginx.conf` для продакшена:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream app {
        server app:8000;
    }

    # Редирект с HTTP на HTTPS
    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS конфигурация
    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        # SSL сертификаты
        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;
        
        # SSL настройки
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;

        # Безопасность
        add_header Strict-Transport-Security "max-age=63072000" always;
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;

        # Размер загружаемых файлов
        client_max_body_size 10M;

        # Основное приложение
        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### 4. Запуск продакшен окружения

```bash
# Обновляем переменные окружения для продакшена
nano .env

# Запускаем с продакшен профилем
docker-compose --profile production up --build -d

# Проверяем статус
docker-compose ps
```

## 🤖 Настройка Telegram бота

### Webhook режим (для продакшена)

```bash
# Устанавливаем webhook
curl -X GET "https://your-domain.com/api/webhook/telegram/set"

# Проверяем статус webhook
curl -X GET "https://your-domain.com/api/webhook/telegram/info"
```

### Polling режим (для разработки)

```bash
# Запускаем бота в отдельном контейнере
docker-compose --profile bot-polling up -d telegram-bot
```

## 📊 Мониторинг и логи

### Просмотр логов

```bash
# Логи всех сервисов
docker-compose logs -f

# Логи конкретного сервиса
docker-compose logs -f app
docker-compose logs -f nginx
docker-compose logs -f telegram-bot
```

### Health check

```bash
# Проверка здоровья приложения
curl https://your-domain.com/health

# Ответ должен быть:
# {"status": "healthy", "service": "AI Content Curator"}
```

### Мониторинг ресурсов

```bash
# Использование ресурсов контейнерами
docker stats

# Размер образов
docker images

# Использование дискового пространства
docker system df
```

## 🔄 Обновление приложения

### Автоматическое обновление

```bash
#!/bin/bash
# update.sh

echo "🔄 Обновление AI Content Curator..."

# Останавливаем сервисы
docker-compose down

# Получаем последние изменения
git pull origin main

# Пересобираем и запускаем
docker-compose --profile production up --build -d

# Очищаем старые образы
docker image prune -f

echo "✅ Обновление завершено!"
```

### Ручное обновление

```bash
# Остановка сервисов
docker-compose down

# Обновление кода
git pull

# Пересборка образов
docker-compose build --no-cache

# Запуск обновленных сервисов
docker-compose --profile production up -d
```

## 🗄️ Резервное копирование

### Backup базы данных

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Создаем директорию для бэкапов
mkdir -p $BACKUP_DIR

# Копируем базу данных
docker cp $(docker-compose ps -q app):/app/data/ai_content_curator.db $BACKUP_DIR/db_backup_$DATE.db

# Архивируем старые бэкапы (старше 30 дней)
find $BACKUP_DIR -name "db_backup_*.db" -mtime +30 -delete

echo "✅ Backup создан: $BACKUP_DIR/db_backup_$DATE.db"
```

### Восстановление из backup

```bash
# Остановка приложения
docker-compose down

# Восстановление базы данных
cp /backups/db_backup_YYYYMMDD_HHMMSS.db ./data/ai_content_curator.db

# Запуск приложения
docker-compose up -d
```

## 🔧 Troubleshooting

### Проблемы с запуском

```bash
# Проверка логов
docker-compose logs app

# Проверка конфигурации
docker-compose config

# Пересборка без кэша
docker-compose build --no-cache
```

### Проблемы с SSL

```bash
# Проверка сертификатов
openssl x509 -in ssl/fullchain.pem -text -noout

# Обновление сертификатов
sudo certbot renew
```

### Проблемы с Telegram ботом

```bash
# Проверка webhook
curl -X GET "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"

# Удаление webhook
curl -X GET "https://api.telegram.org/bot<TOKEN>/deleteWebhook"
```

## 📈 Оптимизация производительности

### Настройки Docker

```yaml
# docker-compose.override.yml для продакшена
version: '3.8'

services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
    restart: unless-stopped
```

### Настройки Nginx

```nginx
# Кэширование статических файлов
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# Gzip сжатие
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
```

## 🔐 Безопасность

### Firewall настройки

```bash
# Настройка UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Регулярные обновления

```bash
# Автоматические обновления безопасности
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### Мониторинг безопасности

```bash
# Установка fail2ban
sudo apt install fail2ban

# Конфигурация для Nginx
sudo nano /etc/fail2ban/jail.local
```

## 📞 Поддержка

При возникновении проблем с деплоем:

1. Проверьте логи: `docker-compose logs`
2. Убедитесь, что все переменные окружения настроены
3. Проверьте доступность портов
4. Обратитесь к разделу Troubleshooting
5. Создайте issue в GitHub репозитории
