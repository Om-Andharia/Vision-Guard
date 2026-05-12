# ============================================================
# 🔌 Python Manual Arduino Serial Control
# ============================================================
# This code allows the user to manually control Arduino
# using Python input from the keyboard.
#
# User enters:
#   1 → Turn Arduino alert ON
#   0 → Turn Arduino alert OFF
#   q → Quit program and turn Arduino OFF
#
# This is useful for testing whether Python can send commands
# to Arduino before connecting it with the full VisionGuard system.
# ============================================================


# ------------------------------------------------------------
# 📦 Import Required Libraries
# ------------------------------------------------------------
import serial
# pyserial library.
# Used to communicate with Arduino through USB Serial.

import time
# Used to add delay after opening Serial connection.


# ------------------------------------------------------------
# 🔌 Connect Python to Arduino
# ------------------------------------------------------------
# Change COM3 to your actual Arduino COM port.
#
# On Windows, Arduino may appear as:
#   COM3, COM4, COM5, etc.
#
# Baud rate 9600 must match Arduino code:
#   Serial.begin(9600);

arduino = serial.Serial('COM3', 9600)

# Arduino usually resets when Serial connection starts.
# This delay gives Arduino time to restart and become ready.
time.sleep(2)


# ------------------------------------------------------------
# 🔁 Start Manual Command Loop
# ------------------------------------------------------------
# This loop keeps asking the user for input until user enters q.
while True:

    command = input("Enter 1 for ON, 0 for OFF, q to quit: ")
    # Takes command from user through keyboard.


    # --------------------------------------------------------
    # ❌ Quit Command
    # --------------------------------------------------------
    if command == "q":

        arduino.write(b'0')
        # Before exiting, send OFF command to Arduino.
        # This ensures LED/buzzer do not remain ON.

        print("Exiting... Arduino OFF")
        break
        # Break stops the while loop.


    # --------------------------------------------------------
    # ✅ Valid ON/OFF Commands
    # --------------------------------------------------------
    if command in ["1", "0"]:

        arduino.write(command.encode())
        # command.encode() converts "1" or "0" string into bytes.
        #
        # Example:
        #   "1" becomes b'1'
        #   "0" becomes b'0'
        #
        # Serial communication sends bytes, so encoding is needed.

        print(f"Sent command: {command}")


    # --------------------------------------------------------
    # ⚠️ Invalid Input Handling
    # --------------------------------------------------------
    else:
        print("Invalid input. Use 1, 0, or q.")
        # Runs when user enters anything other than 1, 0, or q.


# ------------------------------------------------------------
# 🔒 Close Serial Connection
# ------------------------------------------------------------
arduino.close()
# Closes connection safely so Arduino port can be used again later.
