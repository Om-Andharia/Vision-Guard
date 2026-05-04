# VisionGuard – AI Intruder Detection System

VisionGuard is an AI + Embedded Systems project that detects intruders using real-time motion detection and face detection. When an intruder is detected, Python sends a serial command to Arduino Uno, which triggers an LED and buzzer alert.

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

## Output

When motion and face detection conditions are satisfied:

- LED turns ON
- Buzzer turns ON
- Intruder image is saved in the `captures/` folder
- System status changes to ALERT

## Future Scope

- ESP32 WiFi alert system
- Telegram or email notifications
- Authorized vs unauthorized face recognition
