import React from 'react'
import { Link, NavLink } from 'react-router-dom'
import imagen from './imagen.png';

export const Navbar = () => {
    return (
        <nav className="navbar navbar-expand-sm navbar-dark bg-dark">
             <img src={imagen} width="40" height="40" alt="Imagen" />
            <Link 
                className="navbar-brand" 
                to="/"
            >
                IA Detector
            </Link>

            <div className="navbar-collapse">
                <div className="navbar-nav">

                    
                    <NavLink 
                        activeClassName="active"
                        className="nav-item nav-link" 
                        exact
                        to="/configuration"
                    >
                        Configuración
                    </NavLink>

                    <NavLink 
                        activeClassName="active"
                        className="nav-item nav-link" 
                        to="/statistics"
                    >
                        Estadísticas
                    </NavLink>

                    <NavLink 
                        activeClassName="active"
                        className="nav-item nav-link" 
                        exact
                        to="/webcam"
                    >
                        Vivo
                    </NavLink>
                </div>
            </div>

            <div className="navbar-collapse collapse w-100 order-3 dual-collapse2">
                <ul className="navbar-nav ml-auto">
                    <NavLink 
                        activeClassName="active"
                        className="nav-item nav-link" 
                        exact
                        to="/camera"
                    >
                        Salir
                    </NavLink>
                </ul>
            </div>
        </nav>
    )
}