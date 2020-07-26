import React from 'react';
import Webcam from "react-webcam";


export const WebcamScreen = () => {
    const webcamRef = React.useRef(null);
    const [imgSrc, setimgSrc] = React.useState(null);
  
    const capture = React.useCallback(
      () => {
        const imageSrc = webcamRef.current.getScreenshot();
        setimgSrc(imageSrc);
  
      },
      [webcamRef,setimgSrc]
    );
  
    return (
      <div>
        <Webcam
          audio={false}
          height={720}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          width={1280}
        />
        {imgSrc && (<img src = {imgSrc}/>) }
      </div>
    );
  }; 