import serial
import time

ESP32_PORT = "COM4"
BAUD_RATE = 9600


try:
    esp32 = serial.Serial(ESP32_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)

    print("ESP32 connected successfully.")

    print("Turning alert ON...")
    esp32.write(b'1')
    time.sleep(2)

    print("Turning alert OFF...")
    esp32.write(b'0')
    time.sleep(1)

    esp32.close()
    print("Test completed.")

except Exception as e:
    print("ESP32 serial test failed:", e)

