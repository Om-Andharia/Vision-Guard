// ============================================================
// 🛡️ VisionGuard Phase 2 - Basic ESP32 Telegram Test
// ============================================================
// This code connects ESP32 to WiFi and sends one test message
// to Telegram using a Telegram Bot.
//
// Purpose:
//   ✔ Check WiFi connection
//   ✔ Check Telegram Bot Token
//   ✔ Check Chat ID
//   ✔ Confirm ESP32 can send Telegram messages
// ============================================================


// ------------------------------------------------------------
// 📦 Required Libraries
// ------------------------------------------------------------
#include <WiFi.h>                 
// Used to connect ESP32 to WiFi.

#include <WiFiClientSecure.h>     
// Used for secure HTTPS connection required by Telegram.

#include <UniversalTelegramBot.h> 
// Library used to send messages through Telegram Bot API.


// ------------------------------------------------------------
// 📶 WiFi Credentials
// ------------------------------------------------------------
// Replace these values with your actual WiFi name and password.
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";


// ------------------------------------------------------------
// 🤖 Telegram Bot Credentials
// ------------------------------------------------------------
// Replace these with your actual bot token and chat ID.
#define BOT_TOKEN "YOUR_BOT_TOKEN"
#define CHAT_ID "YOUR_CHAT_ID"


// ------------------------------------------------------------
// 🌐 Create Secure Client and Telegram Bot Object
// ------------------------------------------------------------
WiFiClientSecure client;
// Creates a secure internet client for HTTPS communication.

UniversalTelegramBot bot(BOT_TOKEN, client);
// Creates Telegram bot object using bot token and secure client.


// ------------------------------------------------------------
// ⚙️ Setup Function
// ------------------------------------------------------------
// setup() runs only once when ESP32 starts or resets.
void setup() {
  Serial.begin(9600);
  // Starts Serial Monitor communication at 9600 baud rate.

  delay(1000);
  // Small delay to allow ESP32 and Serial Monitor to become ready.


  // ----------------------------------------------------------
  // 📶 Connect ESP32 to WiFi
  // ----------------------------------------------------------
  Serial.println("Connecting to WiFi...");

  WiFi.begin(ssid, password);
  // Starts WiFi connection using given WiFi name and password.

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // This loop keeps running until ESP32 connects to WiFi.
  // A dot is printed every 0.5 seconds to show connection progress.


  // ----------------------------------------------------------
  // ✅ WiFi Connected Successfully
  // ----------------------------------------------------------
  Serial.println("");
  Serial.println("WiFi Connected Successfully!");

  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());
  // Prints ESP32 local IP address after successful connection.


  // ----------------------------------------------------------
  // 🔐 Allow HTTPS Connection
  // ----------------------------------------------------------
  client.setInsecure();
  // Telegram uses HTTPS.
  // This line allows ESP32 to connect without manually adding certificate.


  // ----------------------------------------------------------
  // 📩 Send Telegram Test Message
  // ----------------------------------------------------------
  Serial.println("Sending Telegram message...");

  bool messageSent = bot.sendMessage(
    CHAT_ID,
    "VisionGuard ESP32 Telegram test successful.",
    ""
  );
  // Sends message to the Telegram chat.
  //
  // messageSent will be:
  //   true  → message sent successfully
  //   false → message failed


  // ----------------------------------------------------------
  // 📊 Check Message Status
  // ----------------------------------------------------------
  if (messageSent) {
    Serial.println("Telegram message sent successfully.");
  } else {
    Serial.println("Telegram message failed.");
  }
}


// ------------------------------------------------------------
// 🔁 Loop Function
// ------------------------------------------------------------
// loop() runs repeatedly after setup().
// Here it is empty because we only want to send one test message
// when ESP32 starts.
void loop() {
}
