import React, { Component } from 'react';
import './App.css';
import Plant from './Plant';
import '../api/PlantAPI';

class App extends Component {
  render() {
    return (
        <div className="app">
          <h1>Plants</h1>
          <Plant/>
          <Plant/>
          <Plant/>
          <Plant/>
          <Plant/>
          <div className="clear"/>
        </div>
    );
  }
}

export default App;
