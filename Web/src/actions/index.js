export const INIT_PLANT = 'INIT_PLANT';
export const REFRESH_PLANT_MEASUREMENT = 'REFRESH_PLANT_MEASUREMENT';

export const initPlant = plant => ({
  type: INIT_PLANT,
  plant
});

export const refreshPlantMeasurement = (id, measurement) => ({
  type: REFRESH_PLANT_MEASUREMENT,
  id,
  measurement
});
