import React, { useEffect } from 'react';
import {Img} from 'react-image';
import styled from 'styled-components'
import image from '../../assets/broken-image.png';
import Config from 'Config';
import io from 'socket.io-client';
import { useToasts } from 'react-toast-notifications'

const WebcamWrapper = styled.div`
  align-items: center;
  display: flex;
  justify-content: center;
`

let endpoint = Config.backendEndpoint;
let socket = io.connect(endpoint);

export const WebcamScreen = () => {

  const { addToast } = useToasts()

  useEffect( () => { 
    socket.on('alarm', data => {
      addToast('Infraccion Detectada', { appearance: 'error' })
    });
  }, []);

  return (
    
    <WebcamWrapper>
      <Img
        src={[Config.backendEndpoint + '/video_feed', image]}
      />
    </WebcamWrapper>

  );
};
