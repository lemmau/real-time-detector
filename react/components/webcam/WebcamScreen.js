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


const WebcamWrapper = styled.div`
  align-items: center;
  display: flex;
  justify-content: center;
`




export const WebcamScreen = () => {
  const [show, setShow] = useState(false);
  const getAlarm = async() => {
    const response = await fetch(Config.backendEndpoint + "/alarm");
    const data = await response.json();
    {() => setShow(data)};
  }

  return (
    <>{show && <div>
    <Row>
        <Col xs={6}>
          <Toast onClose={() => setShow(false)} show={show} delay={3000} autohide>
            <Toast.Header>
              <img
                src="holder.js/20x20?text=%20"
                className="rounded mr-2"
                alt=""
              />
              <strong className="mr-auto">Alerta</strong>
              <small>0 mins ago</small>
            </Toast.Header>
            <Toast.Body>Hay mucha gente sin protección</Toast.Body>
          </Toast>
        </Col>
        <Col xs={6}>
          <Button onClick={() => setShow(true)}>Show Toast</Button>
        </Col>
      </Row>
      
      </div>}
    <WebcamWrapper>
      <Img
        src={[Config.backendEndpoint + '/video_feed', image]}
      />
    </WebcamWrapper>
    <ReactAudioPlayer
        src={'/sound.mp3'}
        autoPlay
      />
    </>
  );
};
