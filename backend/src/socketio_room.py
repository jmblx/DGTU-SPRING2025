import asyncio
import json
import logging
from threading import Thread

import socketio
import uvicorn
from fastapi import FastAPI
from redis.asyncio import Redis
from socketio import AsyncServer

from core.config import config_loader

app = FastAPI()

sio = AsyncServer(cors_allowed_origins="*", async_mode="asgi")
app.mount("/socket.io", socketio.ASGIApp(sio))

redis_client = Redis.from_url(config_loader.app_config.redis.uri)

logger = logging.getLogger(__name__)


async def send_race_data():
    while True:
        try:
            current_race_id = await redis_client.get("current_race_id")
            if not current_race_id:
                logger.info("No current race ID found, waiting...")
                await asyncio.sleep(5)
                continue

            current_race_id = current_race_id.decode("utf-8")
            logger.info(f"Processing race ID: {current_race_id}")

            race_data = await redis_client.get(f"race:{current_race_id}:results")
            if not race_data:
                logger.info(f"No data found for race {current_race_id}")
                await asyncio.sleep(5)
                continue

            try:
                runners: list[dict] = json.loads(race_data)

                max_length = max(len(runner["progress"]) for runner in runners)

                for i in range(max_length):
                    update = []
                    for runner in runners:
                        progress = (
                            runner["progress"][i]
                            if i < len(runner["progress"])
                            else runner["progress"][-1]
                        )
                        update.append(
                            {
                                "runner_id": runner["runner_id"],
                                "time": runner["time"],
                                "current_progress": progress,
                                "finished": i >= len(runner["progress"]) - 1,
                            }
                        )

                    await sio.emit(
                        "race_update", {"race_id": current_race_id, "runners": update}
                    )
                    await asyncio.sleep(0.1)

                logger.info(
                    f"Finished sending data for race {current_race_id}, pausing for 5 seconds"
                )
                await asyncio.sleep(5)

            except json.JSONDecodeError:
                logger.error(f"Error decoding JSON for race {current_race_id}")
            except Exception as e:
                logger.error(f"Error processing race data: {e!s}")

        except Exception as e:
            logger.error(f"Error in main loop: {e!s}")

        logger.info("Waiting 30 seconds before checking for new race...")
        await asyncio.sleep(30)


def start_race():
    race_thread = Thread(target=lambda: asyncio.run(send_race_data()))
    race_thread.daemon = True
    race_thread.start()


if __name__ == "__main__":
    start_race()
    uvicorn.run(app, host="0.0.0.0", port=8000)
