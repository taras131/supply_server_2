from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
import asyncio, time
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import event
from core.models import db_helper, Machinery, MachineryComment
from core.websocket_utils import State, get_data_hash
from .crud import get_machinery_list
import hashlib

state = State()

"""
@event.listens_for(MachineryComment, "after_update")
def receive_comment_after_update(mapper, connection, target):
    asyncio.run_coroutine_threadsafe(state.notify_changed(), asyncio.get_event_loop())


@event.listens_for(MachineryComment, "after_insert")
def receive_comment_after_insert(mapper, connection, target):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    try:

        async def notify():
            await state.notify_changed()

        future = asyncio.run_coroutine_threadsafe(notify(), loop)
        future.result(timeout=2.0)  # Ждем результат не более 2 секунд
        print(f"Уведомление о новой машине отправлено успешно: {target}")
    except Exception as e:
        print(f"Ошибка при отправке уведомления: {str(e)}")


@event.listens_for(MachineryComment, "after_delete")
def receive_comment_after_delete(mapper, connection, target):
    asyncio.run_coroutine_threadsafe(state.notify_changed(), asyncio.get_event_loop())
"""


@event.listens_for(Machinery, "after_update")
def receive_machinery_after_update(mapper, connection, target):
    asyncio.create_task(state.notify_changed())


@event.listens_for(Machinery, "after_insert")
def receive_machinery_after_insert(mapper, connection, target):
    asyncio.create_task(state.notify_changed())


@event.listens_for(Machinery, "after_delete")
def receive_machinery_after_delete(mapper, connection, target):
    asyncio.create_task(state.notify_changed())


router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    try:
        await websocket.accept()
        print("WebSocket соединение установлено")
        machinery_list = await get_machinery_list(session)
        state.last_data = [machinery.to_dict() for machinery in machinery_list]
        await websocket.send_json(state.last_data)

        while True:
            try:
                await asyncio.wait_for(state.changed_queue.get(), timeout=50)
                await asyncio.sleep(0.5)

                session.expire_all()
                machinery_list = await get_machinery_list(session)
                current_data = [machinery.to_dict() for machinery in machinery_list]

                if get_data_hash(current_data) != get_data_hash(state.last_data):
                    state.last_data = current_data
                    await websocket.send_json(current_data)

            except Exception as e:
                print(f"Ошибка при обработке: {str(e)}")
                await websocket.close()
                break

    except WebSocketDisconnect:
        print("WebSocket соединение закрыто клиентом")
