# ============================================================
# 🔌 Python to ESP32 Serial Communication Test
# ============================================================
# This code checks whether Python can communicate with ESP32
# through USB Serial.
#
# Python sends:
#   b'1' → ESP32 turns LED and buzzer ON
#   b'0' → ESP32 turns LED and buzzer OFF
#
# Purpose:
#   ✔ Check ESP32 COM port
#   ✔ Check baud rate
#   ✔ Check Python-to-ESP32 serial communication
#   ✔ Test LED and buzzer control from Python
# ============================================================


# ------------------------------------------------------------
# 📦 Import Required Libraries
# ------------------------------------------------------------
import serial
# pyserial library.
# Used to send data from Python to ESP32 through USB.

import time
# Used to add small delays between commands.


# ------------------------------------------------------------
# 🔌 ESP32 Serial Configuration
# ------------------------------------------------------------
ESP32_PORT = "COM4"
# This is the port where ESP32 is connected.
#
# On Windows, ESP32 may appear as:
#   COM3, COM4, COM5, etc.
#
# If this code does not work, check the correct COM port
# from Arduino IDE or Device Manager.

BAUD_RATE = 9600
# Baud rate is the communication speed.
#
# This must match ESP32 code:
#   Serial.begin(9600);
#
# If Python uses 9600 and ESP32 uses 115200,
# communication may fail or behave incorrectly.


# ------------------------------------------------------------
# 🧪 Try Connecting to ESP32
# ------------------------------------------------------------
# try-except is used so the program does not crash badly
# if ESP32 is unplugged or COM port is wrong.

try:
    esp32 = serial.Serial(ESP32_PORT, BAUD_RATE, timeout=1)
    # Open serial connection with ESP32.

    time.sleep(2)
    # ESP32 usually resets when serial connection opens.
    # This delay gives ESP32 time to restart and become ready.

    print("ESP32 connected successfully.")


    # --------------------------------------------------------
    # 🚨 Send Alert ON Command
    # --------------------------------------------------------
    print("Turning alert ON...")

    esp32.write(b'1')
    # Send byte '1' to ESP32.
    # ESP32 should turn LED and buzzer ON.

    time.sleep(2)
    # Keep alert ON for 2 seconds.


    # --------------------------------------------------------
    # ✅ Send Alert OFF Command
    # --------------------------------------------------------
    print("Turning alert OFF...")

    esp32.write(b'0')
    # Send byte '0' to ESP32.
    # ESP32 should turn LED and buzzer OFF.

    time.sleep(1)
    # Small delay before closing connection.


    # --------------------------------------------------------
    # 🔒 Close Serial Connection
    # --------------------------------------------------------
    esp32.close()
    # Close connection so other programs can use ESP32 later.

    print("Test completed.")


# ------------------------------------------------------------
# ❌ Error Handling
# ------------------------------------------------------------
except Exception as e:
    print("ESP32 serial test failed:", e)
    # Shows the exact error if connection fails.
    #
    # Common causes:
    #   - Wrong COM port
    #   - ESP32 unplugged
    #   - Arduino Serial Monitor already using the port
    #   - Required USB driver not installed
