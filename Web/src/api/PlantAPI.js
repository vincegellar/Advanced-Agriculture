class PlantAPI {

  static getPlants() {
    return fetch('api/plants').then((response) => {
      return response.json();
    });
  }

  static getCurrentMeasurements() {
    return fetch('api/current').then((response) => {
      return response.json();
    });
  }

  static getMeasurementHistory() {
    return fetch('api/history').then((response) => {
      return response.json();
    });
  }

  static getSettings(plantId) {
    return fetch(`api/settings?id=${plantId}`).then((response) => {
      return response.json();
    });
  }

  static updateSettings(plantId, settings) {
    return fetch(`api/settings?id=${plantId}`, {
      method: 'POST',
      body: JSON.stringify(settings),
      headers: {
        'content-type': 'application/json',
      },
    }).then((response) => {
      return response.json();
    });
  }

}

export default PlantAPI;
