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
            <Icon name="flower"/> {this.props.info.name}
          </div>
          <div className="controls">
            <a href="/"><Icon name="information"/></a>
            <a href="/"><Icon name="settings"/></a>
          </div>
          <div className="sensors">
            <SoilMoistureSensor value={this.props.sensors.soilMoisture}/>
            <LightIntensitySensor value={this.props.sensors.lightIntensity}/>
            <WaterLevelSensor value={this.props.sensors.waterLevel}/>
            <TemperatureSensor value={this.props.sensors.temperature}/>
          </div>
        </div>
    );
  }
}

Plant.propTypes = {
  info: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string,
  }).isRequired,
  sensors: PropTypes.shape({
    soilMoisture: PropTypes.number,
    lightIntensity: PropTypes.number,
    waterLevel: PropTypes.number,
    temperature: PropTypes.number,
  }).isRequired
};

export default Plant;
