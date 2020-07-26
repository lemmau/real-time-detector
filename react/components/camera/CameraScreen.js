import React from 'react';
import {Button, Modal, ModalHeader, ModalBody, ModalFooter} from 'reactstrap';
//import 'bootstrap/dist/css/bootstrap.css';
//import './Camera.css';
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import { Link, NavLink } from 'react-router-dom'

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
  const [camara, setCamara] = React.useState('');

  const handleChange = (event) => {
    setCamara(event.target.value);
  };

    return (
        <>
        <ModalHeader>
                     Seleccione cámara
                </ModalHeader>
            <FormControl variant="outlined" className={classes.formControl}>
        <InputLabel id="demo-simple-select-outlined-label">Cámara</InputLabel>
        <Select
          labelId="demo-simple-select-outlined-label"
          id="demo-simple-select-outlined"
          label="Age"
        >
          <MenuItem value="">
            <em>None</em>
          </MenuItem>
          <MenuItem value={1}>Cámara 1</MenuItem>
          <MenuItem value={2}>Cámara 2</MenuItem>
          <MenuItem value={3}>Cámara 3</MenuItem>
        </Select>
      </FormControl>
      <hr/>
                        <Button className="right" color="primary" href="/configuration">Guardar</Button>
    </>   


        /*<>
            <Modal isOpen>
                <ModalHeader>
                     Seleccione cámara
                </ModalHeader>
                <ModalBody>
                    <select>
                        <option selected value="1">Cámara 1</option>
                        <option value="2">Cámara 2</option>
                        <option value="3">Cámara 3</option>
                        <option value="4">Cámara 4</option>
                    </select>
                </ModalBody>
                <ModalFooter>
                    <Button color="primary">Guardar</Button>
                </ModalFooter>
            </Modal>
        </>*/
    );
        
} 


