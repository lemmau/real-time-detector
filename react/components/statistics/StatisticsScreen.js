import React, { useState } from "react";
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

export const StatisticsScreen = () => {
  // const [startDate, setStartDate] = useState(new Date());
  const [showReviewStatics, setShowStatics] = useState(false);
  const [sendEmails, setSendEmails] = useState(false);

  const classes = useStyles();

  const handleClose = () => setShowStatics(false);
  const handleShow = () => setShowStatics(true);

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("SendEmails: ", sendEmails);

    if (sendEmails) {
      // console.log("SendStatsEmails.hora: ", SendStatsEmails.hora);
      // console.log("SendStatsEmails.periodicidad: ", SendStatsEmails.periodicidad);
      // console.log("SendStatsEmails.propiedadAdicional: ", SendStatsEmails.propiedadAdicional);

      const frecuency = {
        hora: 'SendStatsEmails.hora',
        periodicidad: 'SendStatsEmails.periodicidad',
        propiedadAdicional: 'SendStatsEmails.propiedadAdicional',
      };

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
        <div id="header">
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
                  onClick={() => setSendEmails(!sendEmails)}
                />
              </FormControl>
            </td>
            <td>
              <p></p>
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
          <p></p>

          <div>
              {
                  sendEmails? <SendStatsEmails /> : null
              }
          </div>

        </div>
        <hr />
        <div>
          <Button className={classes.savebutton} type="submit" color="primary">
            Guardar
          </Button>
        </div>
      </form>
    </>
  );
};
