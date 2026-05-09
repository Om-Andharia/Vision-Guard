# ============================================================
# 🛡️ VisionGuard Phase 2
#    AI Intruder Detection System
#    Motion Detection + Motion Area Visualization
#    Face Detection + ESP32 Alert
# ============================================================
#
# This project combines:
#
#   1. Computer Vision using OpenCV
#      - Uses webcam feed.
#      - Detects motion.
#      - Detects human faces.
#
#   2. ESP32 Hardware Alert System
#      - Python sends signal to ESP32 through USB Serial.
#      - ESP32 can control LED and buzzer.
#
#   3. Smart Alert Logic
#      - Alert is triggered only when motion and face are both detected.
#
# Intruder Alert Condition:
#
#   ALERT happens only when:
#
#       recent_motion == True
#       AND
#       at least one face is detected
#
# Why this logic is powerful:
#
#   - Motion alone may be caused by light, shadow, fan, curtain, etc.
#   - Face alone may be detected from a photo or screen.
#   - Motion + Face gives a more reliable intruder condition.
#
# This code is part of the ESP32-based IoT upgrade of VisionGuard.
# ============================================================


# ------------------------------------------------------------
# 📦 Import Required Libraries
# ------------------------------------------------------------

import os.path
# Used to check whether folders exist.
# Here, it checks whether the "captures" folder exists.

import cv2
# OpenCV library.
# Used for:
#   - accessing webcam
#   - reading video frames
#   - converting images to grayscale
#   - detecting motion
#   - detecting faces
#   - drawing text and rectangles
#   - displaying live output window

import winsound
# Used for sound alerts on Windows.
# In this version, the beep is commented because ESP32 buzzer is used.

import time
# Used for:
#   - cooldown timing
#   - motion memory timing
#   - ESP32 startup delay

import serial
# Used for USB Serial communication.
# Python uses this to send commands to ESP32.


# ------------------------------------------------------------
# 🔌 ESP32 Serial Configuration
# ------------------------------------------------------------
#
# ESP32_PORT:
#   This is the COM port where ESP32 is connected.
#
#   Example:
#       COM3, COM4, COM5, etc.
#
#   In this project, ESP32 is connected on COM4.
#
# BAUD_RATE:
#   Speed of serial communication.
#
#   This must match the ESP32 Arduino code:
#
#       Serial.begin(9600);
#
# If Python uses 9600 but ESP32 uses another baud rate,
# communication will not work correctly.

ESP32_PORT = "COM4"
BAUD_RATE = 9600


# ------------------------------------------------------------
# 🔌 Connect Python Program to ESP32
# ------------------------------------------------------------
#
# We use try-except here because ESP32 may not always be connected.
#
# Without try-except:
#   If ESP32 is unplugged or COM port is wrong,
#   the program will crash immediately.
#
# With try-except:
#   The program continues running.
#   Camera and AI detection still work.
#   Only ESP32 alert is skipped.

try:
    esp32 = serial.Serial(ESP32_PORT, BAUD_RATE, timeout=1)

    # When serial connection starts, ESP32 may reset.
    # This delay gives ESP32 time to restart and become ready.
    time.sleep(2)

except Exception as e:
    esp32 = None

    # If connection fails, show the error clearly.
    print("ESP32 connection failed:", e)


# ------------------------------------------------------------
# 🔌 Function: Send Signal to ESP32
# ------------------------------------------------------------
#
# This function sends alert commands from Python to ESP32.
#
# signal = 1:
#   Python sends byte '1' to ESP32.
#   ESP32 should turn ON LED and buzzer.
#
# signal = 0:
#   Python sends byte '0' to ESP32.
#   ESP32 should turn OFF LED and buzzer.
#
# Important:
#   Serial communication sends bytes.
#   That is why we use b'1' and b'0'.

def send_to_esp32(signal):

    # First check whether ESP32 is connected.
    if esp32 is not None:

        if signal == 1:
            esp32.write(b'1')
            print("ESP32 Alert ON")

        else:
            esp32.write(b'0')
            print("ESP32 Alert OFF")

    else:
        # If ESP32 is not connected, do not crash the program.
        # Just print a message and skip hardware alert.
        print("ESP32 not connected. Alert skipped.")


# ------------------------------------------------------------
# 📁 Create Folder for Captured Images
# ------------------------------------------------------------
#
# Whenever an intruder is detected, the system saves a frame.
# These captured images are stored inside the "captures" folder.
#
# If the folder does not already exist, this code creates it.
# This prevents errors while saving images.

if not os.path.exists("captures"):
    os.makedirs("captures")


# ------------------------------------------------------------
# 🔢 Initialize System Variables
# ------------------------------------------------------------

image_count = 0
# Used for unique image filenames.
#
# Example:
#   captures/intruder_0.jpg
#   captures/intruder_1.jpg
#   captures/intruder_2.jpg

last_capture_time = 0
# Stores the timestamp of the last saved intruder image.

cooldown = 5
# Minimum time gap between two saved images.
#
# Why cooldown is needed:
#   Without cooldown, the system may save many images every second.
#   This creates duplicate images and wastes storage.

system_active = False
# Tracks whether ESP32 alert is currently ON or OFF.
#
# False:
#   ESP32 alert is OFF.
#
# True:
#   ESP32 alert is ON.
#
# Why this is important:
#   The webcam loop runs many times per second.
#   Without system_active, Python would send repeated ON commands
#   to ESP32 again and again.

last_motion_time = 0
# Stores the last time real motion was detected.

motion_hold_time = 2
# Motion memory duration in seconds.
#
# Example:
#   If motion is detected now,
#   recent_motion remains True for 2 seconds.
#
# Why this helps:
#   Sometimes motion briefly disappears for a moment.
#   This prevents alert flickering ON/OFF too quickly.


# ------------------------------------------------------------
# 🧠 STEP 1: Load Face Detection Model
# ------------------------------------------------------------
#
# Haar Cascade is a pre-trained OpenCV model for face detection.
#
# It detects face-like patterns such as:
#   - eyes
#   - nose bridge
#   - forehead area
#   - overall face structure
#
# Important:
#   This is face detection, not face recognition.
#
# Face detection:
#   "A face is present."
#
# Face recognition:
#   "This face belongs to a specific person."

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)


# ------------------------------------------------------------
# 📷 STEP 2: Start Webcam
# ------------------------------------------------------------
#
# 0 means default webcam.
# On most laptops, this opens the built-in camera.
# If an external webcam is used, the value may need to be changed to 1.

cap = cv2.VideoCapture(0)


# ------------------------------------------------------------
# 🖼️ Capture First Frame for Motion Detection
# ------------------------------------------------------------
#
# Motion detection compares:
#   previous frame
#   current frame
#
# Before the loop starts, we capture one frame and store it as prev_frame.
# This becomes the first reference frame.

ret, prev_frame = cap.read()


# ------------------------------------------------------------
# 🔄 STEP 3: Main Video Processing Loop
# ------------------------------------------------------------
#
# This loop continuously:
#   - captures webcam frames
#   - detects motion
#   - draws motion area
#   - detects faces
#   - decides SAFE or ALERT
#   - sends command to ESP32
#   - saves intruder images
#   - displays live output
#
# The loop ends when:
#   - camera fails
#   - user presses q

while True:

    # Capture current webcam frame.
    ret, frame = cap.read()

    # If camera frame is not received, stop safely.
    if not ret:
        print("Camera not detected. Please check webcam connection.")

        cap.release()
        cv2.destroyAllWindows()

        if esp32 is not None:
            esp32.close()

        exit()


    # --------------------------------------------------------
    # 🎨 STEP 4: Motion Detection using Frame Difference
    # --------------------------------------------------------
    #
    # Basic idea:
    #
    #   If previous frame and current frame are different,
    #   something has moved.
    #
    # We compare:
    #
    #   prev_frame  → old frame
    #   frame       → current frame

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert both frames to grayscale.
    #
    # Why grayscale?
    #   Motion detection does not need color information.
    #   Grayscale makes processing faster and simpler.


    prev_gray = cv2.GaussianBlur(prev_gray, (9, 9), 0)
    curr_gray = cv2.GaussianBlur(curr_gray, (9, 9), 0)

    # Gaussian blur smooths the image.
    #
    # Why blur is useful:
    #   Camera noise and small light changes can create false motion.
    #   Blur reduces those small unwanted changes.


    diff = cv2.absdiff(prev_gray, curr_gray)

    # absdiff calculates absolute difference between two frames.
    #
    # Bright pixels:
    #   changed areas
    #
    # Dark pixels:
    #   unchanged areas


    _, thresh = cv2.threshold(diff, 40, 255, cv2.THRESH_BINARY)

    # Threshold converts the difference image into black and white.
    #
    # If pixel difference > 40:
    #   pixel becomes white.
    #
    # If pixel difference <= 40:
    #   pixel becomes black.
    #
    # White regions represent movement.


    thresh = cv2.dilate(thresh, None, iterations=2)

    # Dilation expands white regions.
    #
    # Why dilation is needed:
    #   Motion regions may appear broken into small parts.
    #   Dilation joins nearby white pixels and makes motion areas clearer.


    # --------------------------------------------------------
    # 📦 Motion Area Detection using Contours
    # --------------------------------------------------------
    #
    # Contours are boundaries of white regions.
    #
    # Since white regions represent motion,
    # contours help us find where movement happened.

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # cv2.RETR_EXTERNAL:
    #   Detects only outer contours.
    #
    # cv2.CHAIN_APPROX_SIMPLE:
    #   Compresses contour points to save memory.


    # --------------------------------------------------------
    # 🔵 Draw Largest Motion Area
    # --------------------------------------------------------
    #
    # There may be many small motion regions due to noise.
    # To keep output clean, we draw only the largest motion area.

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)

        # Ignore very small moving regions.
        # This prevents tiny noise from getting motion boxes.
        if cv2.contourArea(largest_contour) > 3000:

            x, y, w, h = cv2.boundingRect(largest_contour)

            # Draw blue rectangle around largest motion area.
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2
            )

            # Add label above motion rectangle.
            cv2.putText(
                frame,
                "Motion",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2
            )


    # --------------------------------------------------------
    # 📊 Calculate Motion Score
    # --------------------------------------------------------

    motion_score = cv2.countNonZero(thresh)

    # countNonZero counts white pixels in threshold image.
    #
    # More white pixels:
    #   more motion
    #
    # Fewer white pixels:
    #   less motion


    motion_detected = motion_score > 7000

    # If motion_score is above 7000,
    # system treats it as significant motion.
    #
    # Tuning:
    #   Increase 7000 if false motion occurs.
    #   Decrease 7000 if real motion is missed.


    if motion_detected:
        last_motion_time = time.time()

    # Whenever motion is detected,
    # store current time.


    recent_motion = (time.time() - last_motion_time) < motion_hold_time

    # recent_motion keeps motion valid for a short time.
    #
    # Example:
    #   motion_hold_time = 2
    #
    # Motion detected 1 second ago:
    #   recent_motion = True
    #
    # Motion detected 3 seconds ago:
    #   recent_motion = False


    print("Motion Score:", motion_score)

    # Prints motion score in terminal.
    # Useful for testing and calibration.


    prev_frame = frame.copy()

    # Update previous frame.
    # Current frame becomes previous frame for next loop cycle.


    # --------------------------------------------------------
    # 🔍 STEP 5: Face Detection
    # --------------------------------------------------------
    #
    # detectMultiScale scans grayscale image and returns detected faces.
    #
    # Each detected face contains:
    #   x → left position
    #   y → top position
    #   w → width
    #   h → height

    faces = face_cascade.detectMultiScale(
        curr_gray,
        scaleFactor=1.2,
        minNeighbors=4,
        minSize=(60, 60)
    )

    # scaleFactor:
    #   Controls how much image size changes during scanning.
    #
    # minNeighbors:
    #   Controls detection strictness.
    #
    # Higher minNeighbors:
    #   fewer false detections, but may miss faces.
    #
    # Lower minNeighbors:
    #   detects more faces, but may create false positives.
    #
    # minSize:
    #   Ignores very small face-like regions.


    # --------------------------------------------------------
    # 📊 Display Face Count and Motion Status
    # --------------------------------------------------------

    cv2.putText(
        frame,
        f"Faces: {len(faces)}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    # Shows number of faces detected.


    cv2.putText(
        frame,
        f"Motion: {recent_motion}",
        (10, 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    # Shows whether recent motion is currently active.


    # --------------------------------------------------------
    # 🚦 STEP 6: Decide SAFE / ALERT Status
    # --------------------------------------------------------
    #
    # ALERT only when:
    #   recent motion is true
    #   AND
    #   at least one face is detected

    status = "ALERT" if (recent_motion and len(faces) > 0) else "SAFE"

    color = (0, 0, 255) if status == "ALERT" else (0, 255, 0)

    # OpenCV uses BGR color format:
    #   (0, 0, 255) = Red
    #   (0, 255, 0) = Green

    cv2.putText(
        frame,
        f"Status: {status}",
        (10, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2
    )


    # --------------------------------------------------------
    # 🚨 STEP 7: State-Based Intruder Handling
    # --------------------------------------------------------
    #
    # This controls:
    #   - ESP32 alert ON/OFF
    #   - image saving
    #
    # State-based logic means:
    #   ESP32 receives ON signal only once when intruder appears.
    #   ESP32 receives OFF signal only once when intruder disappears.
    #
    # This avoids sending repeated commands many times per second.

    current_time = time.time()

    if recent_motion and len(faces) > 0:

        # If intruder condition is true and system is currently OFF,
        # send ON command to ESP32.

        if not system_active:
            print("Intruder Detected!")

            send_to_esp32(1)
            # Sends byte '1' to ESP32.
            # ESP32 should turn ON LED and buzzer.

            # winsound.Beep(1000, 500)
            # Optional laptop beep.
            # Currently commented because ESP32 buzzer is used.

            system_active = True
            # Store that alert system is now ON.


        # Save image only after cooldown time has passed.
        if current_time - last_capture_time > cooldown:

            filename = f"captures/intruder_{image_count}.jpg"

            cv2.imwrite(filename, frame)
            # Saves current processed frame as image.

            image_count += 1
            # Prepares next unique image filename.

            last_capture_time = current_time
            # Updates last image capture time.

    else:

        # If intruder condition is false and system is currently ON,
        # turn ESP32 alert OFF.

        if system_active:
            send_to_esp32(0)
            # Sends byte '0' to ESP32.
            # ESP32 should turn OFF LED and buzzer.

            system_active = False
            # Store that alert system is now OFF.


    # --------------------------------------------------------
    # 🟩 STEP 8: Draw Face Bounding Boxes
    # --------------------------------------------------------
    #
    # For each detected face:
    #   - write "Intruder"
    #   - draw green box around face

    for (x, y, w, h) in faces:

        cv2.putText(
            frame,
            "Intruder",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )


    # --------------------------------------------------------
    # 🖥️ STEP 9: Display Final Output
    # --------------------------------------------------------
    #
    # The output window shows:
    #   - face count
    #   - SAFE / ALERT status
    #   - motion state
    #   - blue motion box
    #   - green face box

    cv2.imshow("Face Detection", frame)


    # --------------------------------------------------------
    # ⌨️ Exit Condition
    # --------------------------------------------------------
    #
    # cv2.waitKey(1) checks for keyboard input.
    #
    # If q is pressed:
    #   the program exits safely.

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# ------------------------------------------------------------
# 🧹 STEP 10: Cleanup and Safe Shutdown
# ------------------------------------------------------------
#
# This section runs when the main loop ends.
#
# Cleanup is important because:
#   - webcam should be released
#   - OpenCV windows should close properly
#   - ESP32 alert should be turned OFF
#   - serial connection should be closed safely

cap.release()
# Releases webcam access.

cv2.destroyAllWindows()
# Closes all OpenCV windows.

send_to_esp32(0)
# Sends safety OFF command to ESP32.
# This ensures LED and buzzer are OFF when program ends.

if esp32 is not None:
    esp32.close()
    # Closes ESP32 serial connection safely.