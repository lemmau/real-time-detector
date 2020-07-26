import React from "react";
import Checkbox from '@material-ui/core/Checkbox';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';
import {Button, Modal, ModalHeader, ModalBody, ModalFooter} from 'reactstrap';
import { Link, NavLink } from 'react-router-dom'

export const ConfigurationScreen = () => (
    <>
    <FormControl component="fieldset">
      <FormLabel component="legend"><b>Elementos obligatorios</b></FormLabel>
      <FormGroup aria-label="position" row></FormGroup>
      <FormControlLabel
          value="Barbijo"
          control={<Checkbox color="primary" />}
          label="Barbijo"
          labelPlacement="Barbijo"
        />
        <FormControlLabel
          value="Protección ocular"
          control={<Checkbox color="primary" />}
          label="Protección ocular"
          labelPlacement="Protección ocular"
        />
        <FormControlLabel
          value="Máscara"
          control={<Checkbox color="primary" />}
          label="Máscara"
          labelPlacement="Máscara"
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
    <hr/>
                        <Button className="right" color="primary" href="/statistics">Guardar</Button>
    </>

);

