import asyncio
import json

from dishka import AsyncContainer, FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from application.race_simulate import RaceBroadcaster, logger

race_router = APIRouter()


@race_router.websocket("/ws/current_race")
@inject
async def websocket_race_updates(
    websocket: WebSocket,
    race_manager: FromDishka[RaceBroadcaster],
    container: FromDishka[AsyncContainer],
):
    """WebSocket endpoint для получения обновлений о текущей гонке"""
    await race_manager.connect_websocket(websocket)

    try:
        logger.info("Current race %s", await race_manager.current_race_id)

        # Wait until a race ID is available (if none exists yet)
        while await race_manager.current_race_id is None:
            await asyncio.sleep(1)  # Wait for 1 second before checking again

        # Fetch and send the initial race metadata
        async with container() as request_container:
            race_meta = await request_container.get(
                lambda: race_manager.redis.get(
                    f"race:{race_manager.current_race_id}:meta"
                )
            )
            if race_meta:
                await websocket.send_json(
                    {"type": "current_race", "race": json.loads(race_meta)}
                )

        # Keep listening for updates and sending new data every 0.1 seconds
        while True:
            await asyncio.sleep(0.1)  # 0.1 seconds interval for updates

            if race_manager.current_race_id:
                race_meta = await container.get(
                    lambda: race_manager.redis.get(
                        f"race:{race_manager.current_race_id}:meta"
                    )
                )
                if race_meta:
                    await websocket.send_json(
                        {"type": "current_race", "race": json.loads(race_meta)}
                    )
                else:
                    logger.warning(
                        f"Race metadata for {race_manager.current_race_id} not found."
                    )
            else:
                logger.warning("Current race ID is not available.")
                await websocket.send_json(
                    {"type": "current_race", "message": "No race has started yet"}
                )

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        race_manager.disconnect_websocket(websocket)
