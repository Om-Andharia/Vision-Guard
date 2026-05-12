// ============================================================
// 🛡️ VisionGuard Phase 2
//    ESP32 Serial + Telegram Alert System
// ============================================================
// This ESP32 code receives commands from Python through Serial.
//
// Python sends:
//   '1' → Intruder detected
//   '0' → System safe
//
// When ESP32 receives '1':
//   ✔ LED turns ON
//   ✔ Buzzer turns ON
//   ✔ Telegram alert is sent
//
// When ESP32 receives '0':
//   ✔ LED turns OFF
//   ✔ Buzzer turns OFF
//   ✔ System becomes ready for next alert
//
// Telegram cooldown:
//   A Telegram message is sent only once every 15 seconds.
//   This prevents message spam.
// ============================================================


// ------------------------------------------------------------
// 📦 Required Libraries
// ------------------------------------------------------------
#include <WiFi.h>                 // Used to connect ESP32 to WiFi
#include <WiFiClientSecure.h>     // Used for secure HTTPS connection
#include <UniversalTelegramBot.h> // Used to send Telegram bot messages


// ------------------------------------------------------------
// ⏱️ Telegram Cooldown Variables
// ------------------------------------------------------------
unsigned long lastTelegramTime = 0;
// Stores the last time a Telegram message was sent.

unsigned long telegramCooldown = 15000;
// 15000 milliseconds = 15 seconds.
// Telegram alert will not be sent repeatedly within this time.


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
// 🤖 Telegram Bot Credentials
// ------------------------------------------------------------
// Replace these with your Telegram Bot Token and Chat ID.
#define BOT_TOKEN "YOUR_BOT_TOKEN"
#define CHAT_ID "YOUR_CHAT_ID"


// ------------------------------------------------------------
// 🌐 Telegram Client Setup
// ------------------------------------------------------------
WiFiClientSecure client;
UniversalTelegramBot bot(BOT_TOKEN, client);


// ------------------------------------------------------------
// 🚦 Alert State Variable
// ------------------------------------------------------------
bool alertSent = false;
// Tracks whether Telegram alert has already been sent
// for the current intruder event.
//
// false → alert not sent yet
// true  → alert already sent


// ------------------------------------------------------------
// 📶 Function: Connect ESP32 to WiFi
// ------------------------------------------------------------
void connectToWiFi() {
  Serial.println("Connecting to WiFi...");

  // Start WiFi connection using given SSID and password.
  WiFi.begin(ssid, password);

  int attempt = 0;

  // Try connecting to WiFi for limited attempts.
  while (WiFi.status() != WL_CONNECTED && attempt < 20) {

    // Blink LED while ESP32 is trying to connect.
    digitalWrite(LED_PIN, HIGH);
    delay(200);

    digitalWrite(LED_PIN, LOW);
    delay(300);

    Serial.print(".");
    attempt++;
  }

  // If WiFi connected successfully.
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("");
    Serial.println("WiFi Connected Successfully!");

    Serial.print("ESP32 IP Address: ");
    Serial.println(WiFi.localIP());

    // Allows HTTPS connection to Telegram without certificate setup.
    client.setInsecure();
  }

  // If WiFi failed.
  else {
    Serial.println("");
    Serial.println("WiFi Connection Failed!");
  }
}


// ------------------------------------------------------------
// ✅ Function: Success Beep
// ------------------------------------------------------------
// Runs when Telegram alert is sent successfully.
void successBeep() {
  digitalWrite(BUZZER_PIN, HIGH);
  delay(300);

  digitalWrite(BUZZER_PIN, LOW);
}


// ------------------------------------------------------------
// ❌ Function: Failure Beep
// ------------------------------------------------------------
// Runs when Telegram alert fails or WiFi is not connected.
void failureBeep() {
  for (int i = 0; i < 3; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(200);

    digitalWrite(BUZZER_PIN, LOW);
    delay(200);
  }
}


// ------------------------------------------------------------
// 📩 Function: Send Telegram Alert
// ------------------------------------------------------------
void sendTelegramAlert() {

  // First check whether ESP32 is connected to WiFi.
  if (WiFi.status() == WL_CONNECTED) {

    // Send alert message to Telegram.
    bool messageSent = bot.sendMessage(
      CHAT_ID,
      "🚨 VisionGuard Alert!\n\nIntruder detected.\nDetection: Motion + Face confirmed.\nAlert Source: ESP32 IoT Module.\nStatus: LED and buzzer activated.",
      ""
    );

    // If message was sent successfully.
    if (messageSent) {
      Serial.println("Telegram alert sent successfully.");
      successBeep();
    }

    // If message failed.
    else {
      Serial.println("Telegram alert failed.");
      failureBeep();
    }
  }

  // If WiFi is not connected.
  else {
    Serial.println("WiFi not connected. Telegram alert skipped.");
    failureBeep();
  }
}


// ------------------------------------------------------------
// ⚙️ Setup Function
// ------------------------------------------------------------
// setup() runs once when ESP32 starts.
void setup() {
  Serial.begin(9600);
  delay(1000);

  // Set LED and buzzer as output devices.
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  // Keep both OFF at startup.
  digitalWrite(LED_PIN, LOW);
  digitalWrite(BUZZER_PIN, LOW);

  // Connect ESP32 to WiFi.
  connectToWiFi();

  Serial.println("ESP32 Serial + Telegram Alert System Ready.");
}


// ------------------------------------------------------------
// 🔁 Loop Function
// ------------------------------------------------------------
// loop() runs again and again.
// It waits for commands from Python.
void loop() {

  // Check if Python has sent any data through Serial.
  if (Serial.available() > 0) {

    // Read one character from Serial.
    char data = Serial.read();


    // --------------------------------------------------------
    // 🚨 If Python Sends '1' → Intruder Alert
    // --------------------------------------------------------
    if (data == '1') {

      // Turn ON LED and buzzer.
      digitalWrite(LED_PIN, HIGH);
      digitalWrite(BUZZER_PIN, HIGH);

      Serial.println("Alert command received from Python.");

      // Send Telegram alert only if:
      //   1. Alert was not already sent for this event
      //   2. 15 seconds cooldown has passed
      if (!alertSent && millis() - lastTelegramTime > telegramCooldown) {
        sendTelegramAlert();

        alertSent = true;
        // Mark alert as already sent for this event.

        lastTelegramTime = millis();
        // Store current time as last Telegram alert time.
      }
    }


    // --------------------------------------------------------
    // ✅ If Python Sends '0' → Safe State
    // --------------------------------------------------------
    else if (data == '0') {

      // Turn OFF LED and buzzer.
      digitalWrite(LED_PIN, LOW);
      digitalWrite(BUZZER_PIN, LOW);

      alertSent = false;
      // Reset alert state.
      // Now system is ready to send Telegram alert for next event.

      Serial.println("Safe command received. Alert OFF.");
    }
  }
}
