import React from 'react';
//import 'bootstrap/dist/css/bootstrap.css';
//import './Camera.css';
import './StatisticsScreen.css'
import Checkbox from '@material-ui/core/Checkbox';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';
import {Button, Modal, ModalHeader, ModalBody, ModalFooter} from 'reactstrap';
import { Link, NavLink } from 'react-router-dom'

export const StatisticsScreen = () => {
  
    return (
      <>
<div id="header">
<FormControl component="fieldset">
      <FormLabel component="legend"><b></b></FormLabel>
      <FormGroup aria-label="position" row></FormGroup>
      <FormControlLabel
          value="Enviar estadísticas por email"
          control={<Checkbox color="primary" />}
          label="Enviar estadísticas por email"
          labelPlacement="Enviar estadísticas por email"
        />
        <FormLabel component="legend"><b>Alertas sonoras</b></FormLabel>
      <FormGroup aria-label="position" row></FormGroup>
      <FormControlLabel
          value="Alertas sonoras"
          control={<Checkbox color="primary" />}
          label="Alertas sonoras"
          labelPlacement="Alertas sonoras"
        />
    </FormControl>
</div>
<hr/>
<div>
                        <Button href="/configuration" color="primary">Volver a Configuración</Button>
                        <Button className="right" href="/webcam" color="primary">Guardar</Button>
                    
                    
</div>
      </>
    );
  }; 