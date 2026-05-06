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
