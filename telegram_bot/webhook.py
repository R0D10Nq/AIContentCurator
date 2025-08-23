"""
Webhook для Telegram бота в FastAPI
"""

from fastapi import APIRouter, Request, HTTPException
from telegram import Update
from telegram.ext import Application
import json
import logging
from backend.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# Глобальная переменная для хранения приложения бота
bot_application: Application = None


async def initialize_bot_application():
    """Инициализация приложения бота для webhook"""
    global bot_application
    
    if bot_application is None:
        from telegram_bot.bot import AIContentCuratorBot
        bot = AIContentCuratorBot()
        await bot.initialize()
        bot_application = bot.application
    
    return bot_application


@router.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    """Обработчик webhook от Telegram"""
    try:
        # Получаем данные от Telegram
        data = await request.json()
        
        # Инициализируем бота если нужно
        app = await initialize_bot_application()
        
        # Создаем объект Update
        update = Update.de_json(data, app.bot)
        
        # Обрабатываем обновление
        await app.process_update(update)
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Ошибка в webhook: {e}")
        raise HTTPException(status_code=500, detail="Ошибка обработки webhook")


@router.get("/webhook/telegram/set")
async def set_telegram_webhook():
    """Установка webhook для Telegram бота"""
    try:
        app = await initialize_bot_application()
        
        webhook_url = f"{settings.TELEGRAM_WEBHOOK_URL}/webhook/telegram"
        await app.bot.set_webhook(url=webhook_url)
        
        return {"status": "webhook set", "url": webhook_url}
        
    except Exception as e:
        logger.error(f"Ошибка установки webhook: {e}")
        raise HTTPException(status_code=500, detail="Ошибка установки webhook")


@router.get("/webhook/telegram/info")
async def get_telegram_webhook_info():
    """Получение информации о webhook"""
    try:
        app = await initialize_bot_application()
        webhook_info = await app.bot.get_webhook_info()
        
        return {
            "url": webhook_info.url,
            "has_custom_certificate": webhook_info.has_custom_certificate,
            "pending_update_count": webhook_info.pending_update_count,
            "last_error_date": webhook_info.last_error_date,
            "last_error_message": webhook_info.last_error_message,
            "max_connections": webhook_info.max_connections,
            "allowed_updates": webhook_info.allowed_updates
        }
        
    except Exception as e:
        logger.error(f"Ошибка получения информации webhook: {e}")
        raise HTTPException(status_code=500, detail="Ошибка получения информации")


@router.delete("/webhook/telegram")
async def delete_telegram_webhook():
    """Удаление webhook"""
    try:
        app = await initialize_bot_application()
        await app.bot.delete_webhook()
        
        return {"status": "webhook deleted"}
        
    except Exception as e:
        logger.error(f"Ошибка удаления webhook: {e}")
        raise HTTPException(status_code=500, detail="Ошибка удаления webhook")
