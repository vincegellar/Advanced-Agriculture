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
const refreshPlants = function() {
  PlantAPI.getPlants().then((plants) => {
    Object.keys(plants).map((id) => {
      const action = Actions.initPlant(plants[id]);
      store.dispatch(action);
    });
  });
};
const refreshMeasurements = function() {
  PlantAPI.getCurrentMeasurements().then((measurements) => {
    Object.keys(measurements).map((id) => {
      const action = Actions.refreshPlantMeasurement(id, measurements[id]);
      store.dispatch(action);
    });
  });
};

refreshPlants();
setInterval(refreshMeasurements, 1000);
setInterval(refreshPlants, 60000);

ReactDOM.render(
    <Provider store={store}>
      <App/>
    </Provider>,
    document.getElementById('root')
);
registerServiceWorker();
