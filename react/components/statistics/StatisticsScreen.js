import React,{useState} from 'react';
//import 'bootstrap/dist/css/bootstrap.css';
//import './Camera.css';
import './StatisticsScreen.css'
import Button from 'react-bootstrap/Button';
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
import "react-datepicker/dist/react-datepicker.css";
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import PropTypes from 'prop-types';
import { FixedSizeList } from 'react-window';
import DeleteIcon from '@material-ui/icons/Delete';
import { ModalGraph } from './StatisticGraphModal';
import Config from "Config";

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 200,
    minHeight:50,
    marginLeft:100,
    marginRight:50
  },
  hourControl: {
    margin: theme.spacing(1),
    minWidth: 100,
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
  savebutton:{ 
    position:"absolute",
    right:150, 
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
  const [showWeekDay, setShowWeekDay] = useState(false);
  const [showMonthDay, setShowMonthDay] = useState(false);
  const [periodicidad, setFrequency] = useState('diaria');
  const [hora, setHour] = useState('');
  const [propiedadAdicional, setAditionalProperty] = useState('');
  

  const classes = useStyles();
  const [camara, setCamara] = React.useState('');

  const handleChange = (event) => {
    setCamara(event.target.value);
  };

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const handleCloseD = () => setShowD(false);
  const handleShowD = () => setShowD(true);
  const handleCloseWeekDay = () => setShowWeekDay(false);
  const handleShowWeekDay = () => setShowWeekDay(true);
  const handleCloseMonthDay = () => setShowMonthDay(false);
  const handleShowMonthDay = () => setShowMonthDay(true);


  function clickDay(){
    setFrequency("diaria");
    setAditionalProperty("");
    handleCloseWeekDay();
    handleCloseMonthDay();

  }
  function clickWeekDay(){
    setFrequency("semanal");
    setAditionalProperty("");
    handleShowWeekDay();
    handleCloseMonthDay();

  }
  function clickMonthDay(){
    setFrequency("mensual");
    setAditionalProperty("");
    handleCloseWeekDay();
    handleShowMonthDay();

  }

  const handleSubmit = (e) => {
    e.preventDefault();

    // TODO API para pasarle los datos al back
    // async function setStatisticsConfiguration() {
    //   const requestOptions = {
    //     method: "GET",
    //   };
  
    //   const response = await fetch(
    //     Config.backendEndpoint + "/configuration"+ periodicidad + hora + propiedadAdicional,
    //     requestOptions
    //   );
    //   const data = await response.json();
    // }
    // setStatisticsConfiguration();
  
  }

  

    return (
      <>
      <form onSubmit={ handleSubmit }>
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

          <ModalGraph/>

        </Modal.Body>
        <Modal.Footer>
        <Button variant="primary" onClick={handleClose}>
            Cerrar
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
          label="Frecuencia"
        >
          <MenuItem value="">
            <em></em>
          </MenuItem>
          <MenuItem value={"diaria"} onClick={clickDay}>Diaria</MenuItem>
          <MenuItem value={"semanal"} onClick={clickWeekDay }>Semanal</MenuItem>
          <MenuItem value={"mensual"} onClick={clickMonthDay}>Mensual</MenuItem>
        </Select>
        </FormControl>
        </td>
        <td>
        {showWeekDay && <FormControl variant="outlined" className={classes.formControl} >
          <InputLabel id="demo-simple-select-outlined-label">Enviar el día</InputLabel>
        <Select
          labelId="demo-simple-select-outlined-label"
          id="demo-simple-select-outlined"
          label="Enviar el día"
        >
          <MenuItem value="">
            <em></em>
          </MenuItem>
          <MenuItem value={"lunes"} onClick={e=>setAditionalProperty("lunes")}>Lunes</MenuItem>
          <MenuItem value={"martes"} onClick={e=>setAditionalProperty("martes")}>Martes</MenuItem>
          <MenuItem value={"miercoles"} onClick={e=>setAditionalProperty("miercoles")}>Miercoles</MenuItem>
          <MenuItem value={"jueves"} onClick={e=>setAditionalProperty("jueves")}>Jueves</MenuItem>
          <MenuItem value={"viernes"} onClick={e=>setAditionalProperty("viernes")}>Viernes</MenuItem>
        </Select>
        </FormControl>}
        </td>
        <td>
        {showMonthDay && <FormControl variant="outlined" className={classes.formControl} >
          <InputLabel id="demo-simple-select-outlined-label">Enviar el día</InputLabel>
        <Select
          labelId="demo-simple-select-outlined-label"
          id="demo-simple-select-outlined"
          label="Enviar el día"
        >
          <MenuItem value="">
            <em></em>
          </MenuItem>
          <MenuItem value={"Primer dia del mes"} onClick={e=>setAditionalProperty("Primer dia del mes")}>Primer dia del mes</MenuItem>
          <MenuItem value={"Último día del mes"} onClick={e=>setAditionalProperty("Último día del mes")}>Ultimo dia del mes</MenuItem>
        </Select>
        </FormControl>}
        </td>
        <td>
        <FormControl variant="outlined" className={classes.hourControl} >
          <InputLabel id="demo-simple-select-outlined-label">Hora</InputLabel>
        <Select
          labelId="demo-simple-select-outlined-label"
          id="demo-simple-select-outlined"
          label="Hora"
        >
          <MenuItem value="">
            <em></em>
          </MenuItem>
          <MenuItem value={"00"} onClick={e=>setHour("00")}>00</MenuItem>
          <MenuItem value={"01"} onClick={e=>setHour("01")}>01</MenuItem>
          <MenuItem value={"02"} onClick={e=>setHour("02")}>02</MenuItem>
          <MenuItem value={"03"} onClick={e=>setHour("03")}>03</MenuItem>
          <MenuItem value={"04"} onClick={e=>setHour("04")}>04</MenuItem>
          <MenuItem value={"05"} onClick={e=>setHour("05")}>05</MenuItem>
          <MenuItem value={"06"} onClick={e=>setHour("06")}>06</MenuItem>
          <MenuItem value={"07"} onClick={e=>setHour("07")}>07</MenuItem>
          <MenuItem value={"08"} onClick={e=>setHour("08")}>08</MenuItem>
          <MenuItem value={"09"} onClick={e=>setHour("09")}>09</MenuItem>
          <MenuItem value={"10"} onClick={e=>setHour("10")}>10</MenuItem>
          <MenuItem value={"11"} onClick={e=>setHour("11")}>11</MenuItem>
          <MenuItem value={"12"} onClick={e=>setHour("12")}>12</MenuItem>
          <MenuItem value={"13"} onClick={e=>setHour("13")}>13</MenuItem>
          <MenuItem value={"14"} onClick={e=>setHour("14")}>14</MenuItem>
          <MenuItem value={"15"} onClick={e=>setHour("15")}>15</MenuItem>
          <MenuItem value={"16"} onClick={e=>setHour("16")}>16</MenuItem>
          <MenuItem value={"17"} onClick={e=>setHour("17")}>17</MenuItem>
          <MenuItem value={"18"} onClick={e=>setHour("18")}>18</MenuItem>
          <MenuItem value={"19"} onClick={e=>setHour("19")}>19</MenuItem>
          <MenuItem value={"20"} onClick={e=>setHour("20")}>20</MenuItem>
          <MenuItem value={"21"} onClick={e=>setHour("21")}>21</MenuItem>
          <MenuItem value={"22"} onClick={e=>setHour("22")}>22</MenuItem>
          <MenuItem value={"23"} onClick={e=>setHour("23")}>23</MenuItem>
                  </Select>
        </FormControl>
        
        </td>
      </tr>
</div>
<hr/>
<div>
    <Button className={classes.savebutton} type="submit"  color="primary"  >Guardar</Button>
</div>
</form>
      </>
    );
  }; 