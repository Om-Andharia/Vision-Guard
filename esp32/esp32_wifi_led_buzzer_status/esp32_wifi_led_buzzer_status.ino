// ============================================================
// 📶 ESP32 WiFi Connection Test with LED and Buzzer
// ============================================================
// This code checks whether ESP32 can connect to WiFi.
//
// If WiFi connects successfully:
//   ✔ Serial Monitor shows success message
//   ✔ ESP32 IP address is printed
//   ✔ LED stays ON
//   ✔ Buzzer beeps once
//
// If WiFi connection fails:
//   ✔ Serial Monitor shows failure message
//   ✔ Buzzer beeps 3 times
//
// This is useful before adding Telegram or IoT alert features.
// ============================================================


// ------------------------------------------------------------
// 📦 Required Library
// ------------------------------------------------------------
#include <WiFi.h>
// WiFi.h is used to connect ESP32 to a WiFi network.


// ------------------------------------------------------------
// 🔌 Pin Configuration
// ------------------------------------------------------------
#define LED_PIN 23
#define BUZZER_PIN 22

// LED is connected to GPIO 23.
// Buzzer is connected to GPIO 22.


// ------------------------------------------------------------
// 📶 WiFi Credentials
// ------------------------------------------------------------
// Replace these with your actual WiFi name and password.
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";


// ------------------------------------------------------------
// ⚙️ Setup Function
// ------------------------------------------------------------
// setup() runs only once when ESP32 starts.
void setup() {
  Serial.begin(9600);
  // Starts Serial Monitor communication at 9600 baud rate.

  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  // Set LED and buzzer pins as output pins.

  digitalWrite(LED_PIN, LOW);
  digitalWrite(BUZZER_PIN, LOW);
  // Keep LED and buzzer OFF at the beginning.

  Serial.println("Connecting to WiFi...");

  WiFi.begin(ssid, password);
  // Start connecting ESP32 to WiFi using given name and password.

  int attempt = 0;
  // Counts how many times ESP32 has tried to connect.


  // ----------------------------------------------------------
  // 🔄 Try Connecting to WiFi
  // ----------------------------------------------------------
  while (WiFi.status() != WL_CONNECTED && attempt < 20) {

    // Blink LED while ESP32 is trying to connect.
    digitalWrite(LED_PIN, HIGH);
    delay(200);

    digitalWrite(LED_PIN, LOW);
    delay(300);

    Serial.print(".");
    // Print dot in Serial Monitor to show progress.

    attempt++;
    // Increase attempt count by 1.
  }


  // ----------------------------------------------------------
  // ✅ If WiFi Connected Successfully
  // ----------------------------------------------------------
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("");
    Serial.println("WiFi Connected Successfully!");

    Serial.print("ESP32 IP Address: ");
    Serial.println(WiFi.localIP());
    // Print ESP32 IP address.

    digitalWrite(LED_PIN, HIGH);
    // Keep LED ON to show WiFi is connected.

    digitalWrite(BUZZER_PIN, HIGH);
    delay(500);
    digitalWrite(BUZZER_PIN, LOW);
    // Buzzer beeps once for success.
  }


  // ----------------------------------------------------------
  // ❌ If WiFi Connection Failed
  // ----------------------------------------------------------
  else {
    Serial.println("");
    Serial.println("WiFi Connection Failed!");

    // Buzzer beeps 3 times to show failure.
    for (int i = 0; i < 3; i++) {
      digitalWrite(BUZZER_PIN, HIGH);
      delay(500);

      digitalWrite(BUZZER_PIN, LOW);
      delay(500);
    }
  }
}


// ------------------------------------------------------------
// 🔁 Loop Function
// ------------------------------------------------------------
// loop() runs repeatedly after setup().
// It is empty because WiFi connection is tested only once.
void loop() {
}
