// ============================================================
// 🛡️ VisionGuard Phase 2 - ESP32 Telegram Test
// ============================================================
// This code connects ESP32 to WiFi and sends a test message
// to Telegram using a Telegram Bot.
//
// If message is sent successfully:
//   - LED and buzzer turn ON once
//
// If WiFi or Telegram message fails:
//   - Buzzer beeps 3 times
// ============================================================


// ------------------------------------------------------------
// 📦 Required Libraries
// ------------------------------------------------------------
#include <WiFi.h>                 // Used to connect ESP32 to WiFi
#include <WiFiClientSecure.h>     // Used for secure HTTPS connection
#include <UniversalTelegramBot.h> // Used to send Telegram messages


// ------------------------------------------------------------
// 🔌 Pin Configuration
// ------------------------------------------------------------
#define LED_PIN 23
#define BUZZER_PIN 22


// ------------------------------------------------------------
// 📶 WiFi Credentials
// ------------------------------------------------------------
// Replace these with your actual WiFi name and password.
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";


// ------------------------------------------------------------
// 🤖 Telegram Bot Details
// ------------------------------------------------------------
// Replace these with your Telegram bot token and chat ID.
#define BOT_TOKEN "YOUR_BOT_TOKEN"
#define CHAT_ID "YOUR_CHAT_ID"


// ------------------------------------------------------------
// 🌐 Telegram Client Setup
// ------------------------------------------------------------
WiFiClientSecure client;
UniversalTelegramBot bot(BOT_TOKEN, client);


// ------------------------------------------------------------
// ✅ Success Alert Function
// ------------------------------------------------------------
// Runs when Telegram message is sent successfully.
void successAlert() {
  digitalWrite(LED_PIN, HIGH);
  digitalWrite(BUZZER_PIN, HIGH);
  delay(300);

  digitalWrite(LED_PIN, LOW);
  digitalWrite(BUZZER_PIN, LOW);
}


// ------------------------------------------------------------
// ❌ Failure Alert Function
// ------------------------------------------------------------
// Runs when WiFi connection or Telegram message fails.
void failureAlert() {
  for (int i = 0; i < 3; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(200);

    digitalWrite(BUZZER_PIN, LOW);
    delay(200);
  }
}


// ------------------------------------------------------------
// ⚙️ Setup Function
// ------------------------------------------------------------
// setup() runs only once when ESP32 starts.
void setup() {
  Serial.begin(9600);
  delay(1000);

  // Set LED and buzzer pins as output pins.
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  // Keep LED and buzzer OFF at startup.
  digitalWrite(LED_PIN, LOW);
  digitalWrite(BUZZER_PIN, LOW);

  Serial.println("Connecting to WiFi...");

  // Start WiFi connection.
  WiFi.begin(ssid, password);

  int attempt = 0;

  // Try connecting to WiFi for limited attempts.
  while (WiFi.status() != WL_CONNECTED && attempt < 20) {
    // Blink LED while connecting.
    digitalWrite(LED_PIN, HIGH);
    delay(200);

    digitalWrite(LED_PIN, LOW);
    delay(300);

    Serial.print(".");
    attempt++;
  }

  // If WiFi is connected successfully.
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("");
    Serial.println("WiFi Connected Successfully!");

    Serial.print("ESP32 IP Address: ");
    Serial.println(WiFi.localIP());

    // Allows secure Telegram connection without certificate setup.
    client.setInsecure();

    Serial.println("Sending Telegram message...");

    // Send test message to Telegram.
    bool messageSent = bot.sendMessage(
      CHAT_ID,
      "VisionGuard ESP32 Telegram test successful.",
      ""
    );

    // Check whether Telegram message was sent.
    if (messageSent) {
      Serial.println("Telegram message sent successfully.");
      successAlert();
    } else {
      Serial.println("Telegram message failed.");
      failureAlert();
    }

  } else {
    // If WiFi did not connect.
    Serial.println("");
    Serial.println("WiFi Connection Failed!");
    failureAlert();
  }
}


// ------------------------------------------------------------
// 🔁 Loop Function
// ------------------------------------------------------------
// loop() is empty because this code only sends one test message
// when ESP32 starts.
void loop() {
}
