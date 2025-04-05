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


# Создаем единственный экземпляр RaceStreamer
race_streamer = RaceStreamer()


@app.get("/", response_class=HTMLResponse)
async def get():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Race Simulation</title>
        <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
        <style>
            .race-info {
                margin-bottom: 20px;
                padding: 10px;
                background-color: #f0f0f0;
                border-radius: 5px;
            }
            .runner {
                margin: 10px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            .progress-container {
                width: 100%;
                background-color: #f1f1f1;
                border-radius: 5px;
                margin-top: 5px;
            }
            .progress-bar {
                height: 20px;
                border-radius: 5px;
                background-color: #4CAF50;
                text-align: center;
                line-height: 20px;
                color: white;
            }
            .finished {
                background-color: #2196F3;
            }
            .waiting {
                padding: 20px;
                text-align: center;
                font-size: 1.2em;
                color: #666;
            }
            .stream-info {
                margin-top: 20px;
                padding: 15px;
                background-color: #e9f7ef;
                border-radius: 5px;
                font-size: 1.1em;
            }
            .countdown {
                font-weight: bold;
                color: #2e7d32;
            }
        </style>
    </head>
    <body>
        <h1>Live Race Updates</h1>
        <div id="race-info" class="race-info">
            Current race: <span id="current-race-id">-</span>
        </div>
        <div id="runners-container"></div>
        <div id="stream-info" class="stream-info" style="display: none;">
            Stream duration: <span id="stream-duration">0</span>s | 
            Next stream in: <span id="next-stream" class="countdown">0</span>s
        </div>
        <div id="waiting-message" class="waiting" style="display: none;">
            Waiting for next race data...
        </div>

        <script>
            const socket = io('http://localhost:8000');
            const runnersContainer = document.getElementById('runners-container');
            const currentRaceIdElement = document.getElementById('current-race-id');
            const waitingMessage = document.getElementById('waiting-message');
            const streamInfo = document.getElementById('stream-info');
            const streamDurationElement = document.getElementById('stream-duration');
            const nextStreamElement = document.getElementById('next-stream');

            let runners = {};
            let currentRaceId = null;
            let countdownInterval = null;

            function startCountdown(seconds) {
                if (countdownInterval) clearInterval(countdownInterval);

                let remaining = Math.round(seconds);
                nextStreamElement.textContent = remaining;

                countdownInterval = setInterval(() => {
                    remaining -= 1;
                    if (remaining >= 0) {
                        nextStreamElement.textContent = remaining;
                    } else {
                        clearInterval(countdownInterval);
                    }
                }, 1000);
            }

            // Очистка бегунов при новой гонке
            socket.on('clear_runners', () => {
                runnersContainer.innerHTML = '';
                runners = {};
            });

            socket.on('race_update', (data) => {
                if (data.stream_complete) {
                    // Показываем информацию о стриме и времени до следующего
                    streamInfo.style.display = 'block';
                    streamDurationElement.textContent = data.stream_duration.toFixed(2);
                    startCountdown(data.next_stream_in);
                    return;
                }

                // Если это новая гонка, обновляем ID
                if (data.race_id !== currentRaceId) {
                    currentRaceId = data.race_id;
                    currentRaceIdElement.textContent = data.race_id;
                    waitingMessage.style.display = 'none';
                    streamInfo.style.display = 'none';
                }

                data.runners.forEach(runner => {
                    if (!runners[runner.runner_id]) {
                        const runnerDiv = document.createElement('div');
                        runnerDiv.className = 'runner';
                        runnerDiv.id = `runner-${runner.runner_id}`;
                        runnerDiv.innerHTML = `
                            <h3>Runner ${runner.runner_id}</h3>
                            <p>Time: <span class="time">${runner.time.toFixed(2)}</span>s</p>
                            <div class="progress-container">
                                <div class="progress-bar" style="width: ${runner.current_progress}%">
                                    ${runner.current_progress.toFixed(1)}%
                                </div>
                            </div>
                            <p class="status">${runner.finished ? 'Finished!' : 'Running...'}</p>
                        `;
                        runnersContainer.appendChild(runnerDiv);
                        runners[runner.runner_id] = runnerDiv;
                    } else {
                        const runnerDiv = runners[runner.runner_id];
                        runnerDiv.querySelector('.progress-bar').style.width = `${runner.current_progress}%`;
                        runnerDiv.querySelector('.progress-bar').textContent = `${runner.current_progress.toFixed(1)}%`;
                        runnerDiv.querySelector('.time').textContent = runner.time.toFixed(2);

                        if (runner.finished) {
                            runnerDiv.querySelector('.progress-bar').classList.add('finished');
                            runnerDiv.querySelector('.status').textContent = 'Finished!';
                        }
                    }
                });
            });

            // Показываем сообщение о ожидании между гонками
            setInterval(() => {
                if (!currentRaceId) {
                    waitingMessage.style.display = 'block';
                }
            }, 5000);
        </script>
    </body>
    </html>
    """
    return html_content


def start_race():
    race_thread = Thread(target=lambda: asyncio.run(race_streamer.send_race_data()))
    race_thread.daemon = True
    race_thread.start()


if __name__ == "__main__":
    start_race()
    uvicorn.run(app, host="0.0.0.0", port=8000)
