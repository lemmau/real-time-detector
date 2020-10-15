import React, { useState, useEffect } from "react";
import Checkbox from "@material-ui/core/Checkbox";
import FormGroup from "@material-ui/core/FormGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import FormControl from "@material-ui/core/FormControl";
import FormLabel from "@material-ui/core/FormLabel";
import PropTypes from "prop-types";
import { Button } from "reactstrap";
import Config from "Config";

const ElementDetectionCheckbox = (props) => {
  const [checked, setChecked] = useState(props.checked);

  async function checkboxClicked() {
    setChecked(!checked);
    props.onChange(props.value, !checked);
  }

  return (
    <FormControlLabel
      value={props.value}
      control={
        <Checkbox
          checked={checked}
          color="primary"
          onChange={checkboxClicked}
          disabled={props.disable}
        />
      }
      label={props.value}
    />
  );
};

ElementDetectionCheckbox.propTypes = {
  value: PropTypes.string,
  checked: PropTypes.bool,
  disable: PropTypes.bool,
};

ElementDetectionCheckbox.defaultProps = {
  checked: false,
  disable: false,
};

export const ConfigurationScreen = () => {
  const [elementsCheckboxs, setElementsCheckboxs] = useState([]);
  const [buttonDisable, setButtonDisable] = useState(true);
  const [originalConfig, setOriginalConfig] = useState();
  const [soundAlarm, setSoundAlarm] = useState(false);
  const [originalSoundConfig, setOriginalSoundConfig] = useState();

  useEffect(() => {
    async function componentMount() {
      await getElementsCheckbox();
    }
    componentMount();
  }, []);

  async function getElementsCheckbox() {
    const requestOptions = {
      method: "GET",
    };

    const response = await fetch(
      Config.backendEndpoint + "/configuration",
      requestOptions
    );

    const config = await response.json();

    setOriginalConfig(config);
    setSoundAlarm(config["soundAlarm"]);
    setOriginalSoundConfig(config["soundAlarm"]);

    delete config["soundAlarm"];
    setElementsCheckboxs(config);
  }

  function checkboxUpdated(key, checkboxValue) {
    let config = JSON.parse(JSON.stringify(elementsCheckboxs)); //deep copy

    config[key]["isChecked"] = checkboxValue;

    const shouldDisableFaceMask =
      config["Barbijo"]["isChecked"] ||
      config["Proteccion ocular"]["isChecked"];
    const shouldDisableGlassesAndMask = config["Mascara"]["isChecked"];

    config["Barbijo"]["isDisabled"] = shouldDisableGlassesAndMask;
    config["Proteccion ocular"]["isDisabled"] = shouldDisableGlassesAndMask;
    config["Mascara"]["isDisabled"] = shouldDisableFaceMask;

    shouldDisableSaveButton(config, soundAlarm);
    setElementsCheckboxs(config);
  }

  function soundAlarmChanged() {
    shouldDisableSaveButton(elementsCheckboxs, !soundAlarm);
    setSoundAlarm(!soundAlarm);
  }

  function shouldDisableSaveButton(elementsCheckboxs, soundAlarm) {
    const shouldDisableSaveButton =
      JSON.stringify(elementsCheckboxs) === JSON.stringify(originalConfig) &&
      soundAlarm === originalSoundConfig;
    setButtonDisable(shouldDisableSaveButton);
  }

  async function saveConfig(e) {
    console.log("Saving config");
    e.preventDefault();
    const configToSave = {};
    Object.entries(elementsCheckboxs).map(([key, value]) => {
      configToSave[key] = value["isChecked"];
    });
    configToSave["soundAlarm"] = soundAlarm;

    console.log(configToSave);

    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(configToSave),
    };

    await fetch(Config.backendEndpoint + "/configuration", requestOptions);
    window.location.replace("/statistics");
  }

  return (
    <div>
      <FormControl component="fieldset">
        <FormLabel component="legend">
          <b>Elementos obligatorios</b>
        </FormLabel>
        <FormGroup aria-label="position" row></FormGroup>

        {Object.entries(elementsCheckboxs).map(([key, check]) => (
          <ElementDetectionCheckbox
            value={check["elementName"]}
            checked={check["isChecked"]}
            disable={check["isDisabled"]}
            key={key}
            onChange={checkboxUpdated}
          />
        ))}

        <FormLabel component="legend">
          <b>Alertas sonoras</b>
        </FormLabel>
        <FormGroup aria-label="position" row></FormGroup>
        <FormControlLabel
          value="Alertas sonoras"
          label="Alertas sonoras"
          control={
            <Checkbox
              color="primary"
              checked={soundAlarm}
              onChange={soundAlarmChanged}
            />
          }
        />
      </FormControl>

      <hr />
      <Button
        className="right"
        color="primary"
        disabled={buttonDisable}
        onClick={saveConfig}
      >
        Guardar
      </Button>
      <hr />
    </div>
  );
};
