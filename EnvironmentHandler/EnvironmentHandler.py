from flask import Flask, request

app = Flask(__name__)

water = 0
temperature = 0.0
humidity = 0
light = 0
moisture = 0

measurement_count = 0


@app.route('/', methods=['POST'])
def send_data():
    global water
    global temperature
    global humidity
    global light
    global moisture
    water += int(request.values['water'])
    temperature += float(request.values['temperature'])
    humidity += int(request.values['humidity'])
    light = int(request.values['light'])
    moisture = int(request.values['moisture'])

    global measurement_count
    measurement_count += 1

    return '{}'


if __name__ == '__main__':
    app.run()
