// ============================================================
// 📶 ESP32 Basic WiFi Connection Test
// ============================================================
// This code connects ESP32 to a WiFi network.
//
// Purpose:
//   ✔ Check whether ESP32 can connect to WiFi
//   ✔ Show connection progress in Serial Monitor
//   ✔ Print ESP32 IP address after successful connection
//
// This is usually the first test before adding Telegram,
// sensors, LED, buzzer, or IoT features.
// ============================================================


// ------------------------------------------------------------
// 📦 Required Library
// ------------------------------------------------------------
#include <WiFi.h>
// WiFi.h is the built-in ESP32 library used for WiFi connection.


// ------------------------------------------------------------
// 📶 WiFi Credentials
// ------------------------------------------------------------
// Replace these with your actual WiFi name and password.
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";


// ------------------------------------------------------------
// ⚙️ Setup Function
// ------------------------------------------------------------
// setup() runs only once when ESP32 starts or resets.
void setup() {
  Serial.begin(9600);
  // Starts Serial Monitor communication at 9600 baud rate.
  // Make sure Serial Monitor is also set to 9600 baud.

  delay(1000);
  // Small delay so ESP32 and Serial Monitor can become ready.


  // ----------------------------------------------------------
  // 🔄 Start WiFi Connection
  // ----------------------------------------------------------
  Serial.println("Connecting to WiFi...");

  WiFi.begin(ssid, password);
  // Starts connecting ESP32 to the WiFi network
  // using the given WiFi name and password.


  // ----------------------------------------------------------
  // ⏳ Wait Until WiFi Connects
  // ----------------------------------------------------------
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // This loop keeps running until ESP32 connects to WiFi.
  // A dot is printed every 0.5 seconds to show progress.


  // ----------------------------------------------------------
  // ✅ WiFi Connected Successfully
  // ----------------------------------------------------------
  Serial.println("");
  Serial.println("WiFi Connected Successfully!");

  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());
  // Prints the local IP address given to ESP32 by the WiFi router.
}


// ------------------------------------------------------------
// 🔁 Loop Function
// ------------------------------------------------------------
// loop() runs repeatedly after setup().
// It is empty because this code only tests WiFi connection once.
void loop() {
}
