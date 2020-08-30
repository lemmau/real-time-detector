import React, { useState } from 'react';
import {Img} from 'react-image';
import styled from 'styled-components'
import image from '../../assets/broken-image.png';
import Config from 'Config';
import Toast from 'react-bootstrap/Toast';
import ToastHeader from 'react-bootstrap/ToastHeader';
import ToastBody from 'react-bootstrap/ToastBody';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import ReactAudioPlayer from 'react-audio-player';
import Webcam from "react-webcam";


const WebcamWrapper = styled.div`
  align-items: center;
  display: flex;
  justify-content: center;
`




export const WebcamScreen = () => {

  return (
    <>
    <Webcam />
    </>
  );
};
