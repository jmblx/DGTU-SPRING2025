import { useState, useEffect } from 'react';
import { ProbabilitiesResponse, PositionProbabilities } from "../types/positionProbabilities.ts";

const ProbabilityTable = () => {
    const [probabilities, setProbabilities] = useState<PositionProbabilities>({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchProbabilities = async () => {
            try {
                const response = await fetch('https://fvbit.ru/api/v1/probabilities');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data: ProbabilitiesResponse = await response.json();
                setProbabilities(data.position_probabilities);
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

    const runnerIds = Object.keys(probabilities);

    return (
        <table cellSpacing="2" cellPadding="12" className="home__threads--table">
            <caption>Таблица вероятности по местам</caption>
            <tbody>
            <tr className="home__threads--places">
                <td className="first">1</td>
                <td className="second">2</td>
                <td className="third">3</td>
                <td>4</td>
                <td>5</td>
                <td>6</td>
            </tr>

            {runnerIds.map((runnerId) => {
                const runnerProbs = probabilities[runnerId];
                return (
                    <tr key={runnerId}>
                        <td>{runnerProbs.position_1.toFixed(2)}</td>
                        <td>{runnerProbs.position_2.toFixed(2)}</td>
                        <td>{runnerProbs.position_3.toFixed(2)}</td>
                        <td>{runnerProbs.position_4.toFixed(2)}</td>
                        <td>{runnerProbs.position_5.toFixed(2)}</td>
                        <td>{runnerProbs.position_6.toFixed(2)}</td>
                    </tr>
                );
            })}
            </tbody>
        </table>
    );
};

export default ProbabilityTable;