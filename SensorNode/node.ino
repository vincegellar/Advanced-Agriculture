#include <DHTesp.h>

#include <Wire.h>
#include <BH1750.h>

#define SERIAL_BAUD 9600
#define PIN_DHT T0
#define PIN_MOISTURE A3
#define PIN_PUMP T1
#define PIN_LAMP T2

BH1750 lightMeter(0x23);
DHTesp dht;

void setup(){

  Serial.begin(SERIAL_BAUD);

  // Initialize the I2C bus (BH1750 library doesn't do this automatically)
  Wire.begin();
  // On esp8266 you can select SCL and SDA pins using Wire.begin(D4, D3);
  lightMeter.begin(BH1750::ONE_TIME_HIGH_RES_MODE);
  dht.setup(PIN_DHT);
}

void loop() {
  delay(max(1000, dht.getMinimumSamplingPeriod()));
  
  uint16_t lux = lightMeter.readLightLevel();
  float humidity = dht.getHumidity();
  float temperature = dht.getTemperature();
  
  
  Serial.print("Light: ");
  Serial.print(lux);
  Serial.println(" lx");

  Serial.print("Temperature: ");
  Serial.print(temperature, 1);
  Serial.println("C");
  
  Serial.print("Humidity: ");
  Serial.print(humidity, 1);
  Serial.println("%");

  float moisture = 100.0 * (4096 - analogRead(PIN_MOISTURE)) / 4096;
  Serial.print("Moisture: ");
  Serial.print(moisture);
  Serial.println("%");
}
