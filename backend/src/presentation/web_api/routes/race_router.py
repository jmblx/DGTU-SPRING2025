import asyncio
import json

from dishka import AsyncContainer, FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

race_router = APIRouter()
