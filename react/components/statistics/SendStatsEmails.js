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
import DeleteIcon from "@material-ui/icons/Delete";
import { StatisticsContext } from "./StatisticsScreen";
import Config from "Config";

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 200,
    minHeight: 50,
    marginRight: 10,
  },
  hourControl: {
    margin: theme.spacing(1),
    minWidth: 100,
    minHeight: 50,
    marginRight: 10,
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
  td: {
    width: 1,
    "white-space": "nowrap",
  },
  sep: {
    position: "relative",
    overflow: "hidden",
    height: "1em",
  },
  destinaries: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
  },
  destinataryTitle: {
    paddingRight: "10px",
  },
  addDestinataryText: {
    fontSize: "20px",
  },
  emailItemList: {
    width: "35%",
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
  }
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
  const [periodicidad, setFrequency] = useState(StatisticsContext._currentValue.periodicidad);
  const [hora, setHour] = useState(StatisticsContext._currentValue.hora);
  const [propiedadAdicional, setAditionalProperty] = useState(StatisticsContext._currentValue.propiedadAdicional);
  const [saveNewEmailDisabled, setsaveNewEmailDisabled] = useState(true);
  const [newEmailError, setNewEmailError] = useState(false);
  const [emailsList, setEmailsList] = useState(StatisticsContext._currentValue.emailsList);
  const [newEmail, setNewEmail] = useState("");

  const handleAddNewEmail = () => setShowAddNewEmailModal(true);
  const handleCloseWeekDay = () => setShowWeekDay(false);
  const handleShowWeekDay = () => setShowWeekDay(true);
  const handleCloseMonthDay = () => setShowMonthDay(false);
  const handleShowMonthDay = () => setShowMonthDay(true);

  async function handleDeleteEmail(email) {
    console.log("Email to delete: ", email);

    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(email),
    };

    await fetch(Config.backendEndpoint + "/removeEmail", requestOptions);

    removeItem(StatisticsContext._currentValue.emailsList, email);
    setEmailsList([...StatisticsContext._currentValue.emailsList]);
  }

  function removeItem(arr, item) {
    var index = arr.indexOf(item);
    if (index > -1) {
      arr.splice(index, 1);
    }
  }

  async function handleSaveNewEmail() {
    console.log("New email to save: ", newEmail);

    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newEmail),
    };

    await fetch(Config.backendEndpoint + "/emails", requestOptions);
    StatisticsContext._currentValue.emailsList.push(newEmail);
    setEmailsList(StatisticsContext._currentValue.emailsList);
    setShowAddNewEmailModal(false);
  }

  function handleCloseAddNewEmail() {
    setShowAddNewEmailModal(false);
  }

  function clickDay() {
    setFrequency("Diaria");
    setAditionalProperty("");
    handleCloseWeekDay();
    handleCloseMonthDay();
    StatisticsContext._currentValue.periodicidad = periodicidad;
    StatisticsContext._currentValue.propiedadAdicional = propiedadAdicional;
  }

  function clickWeekDay() {
    setFrequency("Semanal");
    setAditionalProperty("");
    handleShowWeekDay();
    handleCloseMonthDay();
    StatisticsContext._currentValue.periodicidad = periodicidad;
    StatisticsContext._currentValue.propiedadAdicional = propiedadAdicional;
  }

  function clickMonthDay() {
    setFrequency("Mensual");
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

  const EmailList = (props) => {
    const list = props.list;
    console.log("props.list", props.list);

    return (
      <>
        <List>
          {list.map((email) => (
            <ListItem button key={email} className={classes.emailItemList}>
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
     <hr/>
          <div className={classes.center}>
            
            <div className={classes.destinaries}>
              <h3 className={classes.destinataryTitle}>Destinatarios</h3>
        
              <Button onClick={handleAddNewEmail} >
                <b className={classes.addDestinataryText}>+</b>
              </Button>

            </div>

            <div className={classes.demo}>
              <EmailList list={emailsList} />
            </div>

          </div>

          <hr/>

          <Modal show={showAddNewEmail} onHide={handleCloseAddNewEmail}>
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
              <Button variant="primary" onClick={handleCloseAddNewEmail}>
                Me arrepenti
              </Button>
              <Button
                variant="primary"
                disabled={saveNewEmailDisabled}
                onClick={handleSaveNewEmail}
              >
                Agregar!
              </Button>
            </Modal.Footer>
          </Modal>

          <div className={classes.center}>
            <h3>Periodicidad</h3>
    
            <FormControl variant="outlined" className={classes.formControl}>
              <InputLabel id="demo-simple-select-outlined-label">
                Frecuencia
              </InputLabel>
              <Select
                labelId="demo-simple-select-outlined-label"
                id="demo-simple-select-outlined"
                label="Frecuencia"
                value={periodicidad}
              >
                <MenuItem value={"Diaria"} onClick={clickDay}>
                  Diaria
                </MenuItem>
                <MenuItem value={"Semanal"} onClick={clickWeekDay}>
                  Semanal
                </MenuItem>
                <MenuItem value={"Mensual"} onClick={clickMonthDay}>
                  Mensual
                </MenuItem>
              </Select>
            </FormControl>

            <FormControl variant="outlined" className={classes.hourControl}>
              <InputLabel id="demo-simple-select-outlined-label">Hora</InputLabel>
              <Select
                labelId="demo-simple-select-outlined-label"
                id="demo-simple-select-outlined"
                label="Hora"
                value={hora}
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


            {showWeekDay && (
              <FormControl variant="outlined" className={classes.formControl}>
                <InputLabel id="demo-simple-select-outlined-label">
                  Enviar el día
                </InputLabel>
                <Select
                  labelId="demo-simple-select-outlined-label"
                  id="demo-simple-select-outlined"
                  label="Enviar el día"
                  value={propiedadAdicional}
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

            {showMonthDay && (
              <FormControl variant="outlined" className={classes.formControl}>
                <InputLabel id="demo-simple-select-outlined-label">
                  Enviar el día
                </InputLabel>
                <Select
                  labelId="demo-simple-select-outlined-label"
                  id="demo-simple-select-outlined"
                  label="Enviar el día"
                  value={propiedadAdicional}
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
          </div>

    </>
  );
};
