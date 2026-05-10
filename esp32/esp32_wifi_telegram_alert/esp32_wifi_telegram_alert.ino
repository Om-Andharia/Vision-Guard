#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <UniversalTelegramBot.h>

#define LED_PIN 23
#define BUZZER_PIN 22

const char* ssid = "Nroa";
const char* password = "nroa@072015";

#define BOT_TOKEN "8749292030:AAFJtYp3rYeMlwTOEUjcJJma6fAcKnsKrMw"
#define CHAT_ID "1849203854"

WiFiClientSecure client;
UniversalTelegramBot bot(BOT_TOKEN, client);

void successAlert() {
  digitalWrite(LED_PIN, HIGH);
  digitalWrite(BUZZER_PIN, HIGH);
  delay(300);
  digitalWrite(LED_PIN, LOW);
  digitalWrite(BUZZER_PIN, LOW);
}

void failureAlert() {
  for (int i = 0; i < 3; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(200);
    digitalWrite(BUZZER_PIN, LOW);
    delay(200);
  }
}

void setup() {
  Serial.begin(9600);
  delay(1000);

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

    client.setInsecure();

    Serial.println("Sending Telegram message...");

    bool messageSent = bot.sendMessage(
      CHAT_ID,
      "VisionGuard ESP32 Telegram test successful.",
      ""
    );

    if (messageSent) {
      Serial.println("Telegram message sent successfully.");
      successAlert();
    } else {
      Serial.println("Telegram message failed.");
      failureAlert();
    }
  } else {
    Serial.println("");
    Serial.println("WiFi Connection Failed!");
    failureAlert();
  }
}

void loop() {
}