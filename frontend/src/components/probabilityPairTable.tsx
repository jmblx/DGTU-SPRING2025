import { useState, useEffect } from 'react';
import tshirtRed from '../assets/tshirtRed.png';
import tshirtBlue from '../assets/tshirtBlue.png';
import tshirtYellow from '../assets/tshirtYellow.png';
import tshirtGreen from '../assets/tshirtGreen.png';
import tshirtViolet from '../assets/tshirtViolet.png';
import tshirtBlack from '../assets/tshirtBlack.png';

type RunnerId = '1' | '2' | '3' | '4' | '5' | '6';

interface PairMatrix {
    [runnerId: string]: {
        [opponentId: string]: number | null;
    };
}

const PairProbabilityTable = () => {
    const [pairMatrix, setPairMatrix] = useState<PairMatrix>({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const shirtImages: Record<RunnerId, string> = {
        '1': tshirtRed,
        '2': tshirtBlue,
        '3': tshirtYellow,
        '4': tshirtGreen,
        '5': tshirtViolet,
        '6': tshirtBlack
    };

    const runnerIds: RunnerId[] = ['1', '2', '3', '4', '5', '6'];

    useEffect(() => {
        const fetchProbabilities = async () => {
            try {
                const response = await fetch('https://fvbit.ru/api/v1/probabilities');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                setPairMatrix(data.pair_matrix);
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

        fetchProbabilities();
    }, []);

    if (loading) return <div>Loading probabilities...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <table cellSpacing="2" cellPadding="12" className="home__threads--table">
            <caption>Вероятность занятия 1-го и 2-го мест</caption>
            <tbody>
            <tr className="home__threads--shirts">
                {runnerIds.map(id => (
                    <td key={`header-${id}`}>
                        <img src={shirtImages[id]} alt={`Футболка ${id}`} style={{ width: 30 }} />
                    </td>
                ))}
            </tr>

            {runnerIds.map(rowRunnerId => (
                <tr key={`row-${rowRunnerId}`}>
                    {runnerIds.map(colRunnerId => {
                        if (rowRunnerId === colRunnerId) {
                            return <td key={`${rowRunnerId}-${colRunnerId}`}>-</td>;
                        }

                        const probability = pairMatrix[rowRunnerId]?.[`runner_${colRunnerId}`];
                        const displayValue = probability !== null ? probability.toFixed(4) : '-';

                        return (
                            <td key={`${rowRunnerId}-${colRunnerId}`}>
                                {displayValue}
                            </td>
                        );
                    })}
                </tr>
            ))}
            </tbody>
        </table>
    );
};

export default PairProbabilityTable;