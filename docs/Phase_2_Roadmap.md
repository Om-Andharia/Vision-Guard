# VisionGuard Phase 2 Roadmap – ESP32 IoT Alert System

## Goal

Upgrade VisionGuard from local Arduino-based alerting to an ESP32-based IoT alert system with WiFi-enabled remote notification capability.

## Phase 2 Tasks

### 1. ESP32 Setup
- Install ESP32 board support in Arduino IDE
- Select correct ESP32 board and COM port
- Upload blink test code

### 2. ESP32 LED + Buzzer Test
- Connect LED and active buzzer to ESP32
- Test GPIO-based alert control

### 3. WiFi Connection Test
- Connect ESP32 to local WiFi
- Print connection status and IP address on Serial Monitor

### 4. Python to ESP32 Communication
- Send alert signal from Python to ESP32
- Test serial or WiFi-based command control

### 5. Remote Alert System
- Add Telegram or email notification
- Send alert message when intruder is detected

### 6. Future Expansion
- Cloud image storage
- Authorized vs unauthorized face recognition
