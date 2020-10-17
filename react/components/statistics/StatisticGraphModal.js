import React, { useState, useEffect } from "react";
import Plot from "react-plotly.js";
import TextField from "@material-ui/core/TextField";
import Config from "Config";
import styled from "styled-components";
import PropTypes from "prop-types";
import Moment from "moment";

const Graph = (props) => {
  return (
    <Plot
      data={props.graphData}
      layout={{
        width: 700,
        height: 440,
        title: "Detecciones - " + props.date,
        barmode: "stack",
      }}
    />
  );
};

Graph.propTypes = {
  date: PropTypes.string.isRequired,
  graphData: PropTypes.array.isRequired,
};

const NotFoundWrapper = styled.div`
  align-items: center;
  display: flex;
  justify-content: center;
  width: 700px;
  height: 440px;
  font-size: 25px;
`;

export const ModalGraph = () => {
  const [date, setDate] = useState(Moment(Date.now()).format("YYYY-MM-DD"));
  const [graphData, setGraphData] = useState({});
  const [hasDataAvailable, setHasDataAvailable] = useState(false);

  useEffect(() => {
    async function getStatistics() {
      const requestOptions = {
        method: "GET",
      };

      const response = await fetch(
        Config.backendEndpoint + "/statistic/" + date,
        requestOptions
      );
      const graphData = await response.json();

      for (var element of graphData) {
        element.type = "bar";
        element.marker = {'color': element.color};
      }

      setGraphData(graphData);
      setHasDataAvailable(Object.entries(graphData).length !== 0);
    }

    getStatistics();
  }, [date]);

  return (
    <>
      <TextField
        id="date"
        label="Fecha"
        type="date"
        defaultValue={date}
        onChange={(e) => setDate(e.target.value)}
      />

      {hasDataAvailable ? (
        <Graph date={date} graphData={graphData} />
      ) : (
        <NotFoundWrapper>
          <p>No hay Datos para Mostrar</p>
        </NotFoundWrapper>
      )}
    </>
  );
};
