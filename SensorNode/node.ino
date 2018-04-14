#include <ArduinoJson.h>
#include <BH1750.h>
#include <DHTesp.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Wire.h>

#define SERIAL_BAUDRATE 115200
#define PIN_WATER_SOIL A0
#define PIN_WATER_SELECT D0
#define PIN_SOIL_SELECT D1
#define PIN_DHT D2
#define PIN_SDA D3
#define PIN_SCL D4
#define PIN_PUMP D5
#define PIN_LIGHT D6

#define WATER_0 200
#define WATER_100 500
#define SOIL_0 700
#define SOIL_100 200

#define ANNOUNCE_PORT 44460
#define CONTROLLER_PORT 8080

typedef struct Measurement {
  uint16_t light;
  uint8_t waterLevel;
  uint8_t soilMoisture;
  int8_t temperature;
  uint8_t humidity;
} Measurement;

DHTesp dht;
WiFiUDP udp;
HTTPClient http;
BH1750 lightMeter;
Measurement lastMeasurement;
char controllerIp[16] = {0};
StaticJsonBuffer<256> jsonBuffer;
int plantId;
bool water = false;
unsigned long waterStop;

void setup() {
  Serial.begin(SERIAL_BAUDRATE);

  // Initialize hardware
  Wire.begin(PIN_SCL, PIN_SDA);
  pinMode(PIN_WATER_SOIL, INPUT);
  pinMode(PIN_WATER_SELECT, OUTPUT);
  pinMode(PIN_SOIL_SELECT, OUTPUT);
  pinMode(PIN_PUMP, OUTPUT);
  pinMode(PIN_LIGHT, OUTPUT);
  dht.setup(PIN_DHT);
  lightMeter.begin();

  connectWifi("", "");
  detectController();
  configureNode();

  Serial.println("MAC:        " + WiFi.macAddress());
  Serial.print  ("IP:         "); Serial.println(WiFi.localIP());
  Serial.printf ("Controller: %s\n", controllerIp);
  Serial.printf ("Plant ID:   %d\n", plantId);

  Serial.println("Setup done\n\n");
}

uint8_t loopCounter = 0;
void loop() {
  if (water && millis() >= waterStop) water = false;
  digitalWrite(PIN_PUMP, water ? HIGH : LOW);

  // Send measurements every 2 seconds
  if (++loopCounter >= 20) {
    lastMeasurement = measure();
    Serial.printf("Water level:   %d %%\n", lastMeasurement.waterLevel);
    Serial.printf("Soil moisture: %d %%\n", lastMeasurement.soilMoisture);
    Serial.printf("Light:         %d lx\n", lastMeasurement.light);
    Serial.printf("Temperature:   %d C\n", lastMeasurement.temperature);
    Serial.printf("Humidity:      %d %%\n", lastMeasurement.humidity);
    Serial.print("\n\n");
    upload(lastMeasurement);
    loopCounter = 0;
  }
  
  delay(100);
}

void connectWifi(const char* ssid, const char* password) {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("");
}

void detectController() {
  udp.begin(ANNOUNCE_PORT);
  Serial.print("Detecting controller ");
  while (controllerIp[0] == 0) {
    Serial.print(".");
    int packetSize = udp.parsePacket();
    if (packetSize) {
      IPAddress ip = udp.remoteIP();
      sprintf(controllerIp, "%d.%d.%d.%d", ip[0], ip[1], ip[2], ip[3]);
      udp.stop();
    }
    delay(1000);
  }
  Serial.println("");
}

void configureNode() {
  char data[32];
  String mac = WiFi.macAddress();
  mac.replace(":", "");
  mac.toLowerCase();
  sprintf(data, "mac_address=%s", mac.c_str());  
  post("/configure", data, configureNodeSuccess);
}

void configureNodeSuccess(JsonObject& root) {
  plantId = root["plant_id"].as<int>();
}

void upload(Measurement m) {
  char data[128];
  sprintf(
    data, 
    "id=%d&water=%d&temperature=%d&humidity=%d&light=%d&moisture=%d",
    plantId,
    m.waterLevel,
    m.temperature,
    m.humidity,
    m.light,
    m.soilMoisture
  );
  post("/", data, uploadSuccess);
}

void uploadSuccess(JsonObject& root) {
  int waterTime = root["water_time"];
  bool lightOn = root["light_on"];
  
  if (waterTime > 0) {
    water = true;
    waterStop = millis() + waterTime * 1000;
  } else {
    water = false;
  }
  digitalWrite(PIN_LIGHT, lightOn ? HIGH : LOW);
}

void post(const char* path, char* data, void (*onSuccess)(JsonObject&)) {
  char url[64];
  sprintf(url, "http://%s:%d%s", controllerIp, CONTROLLER_PORT, path);
  http.begin(url);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  int httpStatus = http.POST(data);
  if (httpStatus == HTTP_CODE_OK) {
    onSuccess(jsonBuffer.parseObject(http.getString()));
  } else {
    Serial.printf("[HTTP] POST %s failed, error: %s\n", path, http.errorToString(httpStatus).c_str());
  }
  http.end();
}

Measurement measure() {
  Measurement m;

  digitalWrite(PIN_WATER_SELECT, HIGH);
  digitalWrite(PIN_SOIL_SELECT, LOW);
  m.waterLevel = max(0, min(100, (int) map(analogRead(PIN_WATER_SOIL), WATER_0, WATER_100, 0, 100)));
  digitalWrite(PIN_WATER_SELECT, LOW);
  digitalWrite(PIN_SOIL_SELECT, HIGH);
  m.soilMoisture = max(0, min(100, (int) map(analogRead(PIN_WATER_SOIL), SOIL_0, SOIL_100, 0, 100)));
  m.light = lightMeter.readLightLevel();
  m.temperature = dht.getTemperature();
  m.humidity = dht.getHumidity();

  return m;
}

