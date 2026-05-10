#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <UniversalTelegramBot.h>

const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

#define BOT_TOKEN "YOUR_BOT_TOKEN"
#define CHAT_ID "YOUR_CHAT_ID"

WiFiClientSecure client;
UniversalTelegramBot bot(BOT_TOKEN, client);

void setup() {
  Serial.begin(9600);
  delay(1000);

  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi Connected Successfully!");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());

  // Required for HTTPS connection
  client.setInsecure();

  Serial.println("Sending Telegram message...");

  bool messageSent = bot.sendMessage(
    CHAT_ID,
    "VisionGuard ESP32 Telegram test successful.",
    ""
  );

  if (messageSent) {
    Serial.println("Telegram message sent successfully.");
  } else {
    Serial.println("Telegram message failed.");
  }
}

void loop() {
  // put your main code here, to run repeatedly:

}
