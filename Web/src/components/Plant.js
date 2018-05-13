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
            <Icon name="flower"/> Plant name
          </div>
          <div className="controls">
            <a href="/"><Icon name="information"/></a>
            <a href="/"><Icon name="settings"/></a>
          </div>
          <div className="sensors">
            <SoilMoistureSensor value={70}/>
            <LightIntensitySensor value={432}/>
            <WaterLevelSensor value={100}/>
            <TemperatureSensor value={26}/>
          </div>
        </div>
    );
  }
}

export default Plant;
