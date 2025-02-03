import httpx
from core.config import settings
from .schemas import SubscriberCreateSchema
from . import crud
from sqlalchemy.ext.asyncio import AsyncSession


async def send_telegram_message(chat_id: int, text: str):
    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    print(f"Sending message to {chat_id}: {text}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            print(f"Telegram API response: {response.status_code}")
            print(f"Response content: {response.text}")
            return response.json()
    except Exception as e:
        print(f"Error sending message: {str(e)}")
        raise


async def handle_subscribe(chat_id: int, user_data: dict, session: AsyncSession):
    existing_subscriber = await crud.get_subscriber_by_chat_id(session, chat_id)
    if existing_subscriber:
        response_text = "Вы уже подписаны на уведомления!"
    else:
        # Получаем данные пользователя
        first_name = user_data.get("first_name", "Пользователь")
        username = user_data.get("username", None)
        # Создаем нового подписчика
        subscriber_data = SubscriberCreateSchema(
            chat_id=chat_id, username=username, is_active=True
        )
        await crud.create_subscriber(session, subscriber_data)
        if username:
            response_text = f"Вы успешно подписаны, @{username}!"
        else:
            response_text = (
                f"Вы успешно подписаны, {first_name}! "
                "(к сожалению, не удалось получить ваш ник)"
            )
    response = await send_telegram_message(chat_id, response_text)
    print("Regular message response:", response)


async def handle_message(data: dict, session: AsyncSession):
    try:
        print("Starting message handling...")
        print("Message data:", data)

        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "")
            # Данные отправителя
            user_data = data["message"]["from"]

            print(f"Processing message: chat_id={chat_id}, text={text}")

            if text == "/start":
                response = await send_telegram_message(
                    chat_id, "Добро пожаловать в бота!"
                )
                print("Start command response:", response)
            elif text == "/subscribe":
                # Передаем chat_id и user_data в handle_subscribe
                await handle_subscribe(chat_id, user_data, session)
            else:
                response = await send_telegram_message(chat_id, f"Вы написали: {text}")
                print("Regular message response:", response)
        else:
            print("No 'message' field in data")
    except Exception as e:
        print(f"Error in handle_message: {str(e)}")
        raise


async def set_webhook():
    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/setWebhook"
    webhook_url = f"{settings.WEBHOOK_URL}/api/v1/bot/webhook"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"url": webhook_url})
        return response.json()
