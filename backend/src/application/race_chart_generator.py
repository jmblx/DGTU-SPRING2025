import logging
import matplotlib.pyplot as plt
import io
import base64
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from infrastructure.db.models import Race, RaceResult, Runner


class RaceChartGenerator:
    COLOR_TRANSLATIONS = {
        "красный": "red",
        "синий": "blue",
        "зелёный": "green",
        "фиолетовый": "purple",
        "чёрный": "black",
        "жёлтый": "yellow"
    }

    def __init__(self, session: AsyncSession):
        self.session = session

    async def generate_race_chart(self, race_id: int) -> str:
        """Генерирует график результатов гонки в base64"""
        try:
            query = (
                select(RaceResult, Runner)
                .join(Runner, RaceResult.runner_id == Runner.id)
                .where(RaceResult.race_id == race_id)
                .order_by(RaceResult.position)
            )

            result = await self.session.execute(query)
            results = result.all()

            if not results:
                return ""

            runners = []
            times = []
            colors = []

            for race_result, runner in results:
                runners.append(f"Runner {runner.id}")
                times.append(race_result.finish_time)
                # Переводим цвет
                color = self.COLOR_TRANSLATIONS.get(runner.colour.lower(), "gray")
                colors.append(color)

            plt.figure(figsize=(10, 6))
            bars = plt.barh(runners, times, color=colors)

            plt.bar_label(bars, fmt='%.2f s', padding=3)
            plt.title(f"Race #{race_id} Results")
            plt.xlabel("Finish Time (seconds)")
            plt.tight_layout()

            # Конвертируем в base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            plt.close()

            return base64.b64encode(buffer.read()).decode('utf-8')

        except Exception as e:
            logging.error(f"Error generating chart: {e}")
            return ""

    async def generate_history_chart(self, runner_id: int) -> str:
        """Генерирует график истории результатов бегуна"""
        results = await self.session.execute(
            select(RaceResult)
            .where(RaceResult.runner_id == runner_id)
            .join(Race)
            .order_by(Race.start_time)
            .limit(10)
        )
        results = results.scalars().all()

        if not results:
            return ""

        race_ids = []
        positions = []
        times = []

        for result in results:
            race_ids.append(f"Race {result.race.id}")
            positions.append(result.position)
            times.append(result.finish_time)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

        ax1.plot(race_ids, times, 'o-', color='blue')
        ax1.set_title(f"Runner {runner_id} Performance History")
        ax1.set_ylabel("Finish Time (s)")
        ax1.grid(True)

        ax2.plot(race_ids, positions, 'o-', color='red')
        ax2.set_ylabel("Position")
        ax2.grid(True)
        ax2.invert_yaxis()

        plt.xticks(rotation=45)
        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        return base64.b64encode(buffer.read()).decode('utf-8')
