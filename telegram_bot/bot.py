"""
Telegram бот для AI Content Curator
"""

import asyncio
import logging
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    CallbackQueryHandler, ContextTypes, filters
)
import httpx
from backend.config import settings
from backend.database import SessionLocal
from backend.models import User, TelegramSession, Analysis
from backend.services.gemini_service import GeminiService

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# API URL для взаимодействия с бэкендом
API_BASE_URL = "http://localhost:8000/api"


class AIContentCuratorBot:
    """Основной класс Telegram бота"""
    
    def __init__(self):
        self.application = None
        self.gemini_service = None
        
    async def initialize(self):
        """Инициализация бота"""
        if not settings.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN не установлен")
        
        # Инициализируем Gemini сервис
        try:
            self.gemini_service = GeminiService()
        except Exception as e:
            logger.warning(f"Не удалось инициализировать Gemini: {e}")
        
        # Создаем приложение
        self.application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        
        # Регистрируем обработчики
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("connect", self.connect_command))
        self.application.add_handler(CommandHandler("disconnect", self.disconnect_command))
        self.application.add_handler(CommandHandler("analyze", self.analyze_command))
        self.application.add_handler(CommandHandler("history", self.history_command))
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        
        logger.info("Бот инициализирован")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        # Сохраняем или обновляем сессию Telegram
        await self.save_telegram_session(user)
        
        welcome_text = f"""
🤖 Привет, {user.first_name}! 

Добро пожаловать в AI Content Curator Bot!

🔥 Что я умею:
• Анализ тональности текста
• Создание кратких выжимок
• Извлечение ключевых слов
• Сохранение истории анализов

📝 Просто отправь мне любой текст, и я проанализирую его с помощью ИИ!

Используй /help для получения списка команд.
        """
        
        keyboard = [
            [InlineKeyboardButton("📊 Анализ тональности", callback_data="analyze_sentiment")],
            [InlineKeyboardButton("📄 Краткая выжимка", callback_data="analyze_summary")],
            [InlineKeyboardButton("🔑 Ключевые слова", callback_data="analyze_keywords")],
            [InlineKeyboardButton("🌐 Открыть веб-версию", url="http://localhost:3000")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = """
🤖 AI Content Curator Bot - Команды:

/start - Запуск бота и главное меню
/help - Показать это сообщение
/connect <username> - Привязать аккаунт к Telegram
/disconnect - Отвязать аккаунт от Telegram
/analyze <тип> <текст> - Быстрый анализ
/history - Показать последние анализы

📝 Типы анализа:
• sentiment - анализ тональности
• summary - краткая выжимка  
• keywords - ключевые слова

💡 Примеры использования:
/analyze sentiment Отличный продукт!
/analyze summary Длинный текст для сокращения...

Или просто отправь текст, и я предложу варианты анализа!
        """
        await update.message.reply_text(help_text)
    
    async def connect_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /connect"""
        if not context.args:
            await update.message.reply_text(
                "❌ Укажите имя пользователя: /connect <username>"
            )
            return
        
        username = context.args[0]
        telegram_id = str(update.effective_user.id)
        
        # Здесь должна быть логика привязки аккаунта
        # Пока что просто сохраняем связь в базе
        db = SessionLocal()
        try:
            # Ищем пользователя по имени
            user = db.query(User).filter(User.username == username).first()
            if not user:
                await update.message.reply_text(
                    f"❌ Пользователь '{username}' не найден. "
                    "Зарегистрируйтесь на сайте: http://localhost:3000/register"
                )
                return
            
            # Обновляем telegram_id у пользователя
            user.telegram_id = telegram_id
            db.commit()
            
            await update.message.reply_text(
                f"✅ Аккаунт '{username}' успешно привязан к Telegram!\n"
                "Теперь ваши анализы будут сохраняться в личном кабинете."
            )
            
        except Exception as e:
            logger.error(f"Ошибка при привязке аккаунта: {e}")
            await update.message.reply_text(
                "❌ Произошла ошибка при привязке аккаунта. Попробуйте позже."
            )
        finally:
            db.close()
    
    async def disconnect_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /disconnect"""
        telegram_id = str(update.effective_user.id)
        
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            if user:
                user.telegram_id = None
                db.commit()
                await update.message.reply_text("✅ Аккаунт отвязан от Telegram")
            else:
                await update.message.reply_text("❌ Аккаунт не был привязан")
        except Exception as e:
            logger.error(f"Ошибка при отвязке аккаунта: {e}")
            await update.message.reply_text("❌ Произошла ошибка")
        finally:
            db.close()
    
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /analyze"""
        if len(context.args) < 2:
            await update.message.reply_text(
                "❌ Использование: /analyze <тип> <текст>\n"
                "Типы: sentiment, summary, keywords"
            )
            return
        
        analysis_type = context.args[0].lower()
        text = " ".join(context.args[1:])
        
        if analysis_type not in ["sentiment", "summary", "keywords"]:
            await update.message.reply_text(
                "❌ Неверный тип анализа. Доступные: sentiment, summary, keywords"
            )
            return
        
        await self.perform_analysis(update, text, analysis_type)
    
    async def history_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /history"""
        telegram_id = str(update.effective_user.id)
        
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            if not user:
                await update.message.reply_text(
                    "❌ Аккаунт не привязан. Используйте /connect <username>"
                )
                return
            
            # Получаем последние анализы
            analyses = db.query(Analysis).filter(
                Analysis.user_id == user.id
            ).order_by(Analysis.created_at.desc()).limit(5).all()
            
            if not analyses:
                await update.message.reply_text("📭 У вас пока нет анализов")
                return
            
            history_text = "📊 Ваши последние анализы:\n\n"
            for i, analysis in enumerate(analyses, 1):
                type_emoji = {
                    "sentiment": "😊",
                    "summary": "📄",
                    "keywords": "🔑"
                }.get(analysis.analysis_type, "📊")
                
                history_text += f"{type_emoji} {i}. {analysis.analysis_type.title()}\n"
                history_text += f"📝 {analysis.original_text[:50]}...\n"
                history_text += f"💡 {analysis.result[:100]}...\n"
                history_text += f"📅 {analysis.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
            
            await update.message.reply_text(history_text)
            
        except Exception as e:
            logger.error(f"Ошибка при получении истории: {e}")
            await update.message.reply_text("❌ Произошла ошибка")
        finally:
            db.close()
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на кнопки"""
        query = update.callback_query
        await query.answer()
        
        if query.data.startswith("analyze_"):
            analysis_type = query.data.replace("analyze_", "")
            context.user_data["waiting_for_text"] = analysis_type
            
            type_names = {
                "sentiment": "анализа тональности",
                "summary": "создания выжимки",
                "keywords": "извлечения ключевых слов"
            }
            
            await query.edit_message_text(
                f"📝 Отправьте текст для {type_names.get(analysis_type, 'анализа')}:"
            )
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений"""
        text = update.message.text
        
        # Проверяем, ждем ли мы текст для анализа
        if "waiting_for_text" in context.user_data:
            analysis_type = context.user_data.pop("waiting_for_text")
            await self.perform_analysis(update, text, analysis_type)
            return
        
        # Если текст длинный, предлагаем варианты анализа
        if len(text) > 20:
            keyboard = [
                [InlineKeyboardButton("😊 Анализ тональности", callback_data="analyze_sentiment")],
                [InlineKeyboardButton("📄 Краткая выжимка", callback_data="analyze_summary")],
                [InlineKeyboardButton("🔑 Ключевые слова", callback_data="analyze_keywords")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "📝 Получил ваш текст! Выберите тип анализа:",
                reply_markup=reply_markup
            )
            context.user_data["last_text"] = text
        else:
            await update.message.reply_text(
                "📝 Отправьте более длинный текст для анализа (минимум 20 символов)"
            )
    
    async def perform_analysis(self, update: Update, text: str, analysis_type: str):
        """Выполнение анализа текста"""
        if not self.gemini_service:
            await update.message.reply_text(
                "❌ Сервис анализа недоступен. Проверьте настройки Gemini API."
            )
            return
        
        # Отправляем сообщение о начале анализа
        status_message = await update.message.reply_text("🤖 Анализирую текст...")
        
        try:
            # Выполняем анализ
            if analysis_type == "sentiment":
                result, confidence = await self.gemini_service.analyze_sentiment(text)
                emoji = "😊"
                type_name = "Анализ тональности"
            elif analysis_type == "summary":
                result, confidence = await self.gemini_service.create_summary(text)
                emoji = "📄"
                type_name = "Краткая выжимка"
            elif analysis_type == "keywords":
                result, confidence = await self.gemini_service.extract_keywords(text)
                emoji = "🔑"
                type_name = "Ключевые слова"
            else:
                await status_message.edit_text("❌ Неподдерживаемый тип анализа")
                return
            
            # Сохраняем результат в базу данных (если пользователь привязан)
            await self.save_analysis(update.effective_user.id, text, analysis_type, result, confidence)
            
            # Формируем ответ
            response_text = f"{emoji} **{type_name}**\n\n"
            response_text += f"📝 **Исходный текст:**\n{text[:200]}{'...' if len(text) > 200 else ''}\n\n"
            response_text += f"💡 **Результат:**\n{result}\n\n"
            
            if confidence:
                response_text += f"🎯 **Уверенность:** {confidence}\n"
            
            response_text += "✅ Анализ завершен!"
            
            await status_message.edit_text(response_text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Ошибка при анализе: {e}")
            await status_message.edit_text(
                "❌ Произошла ошибка при анализе текста. Попробуйте позже."
            )
    
    async def save_telegram_session(self, user):
        """Сохранение сессии Telegram пользователя"""
        db = SessionLocal()
        try:
            session = db.query(TelegramSession).filter(
                TelegramSession.telegram_id == str(user.id)
            ).first()
            
            if not session:
                session = TelegramSession(
                    telegram_id=str(user.id),
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name
                )
                db.add(session)
            else:
                session.username = user.username
                session.first_name = user.first_name
                session.last_name = user.last_name
            
            db.commit()
        except Exception as e:
            logger.error(f"Ошибка при сохранении сессии: {e}")
        finally:
            db.close()
    
    async def save_analysis(self, telegram_user_id: int, text: str, analysis_type: str, result: str, confidence: Optional[float]):
        """Сохранение результата анализа в базу данных"""
        db = SessionLocal()
        try:
            # Ищем пользователя по telegram_id
            user = db.query(User).filter(User.telegram_id == str(telegram_user_id)).first()
            if not user:
                return  # Пользователь не привязан
            
            # Создаем запись анализа
            analysis = Analysis(
                user_id=user.id,
                original_text=text,
                analysis_type=analysis_type,
                result=result,
                confidence_score=str(confidence) if confidence else None
            )
            
            db.add(analysis)
            db.commit()
            
        except Exception as e:
            logger.error(f"Ошибка при сохранении анализа: {e}")
        finally:
            db.close()
    
    async def run(self):
        """Запуск бота"""
        await self.initialize()
        logger.info("Запускаю бота...")
        await self.application.run_polling()


async def main():
    """Главная функция"""
    bot = AIContentCuratorBot()
    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())
