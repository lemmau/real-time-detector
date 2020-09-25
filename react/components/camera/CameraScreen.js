import React, { useState, useCallback, useEffect } from "react";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import "bootstrap/dist/css/bootstrap.css";
import { makeStyles } from "@material-ui/core/styles";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
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


  const handleChangeDevice = (e) => {
    console.log("Selected device: ", e.label);

    if(e.label != "") {
      setsaveButtonDisabled(false)
    }

    setCamara(e.label);
  };

  const handleSubmit = () => {
    // TODO API para pasarle los datos al back
    // async function setStatisticsConfiguration() {
    //   const requestOptions = {
    //     method: "GET",
    //   };

    //   const response = await fetch(
    //     Config.backendEndpoint + "/configuration"+ periodicidad + hora + propiedadAdicional,
    //     requestOptions
    //   );
    //   const data = await response.json();
    // }
    // setStatisticsConfiguration();
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
            >
              {devices.map((device, key) => (
                <MenuItem value={key} key={key} onClick={handleChangeDevice}>
                  {device.label || `Device ${key + 1}`}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
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
