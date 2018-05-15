import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux'
import { createStore } from 'redux'
import rootReducer from './reducers'
import './index.css';
import App from './components/App';
import registerServiceWorker from './registerServiceWorker';
import * as Actions from './actions';
import PlantAPI from './api/PlantAPI';

const store = createStore(rootReducer);

setInterval(() => {
  const loadedPlants = Object.keys(store.getState().plants);
  PlantAPI.getPlants().forEach(function(plant) {
    if (loadedPlants.indexOf(plant.id.toString()) === -1) {
      store.dispatch(Actions.plantInit(plant));
      loadedPlants.push(plant.id.toString());
    }
  });
  loadedPlants.forEach(function(id) {
    const sensors = PlantAPI.getPlantSensors(id);
    store.dispatch(Actions.plantSensorsRefresh(id, sensors));
  });
}, 1000);

ReactDOM.render(
    <Provider store={store}>
      <App/>
    </Provider>,
    document.getElementById('root')
);
registerServiceWorker();
