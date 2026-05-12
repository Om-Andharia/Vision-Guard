// ============================================================
// 🔌 Arduino Serial LED + Buzzer Control
// ============================================================
// This code allows Arduino to receive commands from Python
// through USB Serial communication.
//
// Python sends:
//   '1' → Turn ON LED and buzzer
//   '0' → Turn OFF LED and buzzer
//
// This is useful in VisionGuard Phase 1, where Python detects
// an intruder and Arduino handles the physical alert output.
// ============================================================


// ------------------------------------------------------------
// 🔌 Pin Configuration
// ------------------------------------------------------------
int ledPin = 13;
// LED is connected to digital pin 13.
// On many Arduino boards, pin 13 also has a built-in LED.

int buzzerPin = 8;
// Buzzer is connected to digital pin 8.


// ------------------------------------------------------------
// ⚙️ Setup Function
// ------------------------------------------------------------
// setup() runs only once when Arduino starts or resets.
void setup() {
  pinMode(ledPin, OUTPUT);
  // Set LED pin as output.
  // Arduino can now turn the LED ON or OFF.

  pinMode(buzzerPin, OUTPUT);
  // Set buzzer pin as output.
  // Arduino can now turn the buzzer ON or OFF.

  Serial.begin(9600);
  // Start Serial communication at 9600 baud rate.
  //
  // Python code must also use the same baud rate:
  //   serial.Serial('COM3', 9600)
}


// ------------------------------------------------------------
// 🔁 Loop Function
// ------------------------------------------------------------
// loop() runs repeatedly after setup().
void loop() {

  // Check if Python has sent any data to Arduino.
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
      digitalWrite(ledPin, HIGH);
      // Turn LED ON.

      digitalWrite(buzzerPin, HIGH);
      // Turn buzzer ON.
    }


    // --------------------------------------------------------
    // ✅ Alert OFF Command
    // --------------------------------------------------------
    else if (data == '0') {
      digitalWrite(ledPin, LOW);
      // Turn LED OFF.

      digitalWrite(buzzerPin, LOW);
      // Turn buzzer OFF.
    }
  }
}
