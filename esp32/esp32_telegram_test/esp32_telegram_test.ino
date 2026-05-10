#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <UniversalTelegramBot.h>

// WiFi details

const char* ssid = "Nroa";
const char* password = "nroa@072015";


// Telegram bot details

#define BOT_TOKEN "8749292030:AAFJtYp3rYeMlwTOEUjcJJma6fAcKnsKrMw"
#define CHAT_ID "1849203854"

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
