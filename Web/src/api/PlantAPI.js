class PlantAPI {

  static getPlants() {
    return [
      {id: 1, name: 'Plant #1'},
      {id: 2, name: 'Plant #2'},
      {id: 3, name: 'Plant #3'},
    ];
  }

  static getPlantSensors(plantId) {
    return {
      soilMoisture: 67,
      temperature: 27,
      waterLevel: 43,
      lightIntensity: 3,
    };
  }

}

export default PlantAPI;
