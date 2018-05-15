import React, { Component } from 'react';
import './App.css';
import PlantList from '../containers/PlantList';

class App extends Component {
  render() {
    return (
        <div className="app">
          <h1>Plants</h1>
          <PlantList/>
        </div>
    );
  }
}
export default App;
