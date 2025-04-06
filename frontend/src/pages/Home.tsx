import React, {useEffect, useState} from 'react';
import tshirtRed from '../assets/tshirtRed.png'
import tshirtBlue from '../assets/tshirtBlue.png'
import tshirtYellow from '../assets/tshirtYellow.png'
import tshirtGreen from '../assets/tshirtGreen.png'
import tshirtViolet from '../assets/tshirtViolet.png'
import tshirtBlack from '../assets/tshirtBlack.png'
import {RunChart} from "../components/runChart.tsx";
import { Divider, Skeleton } from "@mui/material";
import { shirts } from "../types/tshirts.ts";
import '../sass/app.scss';
import StatisticsTable from "../components/statisticsTable.tsx";
import ProbabilityTable from "../components/probabilityTable.tsx";
import TopProbabilitiesTable from "../components/probabilityTopTable.tsx";
import PairProbabilityTable from "../components/probabilityPairTable.tsx";

const Home: React.FC = () => {
    const [tooltipPos] = useState<{ x: number; y: number } | null>(null);
    const [hoveredCol] = useState<number | null>(null);

    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const timeout = setTimeout(() => {
            setLoading(false);
        });

        return () => clearTimeout(timeout);
    }, []);

    return (
        <div className="wrapper">
            <div className="container">
                <div className="home">
                    {loading ? (
                        <Skeleton variant="rectangular" width={50} height={350} animation="wave"></Skeleton>
                    ) : (
                        <table cellSpacing="2" cellPadding="2">
                            <tbody>
                            <tr>
                                <td className="transpanent">
                                    <img src={tshirtRed} alt=""/>
                                </td>
                            </tr>
                            <tr>
                                <td><img src={tshirtRed} alt=""/></td>
                            </tr>
                            <tr>
                                <td><img src={tshirtBlue} alt=""/></td>
                            </tr>
                            <tr>
                                <td><img src={tshirtYellow} alt=""/></td>
                            </tr>
                            <tr>
                                <td><img src={tshirtGreen} alt=""/></td>
                            </tr>
                            <tr>
                                <td><img src={tshirtViolet} alt=""/></td>
                            </tr>
                            <tr>
                                <td><img src={tshirtBlack} alt=""/></td>
                            </tr>
                            </tbody>
                        </table>
                    )
                    }
                    <Divider orientation="vertical" flexItem sx={{backgroundColor: 'white'}}/>
                    <div className="home__threads">
                        {loading ? (
                            <Skeleton variant="rectangular" width={350} height={350} animation="wave"></Skeleton>
                        ) : (
                            <ProbabilityTable />
                            )
                        }
                    </div>
                    <Divider orientation="vertical" flexItem sx={{backgroundColor: 'white'}}/>
                    <div className="home__threads--top">
                        {loading ? (
                            <Skeleton variant="rectangular" width={350} height={350} animation="wave"></Skeleton>
                        ) : (
                            <TopProbabilitiesTable />
                            )
                        }
                    </div>
                    <Divider orientation="vertical" flexItem sx={{backgroundColor: 'white'}}/>
                    <div className="home__threads--leaders">
                        {loading ? (
                            <Skeleton variant="rectangular" width={350} height={350} animation="wave"></Skeleton>
                        ) : (
                            <PairProbabilityTable />
                            )
                        }
                    </div>
                    <Divider orientation="vertical" flexItem sx={{backgroundColor: "white"}}/>
                    <table cellSpacing="2" cellPadding="2">
                        <tbody>
                        <tr>
                            <td className="transpanent">
                                <img src={tshirtRed} alt=""/>
                            </td>
                        </tr>
                        <tr>
                            <td><img src={tshirtRed} alt=""/></td>
                        </tr>
                        <tr>
                            <td><img src={tshirtBlue} alt=""/></td>
                        </tr>
                        <tr>
                            <td><img src={tshirtYellow} alt=""/></td>
                        </tr>
                        <tr>
                            <td><img src={tshirtGreen} alt=""/></td>
                        </tr>
                        <tr>
                            <td><img src={tshirtViolet} alt=""/></td>
                        </tr>
                        <tr>
                            <td><img src={tshirtBlack} alt=""/></td>
                        </tr>
                        </tbody>
                    </table>
                </div>
                <div className="home__analytics">
                    <div className="home__statistics">
                        {loading ? (
                            <Skeleton variant="rectangular" width={350} height={400} animation="wave"></Skeleton>
                        ) : (
                            <StatisticsTable/>
                        )
                        }
                        {hoveredCol !== null && tooltipPos && (
                            <div
                                style={{
                                    position: 'fixed',
                                    top: tooltipPos.y,
                                    left: tooltipPos.x,
                                    transform: 'translate(-50%, -100%)',
                                    background: 'white',
                                    padding: '6px',
                                    borderRadius: '8px',
                                    boxShadow: '0 4px 10px rgba(0,0,0,0.2)',
                                    zIndex: 1000,
                                }}
                            >
                                <img
                                    src={shirts[hoveredCol].src}
                                    alt={`Футболка ${shirts[hoveredCol].name}`}
                                    style={{ width: 50, height: 50 }}
                                />
                            </div>
                        )}
                    </div>
                    <Divider orientation="vertical" flexItem sx={{backgroundColor: "white"}}/>
                    <div className="home__run">
                        {loading ? (
                            <Skeleton variant="rectangular" width={500} height={300} animation="wave"></Skeleton>
                        ) : (
                            <RunChart />
                            )
                        }
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Home;