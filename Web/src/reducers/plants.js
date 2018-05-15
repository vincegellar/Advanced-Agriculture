import * as ActionTypes from '../actions';

const plants = (state = {}, action) => {
  switch (action.type) {
    case ActionTypes.INIT_PLANT:
      return Object.assign({}, state, {
        [action.plant.id]: action.plant
      });

    case ActionTypes.REFRESH_PLANT_MEASUREMENT:
      if (typeof(state[action.id]) === 'undefined') return state;
      return Object.assign({}, state, {
        [action.id]: Object.assign({}, state[action.id], {
          current_measurement: action.measurement
        })
      });

    default:
      return state;
  }
};

export default plants;
