import React, { Component } from 'react';
import './PlantList.css';
import Plant from '../containers/Plant';

class PlantList extends Component {
  render() {
    const plants = this.props.plants;
    return (
        <div className="plant-list">
          {
            Object.keys(plants).map((id) => (<Plant key={id} {...plants[id]}/>))
          }
        </div>
    );
  }
}

export default PlantList;
