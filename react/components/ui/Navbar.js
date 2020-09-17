import React from 'react'
import { Link, NavLink } from 'react-router-dom'
import imagen from '../../assets/rtd-icon.png';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
    formControl: {
      margin: theme.spacing(1),
      minWidth: 200,
      minHeight:50,
      marginLeft:100,
      marginRight:50
    },
    selectEmpty: {
      marginTop: theme.spacing(2),
    },
    root: {
      width: '100%',
      height: 400,
      maxWidth: 300,
      backgroundColor: theme.palette.background.paper,
    },
    center:{
      justifyContent: "center",
      alignItems: "center",
      verticalAlign: "middle",
      marginRight:50,
      marginLeft:20,
    },
    rtd:{
        marginRight:10,
        marginLeft:10,
      },
    topcorner:{ 
      position:"absolute",
       top:0,
      right:0, },
  }));

export const Navbar = () => {
    const classes = useStyles();
    return (
        <nav className="navbar navbar-expand-sm navbar-dark bg-dark">
            <div className={classes.rtd}><img src={imagen} width="40" height="40" alt="Imagen" /></div>
            
            <Link 
                className="navbar-brand" 
                to="/"
            >
                RTD
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
  );
};