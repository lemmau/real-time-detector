import React, { useState } from "react";
import "./StatisticsScreen.css";
import Button from "react-bootstrap/Button";
import "react-datepicker/dist/react-datepicker.css";
import Modal from "react-bootstrap/Modal";
import FormControl from "@material-ui/core/FormControl";
import TextField from "@material-ui/core/TextField";
import { makeStyles } from "@material-ui/core/styles";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import Select from "@material-ui/core/Select";
import "react-datepicker/dist/react-datepicker.css";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import Typography from "@material-ui/core/Typography";
import DeleteIcon from "@material-ui/icons/Delete";
import { StatisticsContext } from "./StatisticsScreen";
import Config from "Config";

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
  demo: {
    backgroundColor: theme.palette.background.paper,
  },
  title: {
    margin: theme.spacing(4, 0, 2),
  },
}));

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
  const [showAddNewEmail, setShowAddNewEmailModal] = useState(false);
  const [showWeekDay, setShowWeekDay] = useState(false);
  const [showMonthDay, setShowMonthDay] = useState(false);
  const [periodicidad, setFrequency] = useState("diaria");
  const [hora, setHour] = useState("");
  const [propiedadAdicional, setAditionalProperty] = useState("");
  const [saveNewEmailDisabled, setsaveNewEmailDisabled] = useState(true);
  const [newEmailError, setNewEmailError] = useState(false);
  const [emailsList, setEmailsList] = useState(
    StatisticsContext._currentValue.emailsList
  );
  const [newEmail, setNewEmail] = useState("");

  const handleAddNewEmail = () => setShowAddNewEmailModal(true);
  const handleCloseWeekDay = () => setShowWeekDay(false);
  const handleShowWeekDay = () => setShowWeekDay(true);
  const handleCloseMonthDay = () => setShowMonthDay(false);
  const handleShowMonthDay = () => setShowMonthDay(true);

  function handleDeleteEmail(email) {
    console.log("Email to delete: ", email);

    // const requestOptions = {
    //   method: "POST",
    //   headers: { "Content-Type": "application/json" },
    //   body: JSON.stringify(newEmail),
    // };

    // // await fetch(Config.backendEndpoint + "/email", requestOptions);
    console.log(
      "StatisticsContext._currentValue.emailsList before: ",
      StatisticsContext._currentValue.emailsList
    );
    removeItem(StatisticsContext._currentValue.emailsList, email);
    console.log(
      "StatisticsContext._currentValue.emailsList after: ",
      StatisticsContext._currentValue.emailsList
    );
    // setShowAddNewEmailModal(false);
  }

  function removeItem(arr, item) {
    var index = arr.indexOf(item);
    if (index > -1) {
      arr.splice(index, 1);
    }
  }

  function handleSaveNewEmail() {
    console.log("New email to save: ", newEmail);

    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newEmail),
    };

    // await fetch(Config.backendEndpoint + "/email", requestOptions);
    StatisticsContext._currentValue.emailsList.push(newEmail);
    setShowAddNewEmailModal(false);
  }

  function clickDay() {
    setFrequency("diaria");
    setAditionalProperty("");
    handleCloseWeekDay();
    handleCloseMonthDay();
    StatisticsContext._currentValue.periodicidad = periodicidad;
    StatisticsContext._currentValue.propiedadAdicional = propiedadAdicional;
  }

  function clickWeekDay() {
    setFrequency("semanal");
    setAditionalProperty("");
    handleShowWeekDay();
    handleCloseMonthDay();
    StatisticsContext._currentValue.periodicidad = periodicidad;
    StatisticsContext._currentValue.propiedadAdicional = propiedadAdicional;
  }

  function clickMonthDay() {
    setFrequency("mensual");
    setAditionalProperty("");
    handleCloseWeekDay();
    handleShowMonthDay();
    StatisticsContext._currentValue.periodicidad = periodicidad;
    StatisticsContext._currentValue.propiedadAdicional = propiedadAdicional;
  }

  function validateEmail(email) {
    const pattern = new RegExp(
      /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
    const emailValue = email.target.value;
    console.log("email: ", emailValue);

    if (!pattern.test(emailValue)) {
      console.log("Invalid email");
      setsaveNewEmailDisabled(true);
      setNewEmailError(true);
    } else {
      console.log("Valid email");
      setNewEmailError(false);
      setsaveNewEmailDisabled(false);
      setNewEmail(emailValue);
    }
  }

  const classes = useStyles();

  const EmailList = () => {
    return (
      <>
        <List>
          {emailsList.map((email) => (
            <ListItem button key={email}>
              <ListItemText primary={email} />
              <DeleteIcon onClick={() => handleDeleteEmail(email)} />
            </ListItem>
          ))}
        </List>
      </>
    );
  };

  return (
    <>
      <tr>
        <td>
          <div className={classes.center}>
            <Typography variant="h6" className={classes.title}>
              Destinatarios
            </Typography>
            <div className={classes.demo}>
              <EmailList />
            </div>
          </div>
        </td>
        <td className="align-top">
          <Button variant="primary" onClick={handleAddNewEmail}>
            Agregar nuevo destinatario
          </Button>

          <Modal show={showAddNewEmail}>
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
                  onChange={validateEmail}
                  error={newEmailError}
                />
              </form>
            </Modal.Body>
            <Modal.Footer>
              <Button
                variant="primary"
                disabled={saveNewEmailDisabled}
                onClick={handleSaveNewEmail}
              >
                Guardar
              </Button>
            </Modal.Footer>
          </Modal>
        </td>
      </tr>
      <tr>
        <th>
          <h3>Periodicidad</h3>
        </th>
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
              value=""
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
                value=""
              >
                {weekDays.map((day) => (
                  <MenuItem
                    key={day}
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
                value=""
              >
                {monthlyOptions.map((monthlyOption) => (
                  <MenuItem
                    key={monthlyOption}
                    value={monthlyOption}
                    onClick={() => setAditionalProperty(monthlyOption)}
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
              value=""
            >
              {hours.map((hour) => (
                <MenuItem
                  key={hour}
                  value={hour}
                  onClick={() => {
                    setHour(hour);
                    StatisticsContext._currentValue.hora = hour;
                    StatisticsContext._currentValue.periodicidad = periodicidad;
                    StatisticsContext._currentValue.propiedadAdicional = propiedadAdicional;
                  }}
                >
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