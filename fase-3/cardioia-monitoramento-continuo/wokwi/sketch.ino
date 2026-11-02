#include <Arduino.h>
#include <DHT.h>
#include <PubSubClient.h>
#include <WiFi.h>

// CardioIA Fase 3 — todos os dados são sintéticos e educacionais.
namespace Config {
constexpr char WIFI_SSID[] = "Wokwi-GUEST";
constexpr char WIFI_PASSWORD[] = "";
constexpr char MQTT_HOST[] = "broker.hivemq.com";
constexpr uint16_t MQTT_PORT = 1883;
constexpr char DEVICE_ID[] = "cardioia-esp32-01";

constexpr uint8_t DHT_PIN = 15;
constexpr uint8_t DHT_TYPE = DHT22;
constexpr uint8_t BPM_PIN = 34;
constexpr uint8_t FORCE_OFFLINE_PIN = 4;
constexpr uint8_t ALERT_LED_PIN = 2;

constexpr uint32_t SAMPLE_INTERVAL_MS = 5000;
constexpr uint32_t WIFI_RETRY_INTERVAL_MS = 5000;
constexpr uint32_t MQTT_RETRY_INTERVAL_MS = 3000;
constexpr size_t BUFFER_CAPACITY = 720;  // 1 hora a uma amostra/5 s.
constexpr size_t MAX_SYNC_PER_LOOP = 20;

constexpr uint16_t BPM_MIN = 40;
constexpr uint16_t BPM_MAX = 180;
constexpr uint16_t BPM_LOW_ALERT = 50;
constexpr uint16_t BPM_HIGH_ALERT = 120;
constexpr float TEMP_HIGH_ALERT_C = 38.0F;
}  // namespace Config

enum AlertCode : uint8_t {
  ALERT_NONE = 0,
  ALERT_BPM_LOW = 1 << 0,
  ALERT_BPM_HIGH = 1 << 1,
  ALERT_TEMP_HIGH = 1 << 2,
  ALERT_SENSOR_ERROR = 1 << 3,
};

struct Sample {
  uint32_t sequence;
  uint32_t capturedAtMs;
  float temperatureC;
  float humidityPct;
  uint16_t bpm;
  uint8_t alertCode;
};

class SampleRingBuffer {
 public:
  void push(const Sample& sample) {
    if (count_ == Config::BUFFER_CAPACITY) {
      head_ = (head_ + 1) % Config::BUFFER_CAPACITY;
      --count_;
      ++dropped_;
    }
    const size_t tail = (head_ + count_) % Config::BUFFER_CAPACITY;
    samples_[tail] = sample;
    ++count_;
  }

  bool empty() const { return count_ == 0; }
  size_t size() const { return count_; }
  uint32_t dropped() const { return dropped_; }
  const Sample& front() const { return samples_[head_]; }

  void pop() {
    if (count_ == 0) return;
    head_ = (head_ + 1) % Config::BUFFER_CAPACITY;
    --count_;
  }

 private:
  Sample samples_[Config::BUFFER_CAPACITY]{};
  size_t head_ = 0;
  size_t count_ = 0;
  uint32_t dropped_ = 0;
};

DHT dht(Config::DHT_PIN, Config::DHT_TYPE);
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
SampleRingBuffer offlineBuffer;

uint32_t nextSequence = 1;
uint32_t lastSampleAt = 0;
uint32_t lastWifiAttemptAt = 0;
uint32_t lastMqttAttemptAt = 0;
bool forcedOffline = false;

const char* topicTelemetry = "cardioia/fase3/cardioia-esp32-01/telemetria";
const char* topicAlert = "cardioia/fase3/cardioia-esp32-01/alerta";
const char* topicStatus = "cardioia/fase3/cardioia-esp32-01/status";

uint8_t calculateAlert(float temperatureC, uint16_t bpm, bool sensorValid) {
  uint8_t code = ALERT_NONE;
  if (!sensorValid) code |= ALERT_SENSOR_ERROR;
  if (sensorValid && temperatureC > Config::TEMP_HIGH_ALERT_C) code |= ALERT_TEMP_HIGH;
  if (bpm < Config::BPM_LOW_ALERT) code |= ALERT_BPM_LOW;
  if (bpm > Config::BPM_HIGH_ALERT) code |= ALERT_BPM_HIGH;
  return code;
}

const char* alertLabel(uint8_t code) {
  if (code == ALERT_NONE) return "normal";
  if (code & ALERT_SENSOR_ERROR) return "sensor_error";
  if (code & ALERT_TEMP_HIGH) return "high_temperature";
  if (code & ALERT_BPM_HIGH) return "high_bpm";
  if (code & ALERT_BPM_LOW) return "low_bpm";
  return "multiple_alerts";
}

Sample collectSample() {
  const float temperature = dht.readTemperature();
  const float humidity = dht.readHumidity();
  const bool sensorValid = !isnan(temperature) && !isnan(humidity);
  const int rawBpm = analogRead(Config::BPM_PIN);
  const uint16_t bpm = map(rawBpm, 0, 4095, Config::BPM_MIN, Config::BPM_MAX);

  Sample sample{};
  sample.sequence = nextSequence++;
  sample.capturedAtMs = millis();
  sample.temperatureC = sensorValid ? temperature : -999.0F;
  sample.humidityPct = sensorValid ? humidity : -1.0F;
  sample.bpm = bpm;
  sample.alertCode = calculateAlert(temperature, bpm, sensorValid);
  return sample;
}

void printSample(const Sample& sample, const char* source) {
  Serial.printf(
      "SAMPLE seq=%lu source=%s temp=%.1fC humidity=%.1f%% bpm=%u alert=%s queued=%u dropped=%lu\n",
      static_cast<unsigned long>(sample.sequence), source, sample.temperatureC,
      sample.humidityPct, sample.bpm, alertLabel(sample.alertCode),
      static_cast<unsigned>(offlineBuffer.size()),
      static_cast<unsigned long>(offlineBuffer.dropped()));
}

bool publishSample(const Sample& sample, const char* source) {
  char payload[320];
  snprintf(payload, sizeof(payload),
           "{\"device_id\":\"%s\",\"sequence\":%lu,\"uptime_ms\":%lu,"
           "\"temperature_c\":%.1f,\"humidity_pct\":%.1f,\"bpm\":%u,"
           "\"alert_code\":%u,\"alert\":\"%s\",\"source\":\"%s\","
           "\"buffer_pending\":%u,\"dropped_samples\":%lu}",
           Config::DEVICE_ID, static_cast<unsigned long>(sample.sequence),
           static_cast<unsigned long>(sample.capturedAtMs), sample.temperatureC,
           sample.humidityPct, sample.bpm, sample.alertCode,
           alertLabel(sample.alertCode), source,
           static_cast<unsigned>(offlineBuffer.size()),
           static_cast<unsigned long>(offlineBuffer.dropped()));

  const bool telemetryAccepted = mqttClient.publish(topicTelemetry, payload, false);
  if (!telemetryAccepted) return false;

  if (sample.alertCode != ALERT_NONE) {
    mqttClient.publish(topicAlert, payload, false);
  }
  return true;
}

void publishStatus(const char* state) {
  char payload[220];
  snprintf(payload, sizeof(payload),
           "{\"device_id\":\"%s\",\"state\":\"%s\",\"buffer_pending\":%u,"
           "\"dropped_samples\":%lu,\"uptime_ms\":%lu}",
           Config::DEVICE_ID, state, static_cast<unsigned>(offlineBuffer.size()),
           static_cast<unsigned long>(offlineBuffer.dropped()),
           static_cast<unsigned long>(millis()));
  mqttClient.publish(topicStatus, payload, true);
}

void serviceWifi() {
  const bool buttonRequestsOffline = digitalRead(Config::FORCE_OFFLINE_PIN) == LOW;
  if (buttonRequestsOffline) {
    if (!forcedOffline) {
      forcedOffline = true;
      WiFi.disconnect();
      Serial.println("EDGE: modo offline forçado; coletas continuarão no buffer.");
    }
    return;
  }

  if (forcedOffline) {
    forcedOffline = false;
    lastWifiAttemptAt = 0;
    Serial.println("EDGE: modo online liberado; iniciando reconexão.");
  }

  if (WiFi.status() == WL_CONNECTED) return;
  if (millis() - lastWifiAttemptAt < Config::WIFI_RETRY_INTERVAL_MS) return;

  lastWifiAttemptAt = millis();
  WiFi.begin(Config::WIFI_SSID, Config::WIFI_PASSWORD, 6);
  Serial.println("WIFI: tentativa de conexão iniciada.");
}

void serviceMqtt() {
  if (forcedOffline || WiFi.status() != WL_CONNECTED) return;
  if (mqttClient.connected()) {
    mqttClient.loop();
    return;
  }
  if (millis() - lastMqttAttemptAt < Config::MQTT_RETRY_INTERVAL_MS) return;

  lastMqttAttemptAt = millis();
  String clientId = String(Config::DEVICE_ID) + "-" + String(static_cast<uint32_t>(ESP.getEfuseMac()), HEX);
  if (mqttClient.connect(clientId.c_str(), topicStatus, 0, true,
                         "{\"device_id\":\"cardioia-esp32-01\",\"state\":\"offline_unexpected\"}")) {
    Serial.println("MQTT: conectado ao broker; sincronização liberada.");
    publishStatus("online");
  } else {
    Serial.printf("MQTT: conexão falhou, rc=%d.\n", mqttClient.state());
  }
}

void syncBufferedSamples() {
  if (!mqttClient.connected()) return;
  size_t sentThisLoop = 0;
  while (!offlineBuffer.empty() && sentThisLoop < Config::MAX_SYNC_PER_LOOP) {
    const Sample& sample = offlineBuffer.front();
    if (!publishSample(sample, "buffered")) {
      Serial.println("MQTT: publicação recusada; amostra mantida no buffer.");
      break;
    }
    printSample(sample, "synced");
    offlineBuffer.pop();
    ++sentThisLoop;
    mqttClient.loop();
  }
  if (sentThisLoop > 0) publishStatus("online_syncing");
}

void setup() {
  Serial.begin(115200);
  pinMode(Config::FORCE_OFFLINE_PIN, INPUT_PULLUP);
  pinMode(Config::ALERT_LED_PIN, OUTPUT);
  digitalWrite(Config::ALERT_LED_PIN, LOW);
  analogReadResolution(12);

  dht.begin();
  WiFi.mode(WIFI_STA);
  mqttClient.setServer(Config::MQTT_HOST, Config::MQTT_PORT);
  mqttClient.setBufferSize(512);

  Serial.println("CardioIA Fase 3 iniciado — dados exclusivamente sintéticos.");
  serviceWifi();
}

void loop() {
  serviceWifi();
  serviceMqtt();
  syncBufferedSamples();

  if (millis() - lastSampleAt >= Config::SAMPLE_INTERVAL_MS) {
    lastSampleAt = millis();
    const Sample sample = collectSample();
    digitalWrite(Config::ALERT_LED_PIN,
                 sample.alertCode == ALERT_NONE ? LOW : HIGH);

    // Toda leitura entra primeiro na fila: há um único caminho de entrega e
    // nenhuma amostra é removida antes da confirmação local do cliente MQTT.
    offlineBuffer.push(sample);
    printSample(sample, mqttClient.connected() ? "queued_online" : "queued_offline");
    syncBufferedSamples();
  }

  delay(10);
}

