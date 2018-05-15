export const PLANT_INIT = 'PLANT_INIT';
export const PLANT_SENSORS_REFRESH = 'PLANT_SENSORS_REFRESH';

export const plantInit = plant => ({
  type: PLANT_INIT,
  plant
});

export const plantSensorsRefresh = (id, sensors) => ({
  type: PLANT_SENSORS_REFRESH,
  id,
  sensors
});
