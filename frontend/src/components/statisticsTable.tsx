import { useState, useEffect } from 'react';
import { RacesData, ProcessedRace } from "../types/raceResult.ts";
import { shirts } from "../types/tshirts.ts";

const StatisticsTable = () => {
    const [processedRaces, setProcessedRaces] = useState<ProcessedRace[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchLastRaces = async () => {
            try {
                const response = await fetch('https://fvbit.ru/api/v1/races/last');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data: RacesData = await response.json();

                const racesArray: ProcessedRace[] = Object.entries(data.races).map(
                    ([raceId, results]) => ({
                        raceId,
                        results: Object.entries(results).map(([runnerId, position]) => ({
                            runnerId,
                            position,
                        }))
                    })
                );

                setProcessedRaces(racesArray);
            } catch (err) {
                if (err instanceof Error) {
                    setError(err.message);
                } else {
                    setError('An unknown error occurred');
                }
            } finally {
                setLoading(false);
            }
        };

        fetchLastRaces();

        const intervalId = setInterval(fetchLastRaces, 4000);

        return () => clearInterval(intervalId);
    }, []);

    if (loading) return <div>Loading statistics...</div>;
    if (error) return <div>Error: {error}</div>;

    const last10Races = processedRaces.slice(0, 10);

    return (
        <table className="home__statistics--table" cellSpacing="2" cellPadding="12">
            <caption>Статистика</caption>
            <thead>
            <tr>
                <th></th>
                {last10Races.map(race => (
                    <th key={race.raceId}>Забег {race.raceId}</th>
                ))}
            </tr>
            </thead>
            <tbody>
            {[1, 2, 3, 4, 5, 6].map(position => (
                <tr key={position}>
                    <td className={
                        position === 1 ? "first" :
                            position === 2 ? "second" :
                                position === 3 ? "third" : ""
                    }>
                        {position}
                    </td>
                    {last10Races.map(race => {
                        const result = race.results.find(r => r.position === position);
                        const shirt = result ? shirts.find(s => s.id.toString() === result.runnerId) : null;

                        return (
                            <td key={`${race.raceId}-${position}`}>
                                {shirt ? (
                                    <img
                                        src={shirt.src}
                                        alt={`${shirt.name}`}
                                        style={{width: 30}}
                                        title={`${shirt.name}`}
                                    />
                                ) : '-'}
                            </td>
                        );
                    })}
                </tr>
            ))}
            </tbody>
        </table>
    );
};

export default StatisticsTable;