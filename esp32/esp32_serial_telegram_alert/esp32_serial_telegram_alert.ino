#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <UniversalTelegramBot.h>

unsigned long lastTelegramTime = 0;
unsigned long telegramCooldown = 15000; // 15 seconds

#define LED_PIN 23
#define BUZZER_PIN 22

// WiFi credentials
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

// Telegram credentials
#define BOT_TOKEN "YOUR_BOT_TOKEN"
#define CHAT_ID "YOUR_CHAT_ID"

WiFiClientSecure client;
UniversalTelegramBot bot(BOT_TOKEN, client);

bool alertSent = false;

void connectToWiFi() {
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
  } else {
    Serial.println("");
    Serial.println("WiFi Connection Failed!");
  }
}

void successBeep() {
  digitalWrite(BUZZER_PIN, HIGH);
  delay(300);
  digitalWrite(BUZZER_PIN, LOW);
}

void failureBeep() {
  for (int i = 0; i < 3; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(200);
    digitalWrite(BUZZER_PIN, LOW);
    delay(200);
  }
}

void sendTelegramAlert() {
  if (WiFi.status() == WL_CONNECTED) {
    bool messageSent = bot.sendMessage(
      CHAT_ID,
      "🚨 VisionGuard Alert!\n\nIntruder detected.\nDetection: Motion + Face confirmed.\nAlert Source: ESP32 IoT Module.\nStatus: LED and buzzer activated.",
      ""
    );

    if (messageSent) {
      Serial.println("Telegram alert sent successfully.");
      successBeep();
    } else {
      Serial.println("Telegram alert failed.");
      failureBeep();
    }
  } else {
    Serial.println("WiFi not connected. Telegram alert skipped.");
    failureBeep();
  }
}

void setup() {
  Serial.begin(9600);
  delay(1000);

  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  digitalWrite(LED_PIN, LOW);
  digitalWrite(BUZZER_PIN, LOW);

  connectToWiFi();

  Serial.println("ESP32 Serial + Telegram Alert System Ready.");
}

void loop() {
  if (Serial.available() > 0) {
    char data = Serial.read();

    if (data == '1') {
      digitalWrite(LED_PIN, HIGH);
      digitalWrite(BUZZER_PIN, HIGH);

      Serial.println("Alert command received from Python.");

      if (!alertSent && millis() - lastTelegramTime > telegramCooldown) {
    sendTelegramAlert();
    alertSent = true;
    lastTelegramTime = millis();
  }
    }

    else if (data == '0') {
      digitalWrite(LED_PIN, LOW);
      digitalWrite(BUZZER_PIN, LOW);

      alertSent = false;

      Serial.println("Safe command received. Alert OFF.");
    }
  }
}