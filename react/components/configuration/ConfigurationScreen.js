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

  useEffect(() => {
    async function componentMount(){
      let checkboxConfig = await getElementsCheckbox();
      setOriginalConfig(checkboxConfig);
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
    const data = await response.json();
    setElementsCheckboxs(data);

    return data;
  }

  function checkboxUpdated(key, checkboxValue){
    let config = JSON.parse(JSON.stringify(elementsCheckboxs)); //deep copy
    console.log(key)
    config[key]['isChecked'] = checkboxValue;

    const shouldDisableFaceMask = config['Barbijo']['isChecked'] || config['Proteccion ocular']['isChecked'];
    const shouldDisableGlassesAndMask = config['Mascara']['isChecked'];

    config["Barbijo"]['isDisabled'] = shouldDisableGlassesAndMask;
    config["Proteccion ocular"]['isDisabled'] = shouldDisableGlassesAndMask;
    config["Mascara"]['isDisabled'] = shouldDisableFaceMask;
    console.log(config)
    setButtonDisable(JSON.stringify(config) === JSON.stringify(originalConfig));

    setElementsCheckboxs(config);
  }

  async function saveConfig(){

    const configToSave = {};
    Object.entries(elementsCheckboxs).map(([key, value]) => {
      configToSave[key] = value['isChecked'];
    });

    console.log(configToSave);

    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(configToSave),
    };

    await fetch(Config.backendEndpoint + "/configuration", requestOptions);
  }

  return (
    <div>
      <FormControl component="fieldset">
        <FormLabel component="legend">
          <b>Elementos obligatorios</b>
        </FormLabel>
        <FormGroup aria-label="position" row></FormGroup>

        {Object.entries(elementsCheckboxs).map(([key, check]) => (
          <ElementDetectionCheckbox value={check['elementName']} checked={check['isChecked']} disable={check['isDisabled']} key={key} onChange={checkboxUpdated}/>
        ))}

        <FormLabel component="legend">
          <b>Alertas sonoras</b>
        </FormLabel>
        <FormGroup aria-label="position" row></FormGroup>
        <FormControlLabel
          value="Alertas sonoras"
          control={<Checkbox color="primary" />}
          label="Alertas sonoras"
        />
      </FormControl>

      <hr />
      <Button className="right" color="primary" href='/statistics' disabled={buttonDisable} onClick={saveConfig}>
        Guardar
      </Button>
      <hr />
    </div>
  );
};
