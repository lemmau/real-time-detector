import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import TextField from '@material-ui/core/TextField';
import Config from "Config";

const Graph = (props) => {

    return(
    <Plot
        data={props.graphData}
        layout={ {width: 700, height: 440, title: 'Detections - ' + props.date, barmode: 'stack'} }
      />
      );
};

export const ModalGraph = () => {

  const [ date, setDate ] = useState('2020-08-30');
  const [ graphData, setGraphData ] = useState({});

  useEffect(() => {

    async function getStatistics(){
    
      const requestOptions = {
        method: "GET",
      };

      const response = await fetch(
        Config.backendEndpoint + "/statistic/" + date,
        requestOptions
      );
      const data = await response.json();

      for(var element in data){
        data[element].type = 'bar'
      }
    
      setGraphData(data)
    };

    getStatistics();
  }, [date]);

  return(
    <>
      <TextField
          id="date"
          label="Date"
          type="date"
          defaultValue={date}
          onChange={(e) => setDate(e.target.value)}
      />

      <Graph
        date={date}
        graphData={graphData}
      />
    </>
    );
};
