"""
Главный файл FastAPI приложения для AI Content Curator
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from backend.database import engine, Base
from backend.routers import analysis, auth, users
from telegram_bot.webhook import router as telegram_router
from backend.config import settings

# Загружаем переменные окружения
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Создаем таблицы в БД при запуске
    Base.metadata.create_all(bind=engine)
    yield
    # Здесь можно добавить код для очистки ресурсов при завершении


# Создаем экземпляр FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Платформа для анализа контента с помощью ИИ",
    lifespan=lifespan
)

# Настройка CORS для работы с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router, prefix="/api/auth", tags=["Аутентификация"])
app.include_router(users.router, prefix="/api/users", tags=["Пользователи"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Анализ контента"])
app.include_router(telegram_router, tags=["Telegram Webhook"])

# Статические файлы для фронтенда
if os.path.exists("frontend/dist"):
    app.mount("/static", StaticFiles(directory="frontend/dist/static"), name="static")


@app.get("/")
async def root():
    """Главная страница API"""
    return {
        "message": "AI Content Curator API работает!",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "healthy", "service": "AI Content Curator"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
