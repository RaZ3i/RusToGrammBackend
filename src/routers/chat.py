import asyncio

from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    Depends,
    Response,
    Request,
)
from typing import Dict

from jwt import ExpiredSignatureError

from schemas.user_info import UserInfo
from service.service import create_message, get_messages_between_users
from schemas.user_info_in import MessageCreate
from src.utils.auth import (
    get_current_auth_user_from_cookie,
    get_current_auth_user_from_refresh,
)

router = APIRouter(prefix="/profile/chat", tags=["Profile_operation"])


active_connections: Dict[int, WebSocket] = {}


# Функция для отправки сообщения пользователю, если он подключен
async def notify_user(user_id: int, message: dict):
    if user_id in active_connections:
        websocket = active_connections[user_id]
        await websocket.send_json(message)


# WebSocket эндпоинт для соединений
@router.websocket("/ws/{user_id}/")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    # Принимаем WebSocket-соединение
    await websocket.accept()
    # Сохраняем активное соединение для пользователя
    active_connections[user_id] = websocket
    try:
        while True:
            # Просто поддерживаем соединение активным (1 секунда паузы)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        # Удаляем пользователя из активных соединений при отключении
        active_connections.pop(user_id, None)


@router.post("/messages/")
async def send_message(
    response: Response,
    request: Request,
    message_data: MessageCreate,
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    if current_user == ExpiredSignatureError:
        current_user = await get_current_auth_user_from_refresh(request=request)
        response.set_cookie(
            key="users_access_token",
            value=current_user["access_token"],
            httponly=True,
        )
        await create_message(
            sender_id=current_user["user_info"]["id"],
            recipient_id=message_data.recipient_id,
            content=message_data.content,
        )
        data = {
            "sender_id": current_user["user_info"]["id"],
            "recipient_id": message_data.recipient_id,
            "content": message_data.content,
        }
        await notify_user(message_data.recipient_id, data)
        await notify_user(current_user["user_info"]["id"], data)
        return {"success": True}
    else:
        await create_message(
            sender_id=current_user["id"],
            recipient_id=message_data.recipient_id,
            content=message_data.content,
        )
        data = {
            "sender_id": current_user["id"],
            "recipient_id": message_data.recipient_id,
            "content": message_data.content,
        }
        await notify_user(message_data.recipient_id, data)
        await notify_user(current_user["id"], data)
        return {"success": True}


@router.get("/messages/{user_id}")
async def get_messages(
    response: Response,
    request: Request,
    user_id: int,
    current_user: UserInfo = Depends(get_current_auth_user_from_cookie),
):
    if current_user == ExpiredSignatureError:
        current_user = await get_current_auth_user_from_refresh(request=request)
        response.set_cookie(
            key="users_access_token",
            value=current_user["access_token"],
            httponly=True,
        )
        res = await get_messages_between_users(
            user_id_1=user_id, user_id_2=current_user["user_info"]["id"]
        )
        return res
    else:
        res = await get_messages_between_users(
            user_id_1=user_id, user_id_2=current_user["id"]
        )
        return res
