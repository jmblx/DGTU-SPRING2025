import { NavLink, useNavigate } from "react-router-dom";
import logo from '../assets/logo.svg';
import '../sass/components/_all.scss';

export const Header = () => {
    const navigate = useNavigate();

    return (
        <div className="wrapper">
            <div className="container">
                <header className="header">
                    <div className="header__logo">
                        <NavLink to={'/simulate'}><img src={logo} alt="Logo"/></NavLink>
                    </div>
                    <button onClick={() => navigate('/parametrs')} className="header__button">
                        Характеристика
                    </button>
                </header>
            </div>
        </div>
    )
}