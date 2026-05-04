import serial
import time

# Change COM3 to your actual Arduino COM port
arduino = serial.Serial('COM3', 9600)
time.sleep(2)

while True:
    command = input("Enter 1 for ON, 0 for OFF, q to quit: ")

    if command == "q":
        arduino.write(b'0')
        print("Exiting... Arduino OFF")
        break

    if command in ["1", "0"]:
        arduino.write(command.encode())
        print(f"Sent command: {command}")
    else:
        print("Invalid input. Use 1, 0, or q.")

arduino.close()