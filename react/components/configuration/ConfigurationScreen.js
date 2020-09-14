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

  function checkboxClicked() {
    setChecked(!checked);
    setConfiguration(+!checked);
  }

  async function setConfiguration(isEnable) {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ element: props.value, enable: isEnable }),
    };

    await fetch(Config.backendEndpoint + "/configuration", requestOptions);
  }

  return (
    <FormControlLabel
      value={props.value}
      control={
        <Checkbox
          checked={checked}
          color="primary"
          onChange={checkboxClicked}
        />
      }
      label={props.value}
    />
  );
};

ElementDetectionCheckbox.propTypes = {
  value: PropTypes.string,
  checked: PropTypes.bool,
};

ElementDetectionCheckbox.defaultProps = {
  checked: false,
};

export const ConfigurationScreen = () => {
  const [elementsCheckboxs, setElementsCheckboxs] = useState({});

  useEffect(() => {
    async function getFields() {
      const requestOptions = {
        method: "GET",
      };

      const response = await fetch(
        Config.backendEndpoint + "/configuration",
        requestOptions
      );
      const data = await response.json();
      setElementsCheckboxs(data);
    }

    getFields();
  }, []);

  return (
    <div>
      <FormControl component="fieldset">
        <FormLabel component="legend">
          <b>Elementos obligatorios</b>
        </FormLabel>
        <FormGroup aria-label="position" row></FormGroup>

        {Object.entries(elementsCheckboxs).map(([key, value]) => (
          <ElementDetectionCheckbox value={key} checked={value} key={key} />
        ))}

        <FormLabel component="legend">
          <b>Alertas sonoras</b>
        </FormLabel>
        <FormGroup aria-label="position" row></FormGroup>
        <FormControlLabel
          value="Alertas sonoras"
          control={<Checkbox color="primary" />}
          label="Alertas sonoras"
          labelPlacement="Alertas sonoras"
        />
      </FormControl>

      <hr />
      <Button className="right" color="primary" href="/statistics">
        Guardar
      </Button>
      <hr />
    </div>
  );
};
