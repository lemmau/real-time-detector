import React, { useEffect } from 'react';
import {Img} from 'react-image';
import styled from 'styled-components'
import image from '../../assets/broken-image.png';
import Config from 'Config';
import io from 'socket.io-client';
import { useToasts } from 'react-toast-notifications'
import alarmSound from '../../assets/alarm_sound.mp3'

const WebcamWrapper = styled.div`
  align-items: center;
  display: flex;
  justify-content: center;
`

const endpoint = Config.backendEndpoint;
const socket = io.connect(endpoint);

export const WebcamScreen = () => {

  const { addToast } = useToasts();
  let alarm = new Audio(alarmSound);

  useEffect( () => {
    socket.off('alarm').on('alarm', data => {

      const shouldSoundTrigger = data['audio']
      
      if(shouldSoundTrigger){
        alarm.play()
      }

      addToast('Infraccion Detectada', { appearance: 'error', autoDismiss: 'true', autoDismissTimeout: '5000' });
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
