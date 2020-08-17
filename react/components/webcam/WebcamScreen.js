import React from 'react';
import {Img} from 'react-image';
import styled from 'styled-components'
import image from '../../assets/broken-image.png';
import Config from 'Config';

const WebcamWrapper = styled.div`
  align-items: center;
  display: flex;
  justify-content: center;
`

export const WebcamScreen = () => {
  return (
    <WebcamWrapper>
      <Img
        src={[Config.backendEndpoint + '/video_feed', image]}
      />
    </WebcamWrapper>
  );
};
