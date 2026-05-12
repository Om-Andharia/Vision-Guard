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

## Day 5 Summary - Python + Telegram IoT Notification

Phase 2 Day 5 focused on full integration between Python AI detection, ESP32 hardware alerting, and Telegram IoT notification.

Phase 2 Day 5 was completed successfully.

The Python OpenCV AI detection system was connected with the ESP32 through Serial communication. The ESP32 was programmed to receive commands from Python and perform both local and remote alert actions.

When Python detected both motion and face, it sent command 1 to the ESP32. The ESP32 then activated the LED and buzzer and sent a Telegram alert message. When the system returned to safe condition, Python sent command 0, and the ESP32 turned OFF the LED and buzzer.

During testing, repeated Telegram alerts were observed when movement continued or restarted. To solve this, a 15-second Telegram cooldown was added using lastTelegramTime and telegramCooldown. This prevented alert spam while still allowing new alerts after the cooldown period.

Private details such as WiFi password, Telegram Bot Token, and Chat ID were removed from GitHub-ready code and replaced with placeholders.

This completed the full AI + ESP32 + Telegram IoT integration for VisionGuard Phase 2.

## Current System Architecture

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

## Security Note

This project uses WiFi credentials, Telegram Bot Token, and Telegram Chat ID for IoT notification testing.

For security reasons, real credentials are not uploaded to GitHub.  
Before running the code, replace the placeholder values with your own private credentials:

```cpp
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

#define BOT_TOKEN "YOUR_BOT_TOKEN"
#define CHAT_ID "YOUR_CHAT_ID"
```
# VisionGuard Phase 2 – ESP32 IoT Alert System

## Overview

**VisionGuard Phase 2** upgrades the existing AI + Arduino intruder detection system into an **ESP32-based IoT alert system**.

In **Phase 1**, the system used Python, OpenCV, motion detection, face detection, and Arduino Uno to trigger local LED and buzzer alerts.

In **Phase 2**, the alert layer is extended using an ESP32. This adds WiFi connectivity, Telegram-based IoT notification, local hardware alerting, cooldown-based anti-spam logic, and reliability improvements.

---

## Phase 2 Goal

The goal of Phase 2 is to allow the Python AI detection system to send alert signals to the ESP32. The ESP32 then performs both local and remote alert actions.

The system can trigger:

- LED alert
- Buzzer alert
- Telegram notification
- WiFi-based IoT alert
- Safe shutdown and failure handling

---

## Current System Architecture

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
Phase 1 vs Phase 2
Feature	Phase 1	Phase 2
Microcontroller	Arduino Uno	ESP32
Alert Type	Local LED + Buzzer	Local + IoT Alert
Connectivity	USB Serial	USB Serial + WiFi
Remote Notification	No	Telegram Notification
IoT Capability	No	Yes
Anti-Spam Logic	No	15-second Telegram cooldown
Failure Handling	Basic	Improved
Current Progress
✅ Phase 1 – AI + Arduino Local Alert System Completed
✅ Phase 2 Day 1 – ESP32 Hardware Setup Completed
✅ Phase 2 Day 2 – ESP32 WiFi Foundation Completed
✅ Phase 2 Day 3 – Python AI + ESP32 Serial Integration Completed
✅ Phase 2 Day 4 – ESP32 Telegram Notification Test Completed
✅ Phase 2 Day 5 – Full AI + ESP32 + Telegram Integration Completed
✅ Phase 2 Day 6 – Final Testing, Reliability, and Documentation Completed
Hardware Used
Component	Purpose
ESP32 WiFi + Bluetooth Board	Main IoT alert controller
External LED	Visual alert indicator
Active Buzzer	Audio alert indicator
220Ω Resistor	LED current protection
Breadboard	Circuit prototyping
Jumper Wires	Hardware connections
USB Cable	ESP32 programming and serial communication
Laptop Camera	Video input for intruder detection
Mobile Phone	Telegram alert receiver
Software and Libraries Used
Software / Library	Purpose
Python	AI detection logic
OpenCV	Motion detection, face detection, webcam processing
pyserial	Python-to-ESP32 serial communication
Arduino IDE	ESP32 programming
ESP32 Board Support Package	ESP32 development support
WiFi.h	ESP32 WiFi connectivity
WiFiClientSecure.h	Secure HTTPS communication
UniversalTelegramBot.h	Telegram Bot API communication
ArduinoJson	JSON support for Telegram library
Telegram App	Remote alert receiving
Silicon Labs USB to UART Bridge VCP Driver	ESP32 COM port detection
Final Working Configuration
Component / Parameter	Value
Microcontroller	ESP32
Board Selected	ESP32 Dev Module
Port Used	COM4
Baud Rate	9600
LED Pin	GPIO 23
Buzzer Pin	GPIO 22
Alert Condition	Motion + Face Detection
Telegram Cooldown	15 seconds
Remote Alert	Telegram Bot Notification
Final Pin Configuration
Component	ESP32 GPIO Pin
LED	GPIO 23
Buzzer	GPIO 22
GND	Common Ground
System Flow
Motion + Face Detected
      ↓
Python confirms intruder
      ↓
Python sends '1' to ESP32
      ↓
ESP32 turns ON LED and buzzer
      ↓
ESP32 sends Telegram alert
      ↓
Telegram cooldown prevents spam
      ↓
Safe condition detected
      ↓
Python sends '0' to ESP32
      ↓
ESP32 turns OFF LED and buzzer
Day 1 Summary – ESP32 Hardware Setup

Phase 2 Day 1 focused on preparing the ESP32 hardware foundation.

Completed work:

Installed ESP32 board support in Arduino IDE
Selected ESP32 Dev Module board
Fixed COM port issue by installing Silicon Labs USB to UART Bridge VCP driver
Verified successful code upload to ESP32
Tested external LED
Tested buzzer
Tested ESP32 Serial Monitor command mode
Challenge Faced

The ESP32 COM port was not visible initially.
The issue was solved by installing the Silicon Labs USB to UART Bridge VCP driver.

The LED was originally tested on GPIO 2, but it did not work on this ESP32 board. The LED pin was changed to GPIO 23, which worked successfully.

Day 2 Summary – ESP32 WiFi Foundation

Phase 2 Day 2 focused on testing ESP32 WiFi connectivity.

Completed work:

Connected ESP32 to WiFi using WiFi.h
Printed WiFi connection status in Serial Monitor
Displayed ESP32 local IP address
Used LED as WiFi connection indicator
Used buzzer as success/failure indicator
Tested WiFi failure case using wrong password
Output Behavior
Condition	LED Output	Buzzer Output
Connecting to WiFi	LED blinks	OFF
WiFi connected	LED stays ON	One beep
WiFi failed	LED stops	Three beeps
Day 3 Summary – Python AI + ESP32 Serial Integration

Phase 2 Day 3 focused on integrating the Python AI detection system with ESP32 using serial communication.

Completed work:

Installed and tested pyserial
Created a Python serial test file
Verified Python-to-ESP32 communication
Added send_to_esp32() function in Python
Triggered ESP32 alert only when motion and face were both detected
Completed the first AI-to-ESP32 hardware alert integration
Alert Logic
if recent_motion and len(faces) > 0:
    send_to_esp32(1)
else:
    send_to_esp32(0)

This ensures that the system does not trigger from motion alone or face detection alone.

Day 4 Summary – ESP32 Telegram Notification Test

Phase 2 Day 4 focused on preparing IoT notification using Telegram.

Completed work:

Created Telegram bot using BotFather
Generated Telegram bot token
Collected Telegram Chat ID using Telegram Bot API
Installed UniversalTelegramBot and ArduinoJson
Sent first Telegram test message from ESP32
Added LED and buzzer confirmation
Tested wrong WiFi password case
Tested wrong bot token case
Replaced private credentials with placeholders
Telegram Test Message
VisionGuard ESP32 Telegram test successful.

This confirmed that the ESP32 could connect to WiFi and send a Telegram message successfully.

Day 5 Summary – Full AI + ESP32 + Telegram Integration

Phase 2 Day 5 focused on full integration between Python AI detection, ESP32 hardware alerting, and Telegram IoT notification.

Completed work:

Modified ESP32 code to receive serial commands and send Telegram alerts
Updated Telegram alert message
Tested ESP32 using Arduino Serial Monitor
Connected Python AI detection code with ESP32 Telegram alert code
Completed full system test
Added 15-second Telegram cooldown
Protected private credentials before GitHub upload
Final Telegram Alert Message
🚨 VisionGuard Alert!

Intruder detected.
Detection: Motion + Face confirmed.
Alert Source: ESP32 IoT Module.
Status: LED and buzzer activated.
Cooldown Logic

A repeated Telegram alert issue was found during testing. When the same person moved again after detection, Telegram alerts were repeated too quickly.

To solve this, a 15-second cooldown was added on the ESP32 side.

unsigned long lastTelegramTime = 0;
unsigned long telegramCooldown = 15000; // 15 seconds
if (!alertSent && millis() - lastTelegramTime > telegramCooldown) {
  sendTelegramAlert();
  alertSent = true;
  lastTelegramTime = millis();
}

This prevents Telegram spam while still allowing new alerts after the cooldown period.

Day 6 Summary – Final Testing, Reliability, and Documentation

Phase 2 Day 6 focused on final testing, reliability improvements, code cleanup, and documentation.

Completed work:

Full system re-tested
15-second Telegram cooldown verified
Failure cases tested
ESP32 unplugged condition handled
Camera not detected condition handled
Camera blocked / too dark condition handled
Camera restored condition handled
Python and ESP32 code cleaned
Comments added throughout code
README updated
GitHub safety check completed
Reliability Improvements Added
Issue	Improvement
ESP32 unplugged while Python runs	Added try-except inside send_to_esp32()
Camera not detected	Added cap.isOpened() check
First frame capture failure	Added first-frame validation
Camera blocked / too dark	Added brightness-based blocked camera detection
Camera restored after blocking	Added recovery flag and motion baseline reset
Telegram repeated alerts	Added 15-second cooldown
GitHub credential risk	Replaced real values with placeholders
Camera Blocked Detection

When the camera is physically blocked, OpenCV may still receive frames. In that case, the motion score becomes 0 because the camera is receiving a dark/static frame.

To handle this, brightness-based camera blockage detection was added.

gray_check = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
average_brightness = cv2.mean(gray_check)[0]

camera_blocked = average_brightness < 10

If the camera is blocked or too dark:

A warning is displayed on the OpenCV window
ESP32 alert is forced OFF
The system does not crash
Detection continues safely after camera view is restored
Safety and Reliability Features
Motion + face condition reduces false alerts.
ESP32 serial communication uses safe error handling.
Python does not crash immediately if ESP32 is unavailable.
Camera open and first-frame validation are included.
Camera blocked / too dark condition is detected using brightness checking.
Camera restored condition resets motion baseline.
ESP32 alert is forced OFF during camera blockage or safe shutdown.
Telegram alert cooldown prevents repeated message spam.
Private credentials are replaced with placeholders before GitHub upload.
Security Note

This project uses WiFi credentials, Telegram Bot Token, and Telegram Chat ID for IoT notification testing.

For security reasons, real credentials are not uploaded to GitHub. Before running the code, replace the placeholder values with your own private credentials.

const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

#define BOT_TOKEN "YOUR_BOT_TOKEN"
#define CHAT_ID "YOUR_CHAT_ID"

Do not share or upload:

WiFi password
Telegram Bot Token
Telegram Chat ID
Screenshots showing private credentials
