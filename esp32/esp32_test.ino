// ============================================================
// 💡🔔 ESP32 LED + Buzzer Test
// ============================================================
// This code turns an LED and buzzer ON and OFF repeatedly.
//
// Purpose:
//   ✔ Check whether ESP32 is working
//   ✔ Check whether LED is connected properly
//   ✔ Check whether buzzer is connected properly
//   ✔ Test GPIO 23 and GPIO 22 output pins
//
// Behavior:
//   - LED and buzzer ON for 1 second
//   - LED and buzzer OFF for 1 second
//   - Repeats forever
// ============================================================


// ------------------------------------------------------------
// 🔌 Pin Configuration
// ------------------------------------------------------------
#define LED_PIN 23
// LED is connected to GPIO 23 on ESP32.

#define BUZZER_PIN 22
// Buzzer is connected to GPIO 22 on ESP32.


// ------------------------------------------------------------
// ⚙️ Setup Function
// ------------------------------------------------------------
// setup() runs only once when ESP32 starts or resets.
void setup() {
  pinMode(LED_PIN, OUTPUT);
  // Set GPIO 23 as an output pin.
  // ESP32 can now send HIGH or LOW signal to the LED.

  pinMode(BUZZER_PIN, OUTPUT);
  // Set GPIO 22 as an output pin.
  // ESP32 can now send HIGH or LOW signal to the buzzer.
}


// ------------------------------------------------------------
// 🔁 Loop Function
// ------------------------------------------------------------
// loop() runs again and again forever.
void loop() {
  digitalWrite(LED_PIN, HIGH);
  // Send HIGH signal to LED pin.
  // This turns the LED ON.

  digitalWrite(BUZZER_PIN, HIGH);
  // Send HIGH signal to buzzer pin.
  // This turns the buzzer ON.

  delay(1000);
  // Wait for 1000 milliseconds.
  // 1000 milliseconds = 1 second.


  digitalWrite(LED_PIN, LOW);
  // Send LOW signal to LED pin.
  // This turns the LED OFF.

  digitalWrite(BUZZER_PIN, LOW);
  // Send LOW signal to buzzer pin.
  // This turns the buzzer OFF.

  delay(1000);
  // Wait for 1 second before turning them ON again.
}
