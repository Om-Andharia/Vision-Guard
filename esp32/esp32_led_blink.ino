// ============================================================
// 💡 ESP32 Basic LED Blink Test
// ============================================================
// This code turns an LED ON and OFF repeatedly.
//
// Purpose:
//   ✔ Check whether ESP32 is working
//   ✔ Check whether LED is connected properly
//   ✔ Test GPIO 23 output
//
// LED behavior:
//   - LED ON for 1 second
//   - LED OFF for 1 second
//   - Repeats forever
// ============================================================


// ------------------------------------------------------------
// 🔌 Pin Configuration
// ------------------------------------------------------------
#define LED_PIN 23
// LED is connected to GPIO 23 on ESP32.


// ------------------------------------------------------------
// ⚙️ Setup Function
// ------------------------------------------------------------
// setup() runs only once when ESP32 starts or resets.
void setup() {
  pinMode(LED_PIN, OUTPUT);
  // Set GPIO 23 as an output pin.
  // Output means ESP32 can send HIGH or LOW signal to this pin.
}


// ------------------------------------------------------------
// 🔁 Loop Function
// ------------------------------------------------------------
// loop() runs again and again forever.
void loop() {
  digitalWrite(LED_PIN, HIGH);
  // Send HIGH signal to GPIO 23.
  // This turns the LED ON.

  delay(1000);
  // Wait for 1000 milliseconds.
  // 1000 milliseconds = 1 second.

  digitalWrite(LED_PIN, LOW);
  // Send LOW signal to GPIO 23.
  // This turns the LED OFF.

  delay(1000);
  // Wait for 1 second before turning LED ON again.
}
