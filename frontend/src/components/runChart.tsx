import { Bar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    BarElement,
    Title,
    ChartOptions
} from 'chart.js';
import '../sass/components/_all.scss';
import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';
import { Runner, RaceUpdateData } from "../types/runners.ts";

ChartJS.register(CategoryScale, LinearScale, PointElement, BarElement, Title);

const options: ChartOptions<'bar'> = {
    responsive: true,
    indexAxis: 'y',
    plugins: {
        title: {
            display: true,
            text: 'Визуализация забега',
            color: '#FFFFFF',
            font: {
                size: 15,
                weight: 'bold' as const,
            }
        },
        tooltip: {
            callbacks: {
                label: (context) => `${context.dataset.label}: ${context.raw}%`,
            }
        }
    },
    scales: {
        y: {
            min: 0,
            max: 100,
        },
        x: {
            title: {
                display: true,
                text: 'Прогресс (%)'
            }
        }
    }
};

const labels = [
    'Ученик 1',
    'Ученик 2',
    'Ученик 3',
    'Ученик 4',
    'Ученик 5',
    'Ученик 6',
];

const initialData = {
    labels,
    datasets: [
        {
            data: Array(labels.length).fill(0),
            backgroundColor: [
                '#FA5252',
                '#5C7CFA',
                '#FCC419',
                '#94D82D',
                '#CC5DE8',
                'rgba(0,0,0,0.6)',
            ],
            borderRadius: 8,
            barThickness: 20,
        }
    ]
};

export const RunChart = () => {
    const [chartData, setChartData] = useState(initialData);
    const [raceId, setRaceId] = useState<string | null>(null);
    const [streamDuration, setStreamDuration] = useState<number | null>(null);
    const [nextStream, setNextStream] = useState<number | null>(null);

    useEffect(() => {
        const socket = io('https://fvbit.ru');

        socket.on('race_update', (data) => {
            if (data.stream_complete) {
                setStreamDuration(data.stream_duration);
                setNextStream(Math.round(data.next_stream_in));
                return;
            }

            setRaceId(data.race_id);
            setStreamDuration(null);
            setNextStream(null);

            setChartData(prev => {
                const newData = [...prev.datasets[0].data];

                (data as RaceUpdateData).runners.forEach((runner: Runner) => {
                    const runnerIndex = runner.runner_id - 1;
                    if (runnerIndex >= 0 && runnerIndex < newData.length) {
                        newData[runnerIndex] = runner.current_progress;
                    }
                });

                return {
                    ...prev,
                    datasets: [{
                        ...prev.datasets[0],
                        data: newData
                    }]
                };
            });
        });

        return () => {
            socket.disconnect();
        };
    }, []);

    useEffect(() => {
        let interval: ReturnType<typeof setInterval>;
        if (nextStream !== null && nextStream > 0) {
            interval = setInterval(() => {
                setNextStream((prev) => (prev !== null && prev > 0 ? prev - 1 : 0));
            }, 1000);
        }
        return () => clearInterval(interval);
    }, [nextStream]);

    return (
        <div>
            {raceId && <div className="currentRun">Текущий забег: {raceId}</div>}

            {streamDuration !== null && nextStream !== null && (
                <div className="stream-info">
                    Длительность забега: <strong>{streamDuration.toFixed(2)} секунд</strong> |
                    Следующий забег через: <strong>{nextStream} секунд</strong>
                </div>
            )}

            <Bar
                width={600}
                height={300}
                options={options}
                data={chartData}
            />
        </div>
    );
};