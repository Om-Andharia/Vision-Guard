# VisionGuard – AI Intruder Detection System

VisionGuard is an AI + Embedded Systems + IoT project that detects intruders using real-time motion detection and face detection. In Phase 1, alerts were triggered using Arduino Uno. In Phase 2, the system was upgraded with ESP32, WiFi connectivity, LED and buzzer alerts, and Telegram IoT notification.

## Phase 1 Status

Phase 1 of VisionGuard has been completed successfully. The system detects motion and faces using Python and OpenCV, sends serial commands to Arduino Uno, and triggers LED and buzzer hardware alerts in real time.

Current Phase 1 capabilities:
- Real-time motion detection
- Face detection using OpenCV
- Motion memory for stable alerts
- Arduino Uno LED and buzzer control
- Evidence image capture with cooldown
- Motion visualization on video feed

## Features

- Real-time webcam monitoring
- Motion detection using frame differencing
- Face detection using OpenCV Haar Cascade
- Motion memory for stable detection
- Arduino Uno LED and buzzer alert
- Cooldown-based image capture
- Real-time status display
- Motion area visualization

## Hardware Used

- Arduino Uno R3
- LED
- 220Ω resistor
- Active buzzer
- Breadboard
- Jumper wires
- Laptop webcam

## Software Used

- Python
- OpenCV
- PySerial
- Arduino IDE

## System Workflow

Camera → Motion Detection → Face Detection → Decision Logic → Python Serial Communication → Arduino Alert

## Installation

pip install -r requirements.txt

## Arduino Setup

1. Upload `arduino/command_mode.ino` to Arduino Uno.
2. Connect LED to pin 13.
3. Connect active buzzer to pin 8.
4. Select correct COM port in Arduino IDE.

## Run the Project

1. Connect Arduino Uno to laptop.
2. Close Arduino Serial Monitor.
3. Open `code/face_detection.py`.
4. Change COM port if needed:
   ```python
   arduino = serial.Serial("COM3", 9600)
5. Run
   python code/face_detection.py
6. Press q to exit.


## Output

When motion and face detection conditions are satisfied:

- LED turns ON
- Buzzer turns ON
- Intruder image is saved in the `captures/` folder
- System status changes to ALERT

## Phase 1 Architecture

![Phase 1 Architecture](images/phase_1_architecture.png)

## Hardware Prototype

![Prototype Circuit](images/prototype_circuit.jpeg)

## Working Demo

![Complete Demo](images/working_demo.jpeg)


# Phase 2 – ESP32 IoT Alert System

## Phase 2 Status

Phase 2 of VisionGuard has been completed successfully. The system has been upgraded from an Arduino Uno local alert system to an ESP32-based IoT alert system with Telegram notification support.

Current Phase 2 capabilities:

- ESP32 hardware alert integration
- LED alert on GPIO 23
- Buzzer alert on GPIO 22
- Python-to-ESP32 serial communication
- ESP32 WiFi connectivity
- Telegram bot notification
- 15-second Telegram cooldown to prevent alert spam
- Camera blocked / too dark detection
- ESP32 disconnection handling
- Safe shutdown handling
- GitHub-safe credential placeholders

---

## Phase 1 vs Phase 2

| Feature             | Phase 1            | Phase 2                     |
| ------------------- | ------------------ | --------------------------- |
| Microcontroller     | Arduino Uno        | ESP32                       |
| Alert Type          | Local LED + Buzzer | Local + IoT Alert           |
| Connectivity        | USB Serial         | USB Serial + WiFi           |
| Remote Notification | No                 | Telegram Notification       |
| IoT Capability      | No                 | Yes                         |
| Anti-Spam Logic     | No                 | 15-second Telegram cooldown |
| Failure Handling    | Basic              | Improved                    |

---

## Phase 2 System Architecture

```text
Laptop Camera
      ↓
Python OpenCV
      ↓
Motion Detection + Face Detection
      ↓
Intruder Decision Logic
      ↓
Python Serial Command
      ↓
ESP32
      ↓
LED + Buzzer Alert
      ↓
WiFi
      ↓
Telegram Notification
```

## Phase 2 Hardware Used

- ESP32 WiFi + Bluetooth board
- External LED
- 220Ω resistor
- Active buzzer
- Breadboard
- Jumper wires
- USB cable
- Laptop webcam

---

## Phase 2 Software Used

- Python
- OpenCV
- PySerial
- Arduino IDE
- ESP32 board support package
- `WiFi.h`
- `WiFiClientSecure.h`
- `UniversalTelegramBot`
- `ArduinoJson`
- Telegram Bot API
- Silicon Labs USB to UART Bridge VCP driver

---

## Phase 2 Final Pin Configuration

| Component | ESP32 GPIO Pin |
| --------- | -------------- |
| LED       | GPIO 23        |
| Buzzer    | GPIO 22        |
| GND       | Common Ground  |

---

## Phase 2 Output

When motion and face detection conditions are satisfied:

- Python sends command `1` to ESP32
- ESP32 turns ON LED
- ESP32 turns ON buzzer
- ESP32 sends Telegram alert
- Intruder image is saved in the `captures/` folder
- System status changes to `ALERT`

When the system becomes safe:

- Python sends command `0` to ESP32
- ESP32 turns OFF LED
- ESP32 turns OFF buzzer
- System becomes ready for the next alert

## ESP32 LED and Buzzer Setup

![ESP32 LED and Buzzer Setup](phase2/images/esp32_led_and_buzzer.jpeg)

```markdown
## Future Scope - Phase 3

- Send captured intruder image through Telegram
- Add timestamp and location to Telegram alerts
- Add authorized vs unauthorized face recognition
- Add WiFi reconnection logic
- Add event logging file for alert history
- Improve face detection using DNN, MediaPipe, or YOLO
- Build a simple dashboard for live system status
```
