#include <WiFi.h>

#define LED_PIN 23
#define BUZZER_PIN 22

const char* ssid = "Nroa";
const char* password = "nroa@072015";

void setup() {
  Serial.begin(9600);

  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  digitalWrite(LED_PIN, LOW);
  digitalWrite(BUZZER_PIN, LOW);

  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);

  int attempt = 0;

  while (WiFi.status() != WL_CONNECTED && attempt < 20) {
    digitalWrite(LED_PIN, HIGH);
    delay(200);
    digitalWrite(LED_PIN, LOW);
    delay(300);

    Serial.print(".");
    attempt++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("");
    Serial.println("WiFi Connected Successfully!");
    Serial.print("ESP32 IP Address: ");
    Serial.println(WiFi.localIP());

    digitalWrite(LED_PIN, HIGH);

    digitalWrite(BUZZER_PIN, HIGH);
    delay(500);
    digitalWrite(BUZZER_PIN, LOW);
  } 
  else {
    Serial.println("");
    Serial.println("WiFi Connection Failed!");

    for (int i = 0; i < 3; i++) {
      digitalWrite(BUZZER_PIN, HIGH);
      delay(500);
      digitalWrite(BUZZER_PIN, LOW);
      delay(500);
    }
  }
}

void loop() {
}