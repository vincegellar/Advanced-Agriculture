# Advanced Agriculture

**_Warning: The project is still in early development, so expect some features and documentation to be missing, or not work correctly._**

## What is this all about?
Use a Raspberry PI to monitor, and care for your plants. Connect the sensors to NodeMCUs to connect many plants to one Raspberry.

## Features:
- Automated Watering
- Automated Light Provisioning
- E-mail warnings
- Web Statistics
- Set Dark Hours
- Set Silent Hours

## Hardware:
- Raspberry PI 3 Model B / Raspberry PI Zero W
- NodeMCU ESP8266 / ESP32

### Sensors:
- Temperature & Humidity: DHT11
- Soil Moisture
- Light Inensity: BH1750FVI
- Water Level In The Tank

### Actuators:
- 12V Submersible Pump
- Full Spectrum 10W Pink LED

## How to install?
Run the following on the Raspberry PI:
```bash
curl -s https://raw.githubusercontent.com/vincegellar/Advanced-Agriculture/master/install.sh | bash
```

## License:

Advanced Agriculture: A plant automation IoT system.
    Copyright (C) 2018  Viktor Bán (viktor.ban@gmail.com), Vince Gellár (gellar.vince@gmail.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
