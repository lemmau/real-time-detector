import React, { useState, useEffect } from "react";
import "./StatisticsScreen.css";
import Button from "react-bootstrap/Button";
import "react-datepicker/dist/react-datepicker.css";
import Modal from "react-bootstrap/Modal";
import Checkbox from "@material-ui/core/Checkbox";
import FormGroup from "@material-ui/core/FormGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import FormControl from "@material-ui/core/FormControl";
import FormLabel from "@material-ui/core/FormLabel";
import { makeStyles } from "@material-ui/core/styles";
import "react-datepicker/dist/react-datepicker.css";
import { ModalGraph } from "./StatisticGraphModal";
import { SendStatsEmails } from "./SendStatsEmails";
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
}));

export const StatisticsContext = React.createContext({
  periodicidad: "",
  hora: "",
  propiedadAdicional: "",
  emailsList: [],
});

export const StatisticsScreen = () => {
  const [showReviewStatics, setShowStatics] = useState(false);
  const [sendEmails, setSendEmails] = useState(false);
  const [periodicidad, setFrequency] = useState("diaria");
  const [hora, setHour] = useState("");
  const [propiedadAdicional, setAditionalProperty] = useState("");
  const classes = useStyles();

  const handleClose = () => setShowStatics(false);
  const handleShow = () => setShowStatics(true);

  useEffect(() => {
    async function loadEmails() {
      if (StatisticsContext._currentValue.emailsList.length == 0) {
        console.log("Loading emails from useEffect");
        const emails = await loadEmailsList();
        StatisticsContext._currentValue.emailsList = emails;
      }

      console.log("Emails loaded from useEffect");
    }

    loadEmails();
  });

  const handleClickSendEmails = async () => {
    setSendEmails(!sendEmails);

    if (StatisticsContext._currentValue.emailsList.length == 0) {
      const emails = await loadEmailsList();
      StatisticsContext._currentValue.emailsList = emails;
    }
  };

  async function loadEmailsList() {
    console.log("Loading emails from DB");

    const requestOptions = {
      method: "GET",
    };

    const emails = await fetch(
      Config.backendEndpoint + "/emails",
      requestOptions
    );

    const parsedEmails = await emails.json();
    console.log("Emails loaded: ", parsedEmails);

    return parsedEmails;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("SendEmails: ", sendEmails);

    if (sendEmails) {
      const frecuency = {
        hora: StatisticsContext._currentValue.hora,
        periodicidad: StatisticsContext._currentValue.periodicidad,
        propiedadAdicional: StatisticsContext._currentValue.propiedadAdicional,
      };

      console.log("Frecuency options: ", frecuency);

      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(frecuency),
      };

      await fetch(Config.backendEndpoint + "/loadCron", requestOptions);
    } else {
      const requestOptions = {
        method: "GET",
      };

      await fetch(Config.backendEndpoint + "/removeCron", requestOptions);
    }
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <h1>Estadísticas</h1>
        <hr />
        <table id="header">
          <tbody>
            <tr>
              <td>
                <FormControl component="fieldset">
                  <FormLabel component="legend">
                    <b></b>
                  </FormLabel>
                  <FormGroup aria-label="position" row></FormGroup>
                  <FormControlLabel
                    value="Enviar estadísticas por email"
                    control={<Checkbox color="primary" />}
                    label="Enviar estadísticas por email"
                    checked={sendEmails}
                    onClick={handleClickSendEmails}
                  />
                </FormControl>
              </td>
              <td className="align-middle">
                <Button variant="primary" onClick={handleShow}>
                  Consultar Estadísticas
                </Button>

                <Modal size="lg" show={showReviewStatics} onHide={handleClose}>
                  <Modal.Header closeButton>
                    <Modal.Title>Estadísticas</Modal.Title>
                  </Modal.Header>
                  <Modal.Body>
                    <ModalGraph />
                  </Modal.Body>
                  <Modal.Footer>
                    <Button variant="primary" onClick={handleClose}>
                      Cerrar
                    </Button>
                  </Modal.Footer>
                </Modal>
              </td>
            </tr>
            {sendEmails ? <SendStatsEmails /> : null}
          </tbody>
        </table>
        <hr />
        <div>
          <Button
            className="right"
            type="submit"
            color="primary"
          >
            Guardar
          </Button>
        </div>
      </form>
    </>
  );
};
