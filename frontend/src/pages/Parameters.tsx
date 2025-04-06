import { useEffect, useState } from 'react';
import tshirtRed from "../assets/tshirtRed.png";
import tshirtBlue from "../assets/tshirtBlue.png";
import tshirtYellow from "../assets/tshirtYellow.png";
import tshirtGreen from "../assets/tshirtGreen.png";
import tshirtViolet from "../assets/tshirtViolet.png";
import tshirtBlack from "../assets/tshirtBlack.png";
import { IHyperParams } from "../types/hyperParams.ts";
import '../sass/components/_all.scss';

export const Parameters = () => {
    const runnerIds = [1, 2, 3, 4, 5, 6];
    const tshirts = [tshirtRed, tshirtBlue, tshirtYellow, tshirtGreen, tshirtViolet, tshirtBlack];
    const [runners, setRunners] = useState<IHyperParams[]>([]);
    const [isEditing, setIsEditing] = useState<number | null>(null);
    const [editValues, setEditValues] = useState<IHyperParams | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        const fetchRunners = async () => {
            setIsLoading(true);
            setError(null);

            try {
                const response = await fetch('https://fvbit.ru/api/v1/runners');

                if (!response.ok) {
                    throw new Error(`Ошибка загрузки: ${response.status}`);
                }

                const data: IHyperParams[] = await response.json();
                setRunners(data.sort((a, b) => a.runner_id - b.runner_id));
            } catch (err) {
                console.error("Ошибка:", err);
                setError("Не удалось загрузить данные бегунов");
            } finally {
                setIsLoading(false);
            }
        };

        fetchRunners();
    }, []);

    const updateRunner = async (id: number) => {
        if (!editValues) return;

        setIsLoading(true);
        setError(null);

        try {
            const response = await fetch(`https://fvbit.ru/api/v1/runners/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(editValues)
            });

            if (!response.ok) {
                throw new Error(`Ошибка обновления: ${response.status}`);
            }

            const updatedRunner = await response.json();

            setRunners(prev =>
                prev.map(runner =>
                    runner.runner_id === id ? updatedRunner : runner
                )
            );

            setIsEditing(null);
            setEditValues(null);
        } catch (err) {
            console.error("Ошибка:", err);
            setError("Ошибка при сохранении изменений");
        } finally {
            setIsLoading(false);
        }
    };

    const startEditing = (id: number) => {
        const runner = runners.find(r => r.runner_id === id);
        if (runner) {
            setEditValues({ ...runner });
            setIsEditing(id);
        }
    };

    const handleChange = (field: keyof IHyperParams, value: string) => {
        if (!editValues) return;

        setEditValues({
            ...editValues,
            [field]: value ? parseFloat(value) : 0
        });
    };

    if (isLoading && runners.length === 0) {
        return <div className="loading">Загрузка данных...</div>;
    }

    return (
        <div className="parameters-container">
            {error && <div className="error-message">{error}</div>}

            <table cellSpacing="2" cellPadding="5" className="params-table">
                <thead>
                <tr>
                    <th></th>
                    <th>Время реакции</th>
                    <th>Ускорение</th>
                    <th>Макс. скорость</th>
                    <th>Потеря скорости</th>
                    <th>Действия</th>
                </tr>
                </thead>
                <tbody>
                {runnerIds.map((id, idx) => {
                    const runner = runners.find(r => r.runner_id === id);
                    const isCurrentEditing = isEditing === id;

                    return (
                        <tr key={id}>
                            <td>
                                <img
                                    src={tshirts[idx]}
                                    alt={`Бегун ${id}`}
                                    className="runner-icon"
                                />
                            </td>

                            {isCurrentEditing ? (
                                <>
                                    <td>
                                        <input
                                            type="number"
                                            step="0.01"
                                            min="0.1"
                                            max="0.3"
                                            value={editValues?.reaction_time ?? 0}
                                            onChange={(e) => handleChange('reaction_time', e.target.value)}
                                        />
                                    </td>
                                    <td>
                                        <input
                                            type="number"
                                            step="0.01"
                                            min="2"
                                            max="10"
                                            value={editValues?.acceleration ?? 0}
                                            onChange={(e) => handleChange('acceleration', e.target.value)}
                                        />
                                    </td>
                                    <td>
                                        <input
                                            type="number"
                                            step="0.01"
                                            min="7"
                                            max="12"
                                            value={editValues?.max_speed ?? 0}
                                            onChange={(e) => handleChange('max_speed', e.target.value)}
                                        />
                                    </td>
                                    <td>
                                        <input
                                            type="number"
                                            step="0.01"
                                            min="0.05"
                                            max="0.5"
                                            value={editValues?.speed_decay ?? 0}
                                            onChange={(e) => handleChange('speed_decay', e.target.value)}
                                        />
                                    </td>
                                    <td>
                                        <button
                                            onClick={() => updateRunner(id)}
                                            disabled={isLoading}
                                            className="params-table--save"
                                        >
                                            {isLoading ? 'Сохранение...' : 'Сохранить'}
                                        </button>
                                        <button
                                            onClick={() => setIsEditing(null)}
                                            disabled={isLoading}
                                            className="params-table--cancel"
                                        >
                                            Отмена
                                        </button>
                                    </td>
                                </>
                            ) : (
                                <>
                                    <td>{runner?.reaction_time?.toFixed(2) ?? '-'}</td>
                                    <td>{runner?.acceleration?.toFixed(2) ?? '-'}</td>
                                    <td>{runner?.max_speed?.toFixed(2) ?? '-'}</td>
                                    <td>{runner?.speed_decay?.toFixed(2) ?? '-'}</td>
                                    <td>
                                        <button
                                            className="params-table--button"
                                            onClick={() => startEditing(id)}
                                        >
                                            Изменить
                                        </button>
                                    </td>
                                </>
                            )}
                        </tr>
                    );
                })}
                </tbody>
            </table>
        </div>
    );
};