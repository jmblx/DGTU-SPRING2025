import { useState, useEffect } from 'react';
import { RacesData, ProcessedRace } from "../types/raceResult.ts";
import { shirts } from "../types/tshirts.ts";

const StatisticsTable = () => {
    const [processedRaces, setProcessedRaces] = useState<ProcessedRace[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [chartImages, setChartImages] = useState<Record<string, string>>({});
    const [hoveredRace, setHoveredRace] = useState<string | null>(null);

    const fetchChartImage = async (raceId: string) => {
        try {
            const response = await fetch(`https://fvbit.ru/api/v1/races/races/${raceId}/chart`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const img = doc.querySelector('img');
            const src = img?.getAttribute('src') || '';

            setChartImages(prev => ({
                ...prev,
                [raceId]: src
            }));
        } catch (err) {
            console.error(`Failed to fetch chart for race ${raceId}:`, err);
        }
    };

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

    const last10Races = processedRaces.slice(0, 10);

    if (loading) return <div>Loading statistics...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div>
            <table className="home__statistics--table" cellSpacing="2" cellPadding="12">
                <caption>Статистика</caption>
                <thead>
                <tr>
                    <th></th>
                    {last10Races.map(race => (
                        <th

                            key={race.raceId}
                        >
                            <span
                                style={{ "textDecoration": 'underline', "cursor": 'pointer'}}
                                onMouseEnter={() => {
                                    setHoveredRace(race.raceId);
                                    if (!chartImages[race.raceId]) {
                                        fetchChartImage(race.raceId);
                                    }
                                }}
                                onMouseLeave={() => setHoveredRace(null)}
                            >
                                Забег {race.raceId}
                            </span>
                        </th>
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
                                <td
                                    key={`${race.raceId}-${position}`}
                                >
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

            {hoveredRace && chartImages[hoveredRace] && (
                <div style={{
                    position: 'fixed',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-105%, -110%)',
                    zIndex: 1000,
                    backgroundColor: 'white',
                    padding: '10px',
                    borderRadius: '5px',
                    boxShadow: '0 0 10px rgba(0,0,0,0.5)'
                }}>
                    <img
                        src={chartImages[hoveredRace]}
                        alt={`Chart for race ${hoveredRace}`}
                        style={{ maxWidth: '600px', maxHeight: '400px' }}
                    />
                    <div style={{ textAlign: 'center', marginTop: '5px' }}>График забега {hoveredRace}</div>
                </div>
            )}
        </div>
    );
};

export default StatisticsTable;