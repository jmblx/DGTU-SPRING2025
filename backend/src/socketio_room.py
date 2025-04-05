import asyncio
import json
import logging
import time
from threading import Thread

import socketio
import uvicorn
from fastapi import FastAPI
from redis.asyncio import Redis
from socketio import AsyncServer
from starlette.responses import HTMLResponse

from core.config import config_loader

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

sio = AsyncServer(cors_allowed_origins="*", async_mode="asgi")
app.mount("/socket.io", socketio.ASGIApp(sio))

redis_client = Redis.from_url(config_loader.app_config.redis.uri)

logger = logging.getLogger(__name__)


class RaceStreamer:
    def __init__(self):
        self.last_race_id = None
        self.stream_duration = 0

    async def send_race_data(self):
        while True:
            try:
                current_race_id = await redis_client.get("current_race_id")
                if not current_race_id:
                    logger.info("No current race ID found, waiting...")
                    await asyncio.sleep(0.1)
                    continue

                current_race_id = current_race_id.decode("utf-8")

                # Если гонка уже обрабатывалась, пропускаем
                if current_race_id == self.last_race_id:
                    await asyncio.sleep(0.1)
                    continue

                logger.info(f"Processing race ID: {current_race_id}")
                race_data = await redis_client.get(f"race:{current_race_id}:results")

                if not race_data:
                    logger.info(f"No data found for race {current_race_id}")
                    await asyncio.sleep(0.1)
                    continue

                try:
                    start_time = time.time()
                    runners: list[dict] = json.loads(race_data)
                    max_length = max(len(runner["progress"]) for runner in runners)

                    await sio.emit("clear_runners")

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
                            "race_update",
                            {
                                "race_id": current_race_id,
                                "runners": update,
                                "stream_complete": False,
                            },
                        )
                        await asyncio.sleep(0.07)

                    self.stream_duration = time.time() - start_time
                    remaining_time = max(0, 25 - self.stream_duration - 0.1)

                    await sio.emit(
                        "race_update",
                        {
                            "race_id": current_race_id,
                            "runners": [],
                            "stream_complete": True,
                            "next_stream_in": remaining_time,
                            "stream_duration": self.stream_duration,
                        },
                    )

                    logger.info(
                        f"Finished sending data for race {current_race_id}. "
                        f"Stream duration: {self.stream_duration:.2f}s. "
                        f"Next stream in: {remaining_time:.2f}s"
                    )

                    self.last_race_id = current_race_id

                    # Ждем оставшееся время до следующего стрима
                    await asyncio.sleep(remaining_time)

                except json.JSONDecodeError:
                    logger.error(f"Error decoding JSON for race {current_race_id}")
                except Exception as e:
                    logger.error(f"Error processing race data: {e!s}")

            except Exception as e:
                logger.error(f"Error in main loop: {e!s}")
                await asyncio.sleep(0.1)


race_streamer = RaceStreamer()


def start_race():
    race_thread = Thread(target=lambda: asyncio.run(race_streamer.send_race_data()))
    race_thread.daemon = True
    race_thread.start()


if __name__ == "__main__":
    start_race()
    uvicorn.run(app, host="0.0.0.0", port=8000)
