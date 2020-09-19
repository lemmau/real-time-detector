import React, { useState } from "react";
import "./StatisticsScreen.css";
import Button from "react-bootstrap/Button";
import "react-datepicker/dist/react-datepicker.css";
import Modal from "react-bootstrap/Modal";
// import Checkbox from "@material-ui/core/Checkbox";
// import FormGroup from "@material-ui/core/FormGroup";
// import FormControlLabel from "@material-ui/core/FormControlLabel";
import FormControl from "@material-ui/core/FormControl";
// import FormLabel from "@material-ui/core/FormLabel";
import TextField from "@material-ui/core/TextField";
import { makeStyles } from "@material-ui/core/styles";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import Select from "@material-ui/core/Select";
import "react-datepicker/dist/react-datepicker.css";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import PropTypes from "prop-types";
import { FixedSizeList } from "react-window";
import DeleteIcon from "@material-ui/icons/Delete";
import Config from "Config";

const hours = [
  "00",
  "01",
  "02",
  "03",
  "04",
  "05",
  "06",
  "07",
  "08",
  "09",
  "10",
  "11",
  "12",
  "13",
  "14",
  "15",
  "16",
  "17",
  "18",
  "19",
  "20",
  "21",
  "22",
  "23",
];

const weekDays = [
  "Lunes",
  "Martes",
  "Miercoles",
  "Jueves",
  "Viernes",
  "Sabado",
  "Domingo",
];

const monthlyOptions = ["Primer dia del mes", "Ultimo dia del mes"];

export const SendStatsEmails = () => {
  const [showAddNewEmail, setShowD] = useState(false);
  const [showWeekDay, setShowWeekDay] = useState(false);
  const [showMonthDay, setShowMonthDay] = useState(false);
  const [periodicidad, setFrequency] = useState("diaria");
  const [hora, setHour] = useState("");
  const [propiedadAdicional, setAditionalProperty] = useState("");

  const handleCloseNewEmail = () => setShowD(false);
  const handleAddNewEmail = () => setShowD(true);
  const handleCloseWeekDay = () => setShowWeekDay(false);
  const handleShowWeekDay = () => setShowWeekDay(true);
  const handleCloseMonthDay = () => setShowMonthDay(false);
  const handleShowMonthDay = () => setShowMonthDay(true);
  const handleClose = () => setShowStatics(false);

  function clickDay() {
    setFrequency("diaria");
    setAditionalProperty("");
    handleCloseWeekDay();
    handleCloseMonthDay();
  }
  function clickWeekDay() {
    setFrequency("semanal");
    setAditionalProperty("");
    handleShowWeekDay();
    handleCloseMonthDay();
  }
  function clickMonthDay() {
    setFrequency("mensual");
    setAditionalProperty("");
    handleCloseWeekDay();
    handleShowMonthDay();
  }

  function renderRow(props) {
    const { index, style } = props;

    return (
      <>
        <ListItem button style={style} key={index}>
          <ListItemText primary={`a${index + 1}@hotmail.com`} />
          <DeleteIcon />
        </ListItem>
      </>
    );
  }

  renderRow.propTypes = {
    index: PropTypes.number.isRequired,
    style: PropTypes.object.isRequired,
  };

  const useStyles = makeStyles((theme) => ({
    formControl: {
      margin: theme.spacing(1),
      minWidth: 200,
      minHeight: 50,
      marginLeft: 100,
      marginRight: 50,
    },
    hourControl: {
      margin: theme.spacing(1),
      minWidth: 100,
      minHeight: 50,
      marginLeft: 100,
      marginRight: 50,
    },
    selectEmpty: {
      marginTop: theme.spacing(2),
    },
    root: {
      width: "100%",
      height: 400,
      maxWidth: 300,
      backgroundColor: theme.palette.background.paper,
    },
    center: {
      justifyContent: "center",
      alignItems: "center",
      verticalAlign: "middle",
      marginRight: 50,
      marginLeft: 20,
    },
    savebutton: {
      position: "absolute",
      right: 150,
    },
    topcorner: {
      position: "absolute",
      top: 0,
      right: 0,
    },
  }));

  const classes = useStyles();

  return (
    <>
      <tr>
        <h3>Destinatarios</h3>
      </tr>
      <tr>
        <td>
          <div className={classes.center}>
            <FixedSizeList
              height={250}
              width={300}
              itemSize={46}
              itemCount={10}
            >
              {renderRow}
            </FixedSizeList>
          </div>
        </td>
        <td className="align-top">
          <Button variant="primary" onClick={handleAddNewEmail}>
            Agregar nuevo destinatario
          </Button>

          <Modal show={showAddNewEmail} onHide={handleCloseNewEmail}>
            <Modal.Header closeButton>
              <Modal.Title>Nuevo destinatario</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              Email
              <form noValidate autoComplete="off">
                <TextField
                  id="outlined-basic"
                  label="Ingresar email"
                  variant="outlined"
                />
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
        <h3>Periodicidad</h3>
      </tr>
      <tr>
        <td>
          <FormControl variant="outlined" className={classes.formControl}>
            <InputLabel id="demo-simple-select-outlined-label">
              Frecuencia
            </InputLabel>
            <Select
              labelId="demo-simple-select-outlined-label"
              id="demo-simple-select-outlined"
              label="Frecuencia"
            >
              <MenuItem value={"diaria"} onClick={clickDay}>
                Diaria
              </MenuItem>
              <MenuItem value={"semanal"} onClick={clickWeekDay}>
                Semanal
              </MenuItem>
              <MenuItem value={"mensual"} onClick={clickMonthDay}>
                Mensual
              </MenuItem>
            </Select>
          </FormControl>
        </td>
        <td>
          {showWeekDay && (
            <FormControl variant="outlined" className={classes.formControl}>
              <InputLabel id="demo-simple-select-outlined-label">
                Enviar el día
              </InputLabel>
              <Select
                labelId="demo-simple-select-outlined-label"
                id="demo-simple-select-outlined"
                label="Enviar el día"
              >
                {weekDays.map((day) => (
                  <MenuItem
                    value={day}
                    onClick={() => setAditionalProperty(day)}
                  >
                    {day}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          )}
        </td>
        <td>
          {showMonthDay && (
            <FormControl variant="outlined" className={classes.formControl}>
              <InputLabel id="demo-simple-select-outlined-label">
                Enviar el día
              </InputLabel>
              <Select
                labelId="demo-simple-select-outlined-label"
                id="demo-simple-select-outlined"
                label="Enviar el día"
              >
                {monthlyOptions.map((monthlyOption) => (
                  <MenuItem
                    value={monthlyOption}
                    onClick={(e) => setAditionalProperty(monthlyOption)}
                  >
                    {monthlyOption}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          )}
        </td>
        <td>
          <FormControl variant="outlined" className={classes.hourControl}>
            <InputLabel id="demo-simple-select-outlined-label">Hora</InputLabel>
            <Select
              labelId="demo-simple-select-outlined-label"
              id="demo-simple-select-outlined"
              label="Hora"
            >
              {hours.map((hour) => (
                <MenuItem value={hour} onClick={() => setHour(hour)}>
                  {hour}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </td>
      </tr>
    </>
  );
};
