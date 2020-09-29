import React, { useState, useEffect } from "react";
import "./StatisticsScreen.css";
import Button from "react-bootstrap/Button";
import "react-datepicker/dist/react-datepicker.css";
import Modal from "react-bootstrap/Modal";
import Loader from 'react-loader-spinner';
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
  const [originalConfig, setOriginalConfig] = useState({});
  const [actualConfig, setActualConfig] = useState({});
  const [isDataLoaded, setIsDataLoaded] = useState(false);
  const [buttonDisable, setButtonDisable] = useState(true);

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

      const screenConfig = {
        sendEmails: config["sendEmails"],
        periodicidad: config["frequency"]["periodicidad"],
        hora: config["frequency"]["hora"],
        propiedadAdicional: config["frequency"]["propiedadAdicional"],
        emailsList: emails,
      };

      setOriginalConfig(screenConfig);
      setActualConfig(screenConfig);
      setIsDataLoaded(true);

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

    if (actualConfig["sendEmails"]) {
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

  function statsEmailsOnChange(newProperties){
    const config = {...actualConfig};
    
    for (var [key, value] of Object.entries(newProperties)) {
      config[key] = value;
    }

    setActualConfig(config);
    console.log(config);

    const shouldDisableSaveButton = JSON.stringify(config) === JSON.stringify(originalConfig);
    setButtonDisable(shouldDisableSaveButton);
  }

  return (
    <>
      <form onSubmit={handleSubmit}>
        <h1>Estadísticas</h1>
        <hr />

        <StatisticsWrapper>
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

        {isDataLoaded? 
        <SendStatsEmails params={actualConfig} onPropertyChange={statsEmailsOnChange}/>
        : <Loader type="ThreeDots" color="#2326CF" height="100" width="100"/>
        }
        <hr />
        <div>
          <Button className="right" type="submit" color="primary" disabled={buttonDisable}>
            Guardar
          </Button>
        </div>
      </form>
    </>
  );
};
