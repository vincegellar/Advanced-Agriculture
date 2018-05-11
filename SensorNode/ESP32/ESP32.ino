#include <DHTesp.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>

#define ANALOG_PIN_FENYEROSSEG 35
#define ANALOG_PIN_TALAJNEDVESSEG 34
#define ANALOG_PIN_TAVOLSAG_TRIGGER 33
#define ANALOG_PIN_TAVOLSAG_VALASZ 25
#define LED 32
#define DIGITAL_PIN 4
#define PIN_DHT 4
#define ANNOUNCE_PORT 44460
#define CONTROLLER_PORT 8080

typedef struct Measurement {
  uint16_t light;
  uint8_t waterLevel;
  uint8_t soilMoisture;
  int8_t temperature;
  uint8_t humidity;
} Measurement;

int analog_fenyerosseg = 0;
int analog_talajnedvesseg = 0;
int digital_value=0;
float duration, distance;
int plantId;
bool water = false;
unsigned long waterStop;
Measurement lastMeasurement;
DHTesp dht;
WiFiUDP udp;
HTTPClient http;
char controllerIp[16] = {0};
StaticJsonBuffer<256> jsonBuffer;


void setup()
{
  Serial.begin(115200);
  delay(1000); // give me time to bring up serial monitor
  Serial.println("ESP32 Analog IN Test");
  dht.setup(PIN_DHT);
  
  pinMode(LED, OUTPUT);
  pinMode(ANALOG_PIN_TAVOLSAG_TRIGGER, OUTPUT);
  pinMode(ANALOG_PIN_TAVOLSAG_VALASZ, INPUT);

  connectWifi("UPC7027718", "ESQCXRFZ");
  detectController();
  configureNode();

  Serial.println("MAC:        " + WiFi.macAddress());
  Serial.print  ("IP:         "); Serial.println(WiFi.localIP());
  Serial.printf ("Controller: %s\n", controllerIp);
  Serial.printf ("Plant ID:   %d\n", plantId);

  Serial.println("Setup done\n\n");
}
uint8_t loopCounter = 0;
void loop()
{
  if (water && millis() >= waterStop) water = false;
  //digitalWrite(PIN_PUMP, water ? HIGH : LOW);
  lastMeasurement = measure();
    Serial.printf("Water level:   %d %%\n", lastMeasurement.waterLevel);
    Serial.printf("Soil moisture: %d %%\n", lastMeasurement.soilMoisture);
    Serial.printf("Light:         %d lx\n", lastMeasurement.light);
    Serial.printf("Temperature:   %d C\n", lastMeasurement.temperature);
    Serial.printf("Humidity:      %d %%\n", lastMeasurement.humidity);
    Serial.print("\n\n");
    upload(lastMeasurement);
  if (analog_fenyerosseg<3500)
    digitalWrite(LED, HIGH);
  if (analog_fenyerosseg>3500)
    digitalWrite(LED, LOW);
  delay(5000);
}

void connectWifi(const char* ssid, const char* password) {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi ");
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
  //digitalWrite(PIN_LIGHT, lightOn ? HIGH : LOW);
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

Measurement measure(){
  Measurement m;
  
  float humidity = dht.getHumidity();
  float temperature = dht.getTemperature();
  analog_fenyerosseg = analogRead(ANALOG_PIN_FENYEROSSEG);
  analog_talajnedvesseg = analogRead(ANALOG_PIN_TALAJNEDVESSEG);
  digital_value = digitalRead(DIGITAL_PIN);
  digitalWrite(ANALOG_PIN_TAVOLSAG_TRIGGER, LOW);
  delayMicroseconds(2);
  digitalWrite(ANALOG_PIN_TAVOLSAG_TRIGGER, HIGH);
  delayMicroseconds(10);
  digitalWrite(ANALOG_PIN_TAVOLSAG_TRIGGER, LOW);
  duration = pulseIn(ANALOG_PIN_TAVOLSAG_VALASZ, HIGH);
  distance = (duration / 2) * 0.0343;
  m.waterLevel=distance;
  m.soilMoisture=analog_talajnedvesseg;
  m.light=analog_fenyerosseg;
  m.temperature=temperature;
  m.humidity=humidity;
  
  return m;
}

