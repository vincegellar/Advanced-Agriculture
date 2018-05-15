import PropTypes from 'prop-types'
import React, { Component } from 'react';
import './Plant.css';
import {
  LightIntensitySensor,
  SoilMoistureSensor,
  TemperatureSensor,
  WaterLevelSensor,
} from './Sensor';
import Icon from './Icon';

class Plant extends Component {
  render() {
    return (
        <div className="plant">
          <div className="name">
            <Icon name="flower"/> {this.props.name}
          </div>
          <div className="controls">
            <a href="/"><Icon name="information"/></a>
            <a href="/"><Icon name="settings"/></a>
          </div>
          <div className="sensors">
            <SoilMoistureSensor value={this.props.current_measurement.soil_moisture}/>
            <LightIntensitySensor value={this.props.current_measurement.light}/>
            <WaterLevelSensor value={this.props.current_measurement.water_level}/>
            <TemperatureSensor value={this.props.current_measurement.temp}/>
          </div>
        </div>
    );
  }
}

Plant.propTypes = {
  id: PropTypes.number.isRequired,
  name: PropTypes.string.isRequired,
  current_measurement: PropTypes.shape({
    soil_moisture: PropTypes.number,
    light: PropTypes.number,
    water_level: PropTypes.number,
    temp: PropTypes.number,
  }).isRequired,
  measurements: PropTypes.shape().isRequired,
  settings: PropTypes.shape().isRequired,
};

export default Plant;
