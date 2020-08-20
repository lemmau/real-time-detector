import React,{useState} from 'react';
//import 'bootstrap/dist/css/bootstrap.css';
//import './Camera.css';
import './StatisticsScreen.css'
import Button from 'react-bootstrap/Button';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import Modal from 'react-bootstrap/Modal';
import Checkbox from '@material-ui/core/Checkbox';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';
import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import TimePicker from 'react-time-picker';
import { ScrollProvider } from '@foo-software/react-scroll-context';
import { Parallax } from 'react-scroll-parallax';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import StarIcon from '@material-ui/icons/Star';
import PropTypes from 'prop-types';
import { FixedSizeList } from 'react-window';
import DeleteIcon from '@material-ui/icons/Delete';
import grafico from './grafico.png';
import { Link, NavLink } from 'react-router-dom'

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
  topcorner:{ 
    position:"absolute",
     top:0,
    right:0, },
}));

function renderRow(props) {
  const { index, style } = props;

  return (
    <>
    <ListItem button style={style} key={index}>
    <ListItemText primary={`lucas_cepeda${index + 1}@hotmail.com`} /><DeleteIcon />
  </ListItem>
  </>
  );
}

renderRow.propTypes = {
  index: PropTypes.number.isRequired,
  style: PropTypes.object.isRequired,
};

export const StatisticsScreen = () => {
  const[startDate, setStartDate]=useState(new Date());
  const [show, setShow] = useState(false);
  const [showD, setShowD] = useState(false);
  const classes = useStyles();
  const [camara, setCamara] = React.useState('');

  const handleChange = (event) => {
    setCamara(event.target.value);
  };

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const handleCloseD = () => setShowD(false);
  const handleShowD = () => setShowD(true);

  const [value, onChange] = useState('10:00');

    return (
      <>
      <h1>Estadísticas</h1>
      <hr/>
<div id="header">
<tr><td><FormControl component="fieldset">
      <FormLabel component="legend"><b></b></FormLabel>
      <FormGroup aria-label="position" row></FormGroup>
      <FormControlLabel
          value="Enviar estadísticas por email"
          control={<Checkbox color="primary" />}
          label="Enviar estadísticas por email"
          labelPlacement="Enviar estadísticas por email"
        />
    </FormControl></td>
    <td>
      <p></p>
    </td>
    <td className="align-middle">
      <Button variant="primary" onClick={handleShow}>
        Consultar Estadísticas
      </Button>
      <Modal size="lg" show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Estadísticas</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <DatePicker selected={startDate} onChange={date => setStartDate(date)} />
          <img src={grafico} alt="Grafico" />

        </Modal.Body>
        <Modal.Footer>
        <Button variant="primary" onClick={handleClose}>
            Guardar
          </Button>
        </Modal.Footer>
      </Modal></td></tr>
      <p></p>
      <tr><h3>Destinatarios</h3></tr>
      <tr>
        <td>
        <div className={classes.center}>
      <FixedSizeList height={250} width={300} itemSize={46} itemCount={10}>
        {renderRow}
      </FixedSizeList>
    </div>
        </td>
        <td className="align-top">
        <Button variant="primary" onClick={handleShowD}>
        Agregar nuevo destinatario
      </Button>
      
      <Modal show={showD} onHide={handleCloseD}>
        <Modal.Header closeButton>
          <Modal.Title>Nuevo destinatario</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          Email
          <form  noValidate autoComplete="off">
            <TextField id="outlined-basic" label="Ingresar email" variant="outlined" />
          </form>
        </Modal.Body>
        <Modal.Footer>
        <Button variant="primary" onClick={handleClose}>
            Guardar
          </Button>
        </Modal.Footer>
      </Modal>
          </td>

      </tr>
      <p></p>
      <tr>
        <h3>
        Periodicidad
        </h3>
        
      </tr>
      <tr>
        <td>
        <FormControl variant="outlined" className={classes.formControl}>
          <InputLabel id="demo-simple-select-outlined-label">Frecuencia</InputLabel>
        <Select
          labelId="demo-simple-select-outlined-label"
          id="demo-simple-select-outlined"
          label="Age"
        >
          <MenuItem value="">
            <em></em>
          </MenuItem>
          <MenuItem value={1}>Diaria</MenuItem>
          <MenuItem value={2}>Semanal</MenuItem>
          <MenuItem value={3}>Mensual</MenuItem>
        </Select>
        </FormControl>
        </td>
        <td>
        <FormControl variant="outlined" className={classes.formControl}>
          <InputLabel id="demo-simple-select-outlined-label">Enviar el día/número</InputLabel>
        <Select
          labelId="demo-simple-select-outlined-label"
          id="demo-simple-select-outlined"
          label="Age"
        >
          <MenuItem value="">
            <em></em>
          </MenuItem>
          <MenuItem value={1}></MenuItem>
          <MenuItem value={2}></MenuItem>
          <MenuItem value={3}></MenuItem>
        </Select>
        </FormControl>
        </td>
        <td>
          <FormControl variant="outlined" className={classes.formControl}>
          <TimePicker
        onChange={onChange}
        value={value}
      />
          </FormControl>
        
        </td>
      </tr>
</div>
<hr/>
<div>
    <Button href="/configuration" color="primary">Volver a Configuración</Button>
    <Button className="right" href="/webcam" color="primary">Guardar</Button>
</div>
      </>
    );
  }; 