# 🤖 AI Content Curator

**Платформа для анализа контента с помощью искусственного интеллекта**

AI Content Curator - это современное веб-приложение для анализа текстового контента с использованием Gemini AI. Проект включает веб-интерфейс на Vue.js, REST API на FastAPI и Telegram бота для удобного доступа.

## 🚀 Возможности

### 📊 Анализ контента
- **Анализ тональности** - определение эмоциональной окраски текста
- **Краткие выжимки** - создание сжатых версий больших текстов
- **Ключевые слова** - извлечение важных терминов и тем

### 🌐 Веб-интерфейс
- Современный адаптивный дизайн на Vue.js 3
- Система аутентификации и регистрации
- История анализов с фильтрацией и поиском
- Экспорт результатов
- Панель управления с статистикой

### 🤖 Telegram бот
- Быстрый анализ текстов прямо из мессенджера
- Привязка к веб-аккаунту
- Сохранение истории анализов
- Интуитивное меню и команды

### 🔧 Технические особенности
- REST API с автоматической документацией
- Интеграция с Gemini AI
- SQLite база данных
- Docker контейнеризация
- Готовность к продакшен деплою

## 🛠 Технологический стек

### Backend
- **FastAPI** - современный Python веб-фреймворк
- **SQLAlchemy** - ORM для работы с базой данных
- **Pydantic** - валидация данных
- **JWT** - аутентификация
- **Google Gemini AI** - анализ текста

### Frontend
- **Vue.js 3** - прогрессивный JavaScript фреймворк
- **Element Plus** - UI компоненты
- **Vuex** - управление состоянием
- **Vue Router** - маршрутизация
- **Axios** - HTTP клиент

### Telegram Bot
- **python-telegram-bot** - библиотека для Telegram API
- **Webhook/Polling** - поддержка обоих режимов

### DevOps
- **Docker** - контейнеризация
- **Docker Compose** - оркестрация
- **Nginx** - веб-сервер для продакшена
- **GitHub Actions** - CI/CD

## 📦 Быстрый старт

### Предварительные требования
- Python 3.11+
- Node.js 18+
- Docker и Docker Compose (для контейнерного запуска)

### 🔧 Установка и настройка

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/yourusername/ai-content-curator.git
cd ai-content-curator
```

2. **Настройте переменные окружения:**
```bash
cp .env.example .env
```

Отредактируйте `.env` файл:
```env
# Gemini AI API ключ (обязательно)
GEMINI_API_KEY=your-gemini-api-key-here

# Telegram Bot токен (опционально)
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here

# Секретный ключ для JWT
SECRET_KEY=your-super-secret-key-change-this-in-production

# База данных
DATABASE_URL=sqlite:///./ai_content_curator.db
```

### 🐳 Запуск с Docker (рекомендуется)

```bash
# Запуск основного приложения
docker-compose up --build -d

# Запуск с Telegram ботом
docker-compose --profile bot-polling up --build -d
```

Приложение будет доступно по адресу: http://localhost:8000

### 🔨 Запуск для разработки

#### Backend
```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend

# Установка зависимостей
npm install

# Запуск dev сервера
npm run serve
```

#### Telegram Bot
```bash
# Запуск бота в polling режиме
python telegram_bot/bot.py
```

## 📚 API Документация

После запуска приложения документация API доступна по адресам:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Основные эндпоинты

#### Аутентификация
- `POST /api/auth/register` - регистрация
- `POST /api/auth/token` - получение токена
- `GET /api/auth/me` - информация о пользователе

#### Анализ контента
- `POST /api/analysis/` - создание анализа
- `GET /api/analysis/` - список анализов
- `GET /api/analysis/{id}` - получение анализа
- `DELETE /api/analysis/{id}` - удаление анализа

## 🤖 Telegram бот

### Команды бота
- `/start` - запуск и главное меню
- `/help` - справка по командам
- `/connect <username>` - привязка аккаунта
- `/analyze <тип> <текст>` - быстрый анализ
- `/history` - история анализов

### Настройка бота

1. Создайте бота через [@BotFather](https://t.me/botfather)
2. Получите токен и добавьте в `.env`
3. Запустите бота или настройте webhook

## 🔧 Конфигурация

### Переменные окружения

| Переменная | Описание | Обязательная |
|------------|----------|--------------|
| `GEMINI_API_KEY` | API ключ Google Gemini | ✅ |
| `TELEGRAM_BOT_TOKEN` | Токен Telegram бота | ❌ |
| `SECRET_KEY` | Секретный ключ для JWT | ✅ |
| `DATABASE_URL` | URL базы данных | ❌ |
| `DEBUG` | Режим отладки | ❌ |
| `ALLOWED_ORIGINS` | CORS origins | ❌ |

### Получение API ключей

#### Gemini AI
1. Перейдите на [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Создайте новый API ключ
3. Добавьте ключ в `.env` файл

#### Telegram Bot
1. Напишите [@BotFather](https://t.me/botfather)
2. Создайте нового бота командой `/newbot`
3. Получите токен и добавьте в `.env`

## 🚀 Деплой

### Docker Compose (рекомендуется)

```bash
# Продакшен с Nginx
docker-compose --profile production up -d

# Только приложение
docker-compose up -d
```

### Ручной деплой

1. Соберите фронтенд:
```bash
cd frontend
npm run build
```

2. Настройте веб-сервер (Nginx/Apache)
3. Запустите FastAPI приложение
4. Настройте SSL сертификаты

## 🧪 Тестирование

```bash
# Запуск тестов
pytest

# С покрытием кода
pytest --cov=backend

# Линтинг
flake8 backend/
black backend/
isort backend/
```

## 📁 Структура проекта

```
ai-content-curator/
├── backend/                 # FastAPI приложение
│   ├── routers/            # API роутеры
│   ├── services/           # Бизнес-логика
│   ├── models.py           # Модели БД
│   ├── schemas.py          # Pydantic схемы
│   └── main.py             # Точка входа
├── frontend/               # Vue.js приложение
│   ├── src/
│   │   ├── components/     # Компоненты
│   │   ├── views/          # Страницы
│   │   ├── store/          # Vuex хранилище
│   │   └── router/         # Маршрутизация
│   └── public/
├── telegram_bot/           # Telegram бот
│   ├── bot.py              # Основной код бота
│   └── webhook.py          # Webhook обработчик
├── scripts/                # Скрипты запуска
├── docker-compose.yml      # Docker конфигурация
├── Dockerfile              # Docker образ
├── requirements.txt        # Python зависимости
└── README.md               # Документация
```

## 🤝 Участие в разработке

1. Форкните репозиторий
2. Создайте ветку для фичи (`git checkout -b feature/amazing-feature`)
3. Сделайте коммит (`git commit -m 'добавил крутую фичу'`)
4. Запушьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

### Стандарты кода
- Следуйте PEP 8 для Python
- Используйте ESLint для JavaScript
- Пишите тесты для новой функциональности
- Обновляйте документацию

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).

## 🆘 Поддержка

- 📧 Email: support@example.com
- 💬 Telegram: [@support_bot](https://t.me/support_bot)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/ai-content-curator/issues)

## 🙏 Благодарности

- [Google Gemini AI](https://ai.google.dev/) за мощный API анализа текста
- [FastAPI](https://fastapi.tiangolo.com/) за отличный веб-фреймворк
- [Vue.js](https://vuejs.org/) за реактивный фронтенд фреймворк
- [Element Plus](https://element-plus.org/) за красивые UI компоненты

---

**Сделано с ❤️ для анализа контента с помощью ИИ**
