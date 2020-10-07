import React, { useState } from "react";
import ToggleButton from 'react-toggle-button';
import styled from "styled-components";

const RowWrapper = styled.div`
    align-items: center;
    display: flex;
    flex-direction: row;
`;

const TextWrapper = styled.div`
    padding-right: 15px;
`;

const ToggleSendEmail = (props) =>{

    const [toggleSendMail, setToggleSendMail] = useState(props.toggled);

    function onToggle(value){
        setToggleSendMail(!value);
        props.onToggle(!value);
    }
    
    return(
        <RowWrapper>
            <TextWrapper>
                <h5>Envio de Estadisticas por Mail</h5>
            </TextWrapper>
            <ToggleButton
                inactiveLabel="No"
                activeLabel="Si"
                colors={{
                activeThumb: {
                    base: 'rgb(62,130,247)',
                },
                inactiveThumb: {
                    base: 'rgb(62,130,247)',
                },
                active: {
                    base: 'rgb(62,130,247)',
                    hover: 'rgb(177, 191, 215)',
                },
                inactive: {
                    base: 'rgb(65,66,68)',
                    hover: 'rgb(95,96,98)',
                }
                }}
                value={toggleSendMail}
                onToggle={(value) => {onToggle(value)}}
            />
        </RowWrapper>
    );
}

export default ToggleSendEmail;