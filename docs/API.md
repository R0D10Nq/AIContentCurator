# 📚 API Документация

## Обзор

AI Content Curator предоставляет RESTful API для анализа текстового контента с помощью искусственного интеллекта. API построен на FastAPI и предоставляет автоматическую документацию.

## Базовый URL

```
http://localhost:8000/api
```

## Аутентификация

API использует JWT токены для аутентификации. Для получения токена используйте эндпоинт `/auth/token`.

### Заголовки

```http
Authorization: Bearer <your-jwt-token>
Content-Type: application/json
```

## Эндпоинты

### Аутентификация

#### POST /auth/register
Регистрация нового пользователя.

**Тело запроса:**
```json
{
  "username": "string",
  "email": "user@example.com",
  "password": "string"
}
```

**Ответ:**
```json
{
  "id": 1,
  "username": "string",
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

#### POST /auth/token
Получение JWT токена.

**Тело запроса (form-data):**
```
username: string
password: string
```

**Ответ:**
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

#### GET /auth/me
Получение информации о текущем пользователе.

**Заголовки:** `Authorization: Bearer <token>`

**Ответ:**
```json
{
  "id": 1,
  "username": "string",
  "email": "user@example.com",
  "telegram_id": "string",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

### Анализ контента

#### POST /analysis/
Создание нового анализа.

**Заголовки:** `Authorization: Bearer <token>`

**Тело запроса:**
```json
{
  "text": "Текст для анализа",
  "analysis_type": "sentiment" // sentiment, summary, keywords
}
```

**Ответ:**
```json
{
  "id": 1,
  "original_text": "Текст для анализа",
  "analysis_type": "sentiment",
  "result": "Результат анализа",
  "confidence_score": "0.95",
  "processing_time": "1.23s",
  "created_at": "2024-01-01T00:00:00"
}
```

#### GET /analysis/
Получение списка анализов пользователя.

**Заголовки:** `Authorization: Bearer <token>`

**Параметры запроса:**
- `skip` (int): Количество пропускаемых записей (по умолчанию: 0)
- `limit` (int): Максимальное количество записей (по умолчанию: 20)
- `analysis_type` (string): Фильтр по типу анализа

**Ответ:**
```json
{
  "analyses": [
    {
      "id": 1,
      "original_text": "Текст для анализа",
      "analysis_type": "sentiment",
      "result": "Результат анализа",
      "confidence_score": "0.95",
      "processing_time": "1.23s",
      "created_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 1
}
```

#### GET /analysis/{analysis_id}
Получение конкретного анализа.

**Заголовки:** `Authorization: Bearer <token>`

**Ответ:**
```json
{
  "id": 1,
  "original_text": "Текст для анализа",
  "analysis_type": "sentiment",
  "result": "Результат анализа",
  "confidence_score": "0.95",
  "processing_time": "1.23s",
  "created_at": "2024-01-01T00:00:00"
}
```

#### DELETE /analysis/{analysis_id}
Удаление анализа.

**Заголовки:** `Authorization: Bearer <token>`

**Ответ:**
```json
{
  "message": "Анализ успешно удален"
}
```

### Пользователи

#### GET /users/
Получение списка пользователей (требует аутентификации).

**Заголовки:** `Authorization: Bearer <token>`

#### PUT /users/me
Обновление профиля текущего пользователя.

**Заголовки:** `Authorization: Bearer <token>`

**Тело запроса:**
```json
{
  "username": "new_username",
  "email": "new@example.com",
  "telegram_id": "123456789"
}
```

## Коды ошибок

| Код | Описание |
|-----|----------|
| 200 | Успешный запрос |
| 201 | Ресурс создан |
| 400 | Неверный запрос |
| 401 | Не авторизован |
| 403 | Доступ запрещен |
| 404 | Ресурс не найден |
| 422 | Ошибка валидации |
| 500 | Внутренняя ошибка сервера |

## Примеры использования

### Python (requests)

```python
import requests

# Регистрация
response = requests.post('http://localhost:8000/api/auth/register', json={
    'username': 'testuser',
    'email': 'test@example.com',
    'password': 'password123'
})

# Получение токена
response = requests.post('http://localhost:8000/api/auth/token', data={
    'username': 'testuser',
    'password': 'password123'
})
token = response.json()['access_token']

# Анализ текста
headers = {'Authorization': f'Bearer {token}'}
response = requests.post('http://localhost:8000/api/analysis/', 
    headers=headers,
    json={
        'text': 'Отличный продукт! Очень доволен покупкой.',
        'analysis_type': 'sentiment'
    }
)
analysis = response.json()
```

### JavaScript (fetch)

```javascript
// Получение токена
const tokenResponse = await fetch('http://localhost:8000/api/auth/token', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: 'username=testuser&password=password123'
});
const { access_token } = await tokenResponse.json();

// Анализ текста
const analysisResponse = await fetch('http://localhost:8000/api/analysis/', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${access_token}`,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        text: 'Отличный продукт! Очень доволен покупкой.',
        analysis_type: 'sentiment'
    })
});
const analysis = await analysisResponse.json();
```

### cURL

```bash
# Получение токена
curl -X POST "http://localhost:8000/api/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=testuser&password=password123"

# Анализ текста
curl -X POST "http://localhost:8000/api/analysis/" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Отличный продукт! Очень доволен покупкой.",
       "analysis_type": "sentiment"
     }'
```

## Ограничения

- Максимальная длина текста для анализа: 5000 символов
- Лимит запросов: 100 запросов в минуту на пользователя
- Поддерживаемые типы анализа: sentiment, summary, keywords

## Webhook для Telegram

### POST /webhook/telegram
Эндпоинт для получения обновлений от Telegram бота.

### GET /webhook/telegram/set
Установка webhook для Telegram бота.

### GET /webhook/telegram/info
Получение информации о текущем webhook.
