import startPageImg from '../assets/startPageImg.png'
import '../sass/components/_all.scss'
import { useNavigate } from 'react-router-dom';

export const StartPage = () => {
    const navigate = useNavigate();

    return (
        <div className="wrapper">
            <div className="container">
                <div className="start">
                    <div className="start__text">
                        <h1>Система симуляции и анализа забегов для тренера по легкой атлетике</h1>
                        <button onClick={() => navigate('/simulate')}>Просмотреть симуляцию</button>
                    </div>
                    <div className="start__image">
                        <img src={startPageImg} alt=""/>
                    </div>
                </div>
            </div>
        </div>
    )
}
