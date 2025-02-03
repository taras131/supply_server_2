from fastapi import APIRouter, Request, Depends
import httpx
from core.config import settings
from api_v1.bot.bot import handle_message
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper

logger = logging.getLogger(__name__)  # Инициализация логгера для модуля
router = APIRouter()


@router.get("/webhook-info")
async def get_webhook_info():
    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/getWebhookInfo"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()


@router.get("/check_webhook")
async def check_webhook_status():
    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/getWebhookInfo"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()


@router.get("/check_bot")
async def check_bot():
    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/getMe"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()


@router.post("/webhook")
async def telegram_webhook(
    request: Request,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    try:
        print("Webhook endpoint hit!")
        data = await request.json()
        print("Received data:", data)
        headers = dict(request.headers)
        print("Request headers:", headers)
        await handle_message(data, session)
        return {"ok": True}
    except Exception as e:
        print(f"Error in webhook handler: {str(e)}")
        return {"ok": False, "error": str(e)}


@router.get("/test-bot")
async def test_bot():
    try:
        me_url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/getMe"
        async with httpx.AsyncClient() as client:
            me_response = await client.get(me_url)
            bot_info = me_response.json()

        webhook_url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/getWebhookInfo"
        async with httpx.AsyncClient() as client:
            webhook_response = await client.get(webhook_url)
            webhook_info = webhook_response.json()

        return {
            "bot_info": bot_info,
            "webhook_info": webhook_info,
            "current_webhook_url": settings.WEBHOOK_URL,
        }
    except Exception as e:
        return {"error": str(e)}
