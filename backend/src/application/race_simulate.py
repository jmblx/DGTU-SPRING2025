import asyncio
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional

from redis.asyncio import Redis
from socketio import AsyncServer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.models import Race, Runner, RaceResult

logger = logging.getLogger(__name__)

class RaceSimulator:
    def __init__(self, session: AsyncSession, redis: Redis, sio: AsyncServer):
        self.session = session
        self.redis = redis
        self.sio = sio
        self.time_step = 0.1  # Шаг симуляции в секундах

    async def create_race(self) -> Race:
        """Создает новую запись о забеге в БД"""
        race = Race(start_time=datetime.utcnow())
        self.session.add(race)
        await self.session.commit()
        return race

    async def simulate_race(self, race_id: int, runners: Optional[List[Runner]] = None):
        """Основной метод симуляции забега"""
        if runners is None:
            runners = await self._get_runners()

        race = await self.session.get(Race, race_id)
        if not race:
            raise ValueError(f"Race {race_id} not found")

        # Инициализация Redis
        redis_key = f"race:{race_id}"
        await self.redis.delete(redis_key)  # Очищаем предыдущие данные

        # Подготовка данных для симуляции
        race_data = {
            "status": "running",
            "start_time": race.start_time.isoformat(),
            "runners": {runner.id: self._runner_to_dict(runner) for runner in runners},
            "progress": {}
        }
        await self._update_redis(redis_key, race_data)

        # Основной цикл симуляции
        t = 0.0
        finished = {runner.id: False for runner in runners}
        positions = {runner.id: 0.0 for runner in runners}

        while not all(finished.values()):
            for runner in runners:
                if finished[runner.id]:
                    continue

                # Расчет новой позиции
                new_pos = self._calculate_position(runner, t)
                positions[runner.id] = new_pos

                # Фиксация финиша
                if new_pos >= 100:
                    finished[runner.id] = True
                    positions[runner.id] = 100.0
                    await self._save_finish_result(race, runner, t)

            # Сохранение прогресса
            race_data["progress"][t] = positions.copy()
            await self._update_redis(redis_key, race_data)

            # Отправка обновления через Socket.IO
            if self.sio:
                await self.sio.emit('race_update', {
                    'race_id': race_id,
                    'time': t,
                    'positions': positions
                })

            t += self.time_step
            await asyncio.sleep(0.1)  # Для реалистичной симуляции

        # Финализация забега
        race.end_time = datetime.utcnow()
        await self.session.commit()
        race_data["status"] = "finished"
        await self._update_redis(redis_key, race_data)

    async def _get_runners(self) -> List[Runner]:
        """Получает список бегунов из БД"""
        result = await self.session.execute(select(Runner))
        return result.scalars().all()

    def _calculate_position(self, runner: Runner, time: float) -> float:
        """Вычисляет текущую позицию бегуна"""
        t_eff = max(0.0, time - float(runner.reaction_time))
        accel = float(runner.acceleration)
        max_v = float(runner.max_speed)
        decay = float(runner.speed_decay)

        if t_eff < max_v / accel:
            speed = accel * t_eff
        else:
            t_decay = t_eff - (max_v / accel)
            speed = max_v * (1 - decay * t_decay)
            speed = max(speed, 3.0)

        return min(100.0, speed * self.time_step)

    async def _save_finish_result(self, race: Race, runner: Runner, finish_time: float):
        """Сохраняет результат финиша в БД"""
        result = RaceResult(
            race_id=race.id,
            runner_id=runner.id,
            finish_time=finish_time,
            position=sum(1 for r in race.results) + 1
        )
        self.session.add(result)

    def _runner_to_dict(self, runner: Runner) -> Dict:
        """Конвертирует объект Runner в словарь"""
        return {
            "id": runner.id,
            "color": runner.colour,
            "reaction_time": float(runner.reaction_time),
            "acceleration": float(runner.acceleration),
            "max_speed": float(runner.max_speed),
            "speed_decay": float(runner.speed_decay)
        }

    async def _update_redis(self, key: str, data: Dict):
        """Обновляет данные в Redis"""
        await self.redis.set(key, json.dumps(data))
        await self.redis.expire(key, 86400)  # Храним 24 часа