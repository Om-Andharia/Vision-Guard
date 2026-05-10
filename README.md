# VisionGuard Phase 2 – ESP32 IoT Alert System

## Overview

VisionGuard Phase 2 upgrades the existing AI + Arduino intruder detection system into an **ESP32-based IoT alert system**.

In Phase 1, the system used Python, OpenCV, motion detection, face detection, and Arduino Uno for local LED and buzzer alerts.  
In Phase 2, the Arduino alert layer is extended using ESP32 to support **WiFi connectivity**, **local hardware alerts**, and future **IoT notifications** such as Telegram or email alerts.

---

## Phase 2 Goal

The goal of Phase 2 is to allow the Python AI detection system to send alert signals to ESP32, which can then trigger:

- LED alert
- Buzzer alert
- WiFi-based status indication
- Future Telegram/email notification

---

## System Flow

Laptop Camera
→ Python OpenCV AI Detection
→ Motion + Face Decision Logic
→ ESP32
→ LED + Buzzer Alert
→ Future IoT Notification

## Phase 1 vs Phase 2

| Feature | Phase 1 | Phase 2 |
|---|---|---|
| Microcontroller | Arduino Uno | ESP32 |
| Alert Type | Local LED + Buzzer | Local + IoT Alert |
| Connectivity | USB Serial | USB Serial + WiFi |
| Remote Notification | No | Planned |
| IoT Capability | No | Yes |

Current Progress
✅ Phase 1 completed
✅ Phase 2 Day 1 completed – ESP32 setup and hardware testing
✅ Phase 2 Day 2 completed – WiFi foundation and status testing
🔄 IoT notification integration pending

## Hardware Used
ESP32 WiFi + Bluetooth board
External LED
220Ω resistor
Active buzzer
Breadboard
Jumper wires
USB cable
Software Used
Arduino IDE
ESP32 board support package
WiFi.h library
Silicon Labs USB to UART Bridge VCP driver
Final Pin Configuration
Component	ESP32 GPIO Pin
LED	GPIO 23
Buzzer	GPIO 22
GND	Common Ground


## Day 1 Summary – ESP32 Setup

On Day 1, the ESP32 foundation was prepared and tested.

Completed work:

Installed ESP32 board support in Arduino IDE
Fixed COM port issue by installing Silicon Labs USB to UART Bridge VCP driver
Verified successful code upload to ESP32
Tested external LED on GPIO 23
Tested buzzer on GPIO 22
Tested Serial Monitor command mode

The LED pin was changed from GPIO 2 to GPIO 23 because GPIO 2 did not work on this ESP32 board.

## Day 2 Summary – WiFi Foundation

On Day 2, ESP32 WiFi connectivity was tested.

Completed work:

Connected ESP32 to WiFi using WiFi.h
Printed WiFi connection status in Serial Monitor
Displayed ESP32 local IP address
Used LED as WiFi connection status indicator
Used buzzer as success/failure indicator
Tested WiFi failure case using wrong password

During WiFi connection, the LED blinked.
After successful connection, the LED stayed ON and the buzzer beeped once.
During failure, the buzzer beeped three times.

## Day 3 Summary - ESP32 - LED and Buzzer Testing

Phase 2 Day 3 focused on integrating the Python AI detection system with ESP32 using serial communication.

The ESP32 was kept in Serial Command Mode, where it responds to commands received from Python through the COM port. The command ‘1’ turns ON the LED and buzzer, while the command ‘0’ turns them OFF.

The pyserial library was installed and tested successfully. A separate Python serial test file was created to verify that Python could control the ESP32 directly. The test confirmed that Python was able to turn ON and OFF the ESP32-connected LED and buzzer.

After successful serial testing, the ESP32 serial communication logic was added to the main OpenCV AI intruder detection code. A reusable send_to_esp32() function was created to send alert commands from Python to ESP32.

The ESP32 alert was triggered only when both motion and face detection conditions were satisfied. This ensured that the alert was not activated by motion alone or face detection alone.

A full system test was completed successfully. The laptop camera detected motion and face, Python confirmed the intruder condition, and ESP32 activated the LED and buzzer. When the system returned to safe condition, Python sent the OFF command and ESP32 turned off the alert.

This completed the first full AI-to-ESP32 integration for VisionGuard Phase 2.

## Day 4 Summary - IoT Notification through Telegram

Phase 2 Day 4 was completed successfully.

A Telegram bot was created using BotFather, the bot token was generated, and the Chat ID was collected using the Telegram Bot API. The required Arduino libraries, including UniversalTelegramBot and ArduinoJson, were installed.

The ESP32 successfully connected to WiFi and sent a Telegram test message. The message was received on the Telegram app, confirming that ESP32-to-Telegram communication was working.

LED and buzzer confirmation were added. The LED blinked during WiFi connection attempts, and after successful Telegram message delivery, the LED blinked once while the buzzer beeped once. Failure cases were also tested using a wrong WiFi password and wrong bot token. In both cases, the ESP32 handled the error condition and triggered warning beeps.

Finally, sensitive credentials such as WiFi password, Telegram bot token, and Chat ID were removed from GitHub-ready code and replaced with placeholder values.

This completes the Telegram notification preparation stage of VisionGuard Phase 2.

## Security Note

This project uses WiFi credentials, Telegram Bot Token, and Telegram Chat ID for IoT notification testing.

For security reasons, real credentials are not uploaded to GitHub.  
Before running the code, replace the placeholder values with your own private credentials:

```cpp
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

#define BOT_TOKEN "YOUR_BOT_TOKEN"
#define CHAT_ID "YOUR_CHAT_ID"
