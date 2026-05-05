# VisionGuard Phase 2 – ESP32 IoT Alert System

## Overview

VisionGuard Phase 2 upgrades the existing AI + Arduino intruder detection system into an **ESP32-based IoT alert system**.

In Phase 1, VisionGuard successfully detected intruders using Python, OpenCV, motion detection, face detection, and Arduino Uno hardware alerts. Phase 2 focuses on replacing or extending the Arduino Uno alert layer with an **ESP32**, enabling future WiFi-based alerts, remote notifications, and IoT functionality.

---

## Phase 2 Goal

The main goal of Phase 2 is to build an ESP32-based alert system that can receive signals from the Python AI detection system and trigger hardware alerts such as:

- LED alert
- Buzzer alert
- Future WiFi notification
- Future Telegram/email alert

---

## Phase 2 System Flow

```text
Laptop Camera
→ Python OpenCV AI Detection
→ Motion + Face Decision Logic
→ ESP32
→ LED + Buzzer Alert
→ Future IoT Notification

Difference Between Phase 1 and Phase 2
Feature	              Phase 1	            Phase 2
Microcontroller	    Arduino Uno	        ESP32
Alert Type	        Local LED + buzzer	Local + IoT alert
Connectivity	      USB serial	        USB serial + WiFi
Remote Notification	No	                Planned
IoT Capability	    No	                Yes
