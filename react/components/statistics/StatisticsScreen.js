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
import "react-datepicker/dist/react-datepicker.css";
import { ModalGraph } from "./StatisticGraphModal";
import { SendStatsEmails } from "./SendStatsEmails";
import styled from "styled-components";
import Config from "Config";

const StatisticsWrapper = styled.div`
  align-items: center;
  display: flex;
  flex-direction: row;
`;

export const StatisticsScreen = () => {
  const [showReviewStatics, setShowStatics] = useState(false);
  const [showSendEmails, setShowSendEmails] = useState(false);
  const [originalConfig, setOriginalConfig] = useState();
  const [actualConfig, setActualConfig] = useState();

  const handleClose = () => setShowStatics(false);
  const handleShow = () => setShowStatics(true);

  useEffect(() => {
    async function loadDefaultDataConfig() {
      const requestOptions = {
        method: "GET",
      };

      const response = await fetch(
        Config.backendEndpoint + "/configuration/stats",
        requestOptions
      );

      const config = await response.json();

      const emails = await loadEmailsList();

      //console.log('config["frequency"]["periodicidad"]', config["frequency"]["periodicidad"]);
      //console.log('config["frequency"]["hora"]', config["frequency"]["hora"]);
      //console.log('config["frequency"]["propiedadAdicional"]', config["frequency"]["propiedadAdicional"]);

      const screenConfig = {
        periodicidad: config["frequency"]["periodicidad"],
        hora: config["frequency"]["hora"],
        propiedadAdicional: config["frequency"]["propiedadAdicional"],
        emailsList: emails,
      };
      setOriginalConfig(screenConfig);
      setActualConfig(screenConfig);
    }

    loadDefaultDataConfig();
  }, []);

  const handleClickSendEmails = async () => {
    setShowSendEmails(!showSendEmails);
  };

  async function loadEmailsList() {

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
    //console.log("SendEmails: ", sendEmails);

    if (actualConfig["emailsList"].lenght) {
      const frecuency = {
        hora: actualConfig['hora'],
        periodicidad: actualConfig['periodicidad'],
        propiedadAdicional: actualConfig['propiedadAdicional'],
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

    updateConfig();
  };

  async function updateConfig() {
    const configToSave = {};
    configToSave["frequency"] = {};
    
    // console.log('StatisticsContext._currentValue.periodicidad', StatisticsContext._currentValue.periodicidad);
    // console.log('StatisticsContext._currentValue.hora', StatisticsContext._currentValue.hora);
    // console.log('StatisticsContext._currentValue.propiedadAdicional', StatisticsContext._currentValue.propiedadAdicional);

    configToSave['sendEmails'] = actualConfig['emailsList'];
    configToSave["frequency"]["periodicidad"] = actualConfig['hora'];
    configToSave["frequency"]["hora"] = actualConfig['configToSave'];
    configToSave["frequency"]["propiedadAdicional"] = actualConfig['configToSave'];
    console.log('Config to save', configToSave);

    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(configToSave),
    };

    await fetch(Config.backendEndpoint + "/configuration/stats", requestOptions);
  }

  return (
    <>
      <form onSubmit={handleSubmit}>
        <h1>Estadísticas</h1>
        <hr />

        <StatisticsWrapper>
          <FormControl component="fieldset">
            <FormLabel component="legend">
              <b></b>
            </FormLabel>
            <FormGroup aria-label="position" row></FormGroup>
            <FormControlLabel
              label="Mostrar Opciones Estadísticas por Email"
              control={<Checkbox
                color="primary"
                checked={showSendEmails}
               />}
              onClick={handleClickSendEmails}
            />
          </FormControl>

          <Button variant="primary" onClick={handleShow}>
            Consultar Estadísticas
          </Button>
        </StatisticsWrapper>

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

        {showSendEmails ? 
          <SendStatsEmails params={actualConfig}/>
        : null}

        <hr />
        <div>
          <Button className="right" type="submit" color="primary">
            Guardar
          </Button>
        </div>
      </form>
    </>
  );
};
