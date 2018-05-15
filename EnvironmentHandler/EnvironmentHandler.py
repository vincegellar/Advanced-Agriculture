from flask import Flask, request, jsonify
from datetime import datetime
from BLL.announcer import Announcer
from BLL.pll import PlantLogic

app = Flask(__name__)


class Measurement:
    def __init__(self):
        self.start = datetime.now()
        self.water = 0
        self.temperature = 0.0
        self.humidity = 0
        self.light = 0
        self.moisture = 0
        self.measurement_count = 0


hourly_measurements = {}
last_measurement = {}
logic_layer = PlantLogic()


@app.route('/', methods=['POST'])
def send_data():
    plant_id = int(request.values['id'])
    water = int(request.values['water'])
    temperature = float(request.values['temperature'])
    humidity = int(request.values['humidity'])
    light = int(request.values['light'])
    moisture = int(request.values['moisture'])
    global hourly_measurements
    if plant_id not in hourly_measurements:
        hourly_measurements[plant_id] = Measurement()
    hourly_measurements[plant_id].water += water
    hourly_measurements[plant_id].temperature += temperature
    hourly_measurements[plant_id].humidity += humidity
    hourly_measurements[plant_id].light += light
    hourly_measurements[plant_id].moisture += moisture
    hourly_measurements[plant_id].measurement_count += 1
    if plant_id not in last_measurement:
        last_measurement[plant_id] = Measurement()
    last_measurement[plant_id].water = water
    last_measurement[plant_id].temperature = temperature
    last_measurement[plant_id].humidity = humidity
    last_measurement[plant_id].light = light
    last_measurement[plant_id].moisture = moisture
    elapsed_measurement_time = hourly_measurements[plant_id].start - datetime.now()
    actuator_response = {'light_on': False, 'water_time': 0}
    if elapsed_measurement_time.seconds >= 3600:
        measurement_count = hourly_measurements[plant_id].measurement_count
        average_water = int(round(hourly_measurements[plant_id].water / measurement_count))
        average_temp = hourly_measurements[plant_id].temperature / measurement_count
        average_humidity = int(round(hourly_measurements[plant_id].humidity / measurement_count))
        average_light = int(round(hourly_measurements[plant_id].light / measurement_count))
        average_moisture = int(round(hourly_measurements[plant_id].moisture / measurement_count))
        global logic_layer
        light_on, water_time = logic_layer.commit_measurement(plant_id, average_water, average_temp, average_humidity,
                                                              average_light, average_moisture)
        actuator_response = {'light_on': light_on, 'water_time': water_time}
        hourly_measurements[plant_id] = Measurement()
    return jsonify(actuator_response)


@app.route('/configure', methods=['POST'])
def configure():
    mac_address = request.values['mac_address']
    plant_id = logic_layer.configure(mac_address)
    response = {'plant_id': plant_id}
    return jsonify(response)


@app.route('/web-ui/plants', methods=['GET'])
def get_plants():
    response = logic_layer.get_plants()
    for plant_id, measurement in last_measurement.items():
        response[plant_id]['current_measurement'] = {'water_level': measurement.water,
                                                     'temp': measurement.temperature,
                                                     'humidity': measurement.humidity,
                                                     'light': measurement.light,
                                                     'soil_moisture': measurement.moisture}
    return jsonify(response)


@app.route('/web-ui/current', methods=['GET'])
def get_current():
    response = {}
    for plant_id, measurement in last_measurement.items():
        response[plant_id]['current_measurement'] = {'water_level': measurement.water,
                                                     'temp': measurement.temperature,
                                                     'humidity': measurement.humidity,
                                                     'light': measurement.light,
                                                     'soil_moisture': measurement.moisture}
    return jsonify(response)


@app.route('/web-ui/history', methods=['GET'])
def get_history():
    response = logic_layer.get_history()
    return jsonify(response)


@app.route('/web-ui/settings', methods=['GET'])
def get_settings():
    plant_id = int(request.values['id'])
    response = logic_layer.get_settings(plant_id)
    return jsonify(response)


@app.route('/web-ui/settings', methods=['POST'])
def post_settings():
    response = logic_layer.post_settings()
    return jsonify(response)


announcer_thread = Announcer()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
