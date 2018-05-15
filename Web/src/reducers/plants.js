import * as ActionTypes from '../actions';

const plants = (state = {}, action) => {
  switch (action.type) {
    case ActionTypes.PLANT_INIT:
      return Object.assign({}, state, {
        [action.plant.id]: {info: action.plant, sensors: {}}
      });

    case ActionTypes.PLANT_SENSORS_REFRESH:
      if (typeof(state[action.id]) === 'undefined') return state;
      return Object.assign({}, state, {
        [action.id]: Object.assign({}, state[action.id], {sensors: action.sensors})
      });

    default:
      return state;
  }
};

export default plants;
