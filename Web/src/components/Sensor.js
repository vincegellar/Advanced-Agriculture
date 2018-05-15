import React, { Component } from 'react';
import './Sensor.css';
import Icon from './Icon';

class Sensor extends Component {
  iconName = undefined;
  unit = undefined;

  render() {
    return (
        <div className="sensor">
          <Icon name={this.iconName}/>
          <span>
            {[this.props.value, this.unit].join(' ')}
          </span>
        </div>
    );
  }
}

class LightIntensitySensor extends Sensor {
  iconName = 'white-balance-sunny';
  unit = 'lx';
}

class SoilMoistureSensor extends Sensor {
  iconName = 'water';
  unit = '%';
}

class TemperatureSensor extends Sensor {
  iconName = 'gauge';
  unit = '°C';
}

class WaterLevelSensor extends Sensor {
  iconName = 'cup-water';
  unit = '%';
}

export { LightIntensitySensor, SoilMoistureSensor, TemperatureSensor, WaterLevelSensor };
