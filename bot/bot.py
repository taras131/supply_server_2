from fastapi import Depends
from core.models import Subscriber, db_helper
from telegram.error import Forbidden
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from telegram.ext import Application, CommandHandler, CallbackContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select

TOKEN = "7588156307:AAH3JN6qVxxjyJ3y1lMeYmekGvG5P-eEFnQ"

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def subscribe(update: Update, context: CallbackContext):
    # Получаем scoped session из db_helper
    session = db_helper.get_scoped_session()

    try:
        # Обработка подписки
        user = update.effective_user
        subscriber = Subscriber(chat_id=user.id, username=user.username or "Unknown")

        session.add(subscriber)  # Добавляем объект в сессию
        await session.commit()  # Завершаем транзакцию

        # Отправляем сообщение пользователю
        await update.message.reply_text(
            f"Спасибо за подписку, {user.first_name or 'Друг'}!"
        )
    except Exception as e:
        # Откат изменений в случае ошибки
        await session.rollback()
        raise e
    finally:
        # Закрытие scoped session после завершения
        await session.remove()


async def post_init(application: Application):
    await application.bot.set_my_commands(
        [
            ("subscribe", "Подписаться на обновления"),
        ]
    )


async def error_handler(update: Update, context: CallbackContext):
    # Логируем исключение
    print("Произошла ошибка:", context.error)


async def start_bot():
    try:
        logger.info("Запуск Telegram бота...")
        application = Application.builder().token(TOKEN).post_init(post_init).build()
        application.add_handler(CommandHandler("subscribe", subscribe))
        application.add_error_handler(error_handler)
        await application.initialize()
        await application.start()
        await application.updater.start_polling()

        while True:
            await asyncio.sleep(3600)
    except Exception as e:
        logger.error(f"Ошибка в работе бота: {e}")
    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()


async def send_notification(chat_id: int, problem_data: dict):
    try:
        message = f"🚨 Новая проблема с оборудованием!"
        # await bot.send_message(
        #    chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN_V2
    #  )
    except Forbidden:
        # Обработка ошибки если пользователь заблокировал бота
        pass
