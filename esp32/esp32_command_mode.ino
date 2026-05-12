// ============================================================
// 🔌 ESP32 Serial LED + Buzzer Control
// ============================================================
// This code allows ESP32 to receive commands from Python
// through USB Serial communication.
//
// Python sends:
//   '1' → Turn ON LED and buzzer
//   '0' → Turn OFF LED and buzzer
//
// This is useful for VisionGuard because Python detects the
// intruder, and ESP32 handles the physical alert output.
// ============================================================


// ------------------------------------------------------------
// 🔌 Pin Configuration
// ------------------------------------------------------------
#define LED_PIN 23
#define BUZZER_PIN 22

// LED is connected to GPIO 23.
// Buzzer is connected to GPIO 22.


// ------------------------------------------------------------
// ⚙️ Setup Function
// ------------------------------------------------------------
// setup() runs once when ESP32 starts or resets.
void setup() {
  pinMode(LED_PIN, OUTPUT);
  // Set LED pin as an output pin.

  pinMode(BUZZER_PIN, OUTPUT);
  // Set buzzer pin as an output pin.

  Serial.begin(9600);
  // Start Serial communication at 9600 baud rate.
  // Python code must also use the same baud rate.
}


// ------------------------------------------------------------
// 🔁 Loop Function
// ------------------------------------------------------------
// loop() keeps running again and again.
void loop() {

  // Check whether Python has sent any data to ESP32.
  if (Serial.available() > 0) {

    char data = Serial.read();
    // Read one character from Serial.
    //
    // Expected values:
    //   '1' = alert ON
    //   '0' = alert OFF


    // --------------------------------------------------------
    // 🚨 Alert ON Command
    // --------------------------------------------------------
    if (data == '1') {
      digitalWrite(LED_PIN, HIGH);
      // Turn LED ON.

      digitalWrite(BUZZER_PIN, HIGH);
      // Turn buzzer ON.
    }


    // --------------------------------------------------------
    // ✅ Alert OFF Command
    // --------------------------------------------------------
    else if (data == '0') {
      digitalWrite(LED_PIN, LOW);
      // Turn LED OFF.

      digitalWrite(BUZZER_PIN, LOW);
      // Turn buzzer OFF.
    }
  }
}
