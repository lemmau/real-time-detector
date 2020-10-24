import React, { useState, useCallback, useEffect } from "react";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import "bootstrap/dist/css/bootstrap.css";
import { makeStyles } from "@material-ui/core/styles";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";
import Config from "Config";

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
  errorMessage: {
    marginTop: theme.spacing(2),
    color:"red"
  },
}));

export const CameraScreen = () => {
  const classes = useStyles();
  const [camara, setCamara] = useState("");
  const [devices, setDevices] = useState([]);
  const [saveButtonDisabled, setsaveButtonDisabled] = useState(true);

  const handleDevices = useCallback(
    (mediaDevices) =>
      setDevices(mediaDevices.filter(({ kind }) => kind === "videoinput")),
    [setDevices]
  );

  useEffect(() => {
    navigator.mediaDevices.enumerateDevices().then(handleDevices);
  }, [handleDevices]);


  const handleChangeDevice = (deviceId) => {
  
    console.log("Selected device id: ", deviceId);

    if(!deviceId) {
      setsaveButtonDisabled(false);
    }

    setCamara(deviceId);
  };

  const handleSubmit = () => {

    async function setStatisticsConfiguration() {
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({"deviceId": camara}),
      };

      await fetch(
        Config.backendEndpoint + "/set_camera",
        requestOptions
      );

    }
    setStatisticsConfiguration();
  };

  return (
    <>
      <Modal show={true}>
        <Modal.Header closeButton>
          <Modal.Title>Seleccione cámara</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <FormControl variant="outlined" className={classes.formControl}>
            <InputLabel id="demo-simple-select-outlined-label">
              Cámara
            </InputLabel>
            <Select
              labelId="demo-simple-select-outlined-label"
              id="demo-simple-select-outlined"
              label="Cámara"
              error={devices.length == 0}
            >
              {devices.map((device, key) => (
                <MenuItem value={key} key={key} onClick={() => handleChangeDevice(key)}>
                  {device.label || `Device ${key + 1}`}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          {devices.length == 0 ?
            <div className={classes.errorMessage}>
              No se han detectado cámaras. Por favor verifique la conexión de las mismas"
            </div> : ""}
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="primary"
            onClick={handleSubmit}
            href="/configuration"
            type="submit"
            disabled={saveButtonDisabled}
          >
            Guardar
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};
