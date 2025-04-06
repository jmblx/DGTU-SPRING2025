import { useState, useEffect } from 'react';
import { TopProbabilities, ProbabilitiesTopResponse} from '../types/positionProbabilities.ts'

const TopProbabilitiesTable = () => {
    const [top2Probs, setTop2Probs] = useState<TopProbabilities>({});
    const [top3Probs, setTop3Probs] = useState<TopProbabilities>({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchProbabilities = async () => {
            try {
                const response = await fetch('https://fvbit.ru/api/v1/probabilities');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data: ProbabilitiesTopResponse = await response.json();
                setTop2Probs(data.top2_probabilities);
                setTop3Probs(data.top3_probabilities);
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

    const runnerIds = Object.keys(top2Probs);

    return (
        <table cellSpacing="2" cellPadding="12" className="home__threads--table">
            <caption>Вероятность попадания в топ 2 или топ 3</caption>
            <tbody>
            <tr className="home__threads--places">
                <td className="first">1</td>
                <td className="second">2</td>
                <td style={{ border: "none" }}>&nbsp;</td>
                <td className="first">1</td>
                <td className="second">2</td>
                <td className="third">3</td>
            </tr>

            {runnerIds.map((runnerId) => (
                <tr key={runnerId}>
                    <td>{top2Probs[runnerId]?.toFixed(2) || '0.00'}</td>
                    <td>{top2Probs[runnerId]?.toFixed(2) || '0.00'}</td>
                    <td style={{ border: "none" }}></td>

                    <td>{top3Probs[runnerId]?.toFixed(2) || '0.00'}</td>
                    <td>{top3Probs[runnerId]?.toFixed(2) || '0.00'}</td>
                    <td>{top3Probs[runnerId]?.toFixed(2) || '0.00'}</td>
                </tr>
            ))}
            </tbody>
        </table>
    );
};

export default TopProbabilitiesTable;