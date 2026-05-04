# ============================================================
# 🛡️ AI Intruder Detection System
#    Motion Detection + Motion Area Visualization
#    Face Detection + Arduino Alert
# ============================================================
#
# This project combines Computer Vision with Arduino hardware control.
#
# The system continuously watches through the webcam and performs:
#
#   1. Motion Detection
#      - Compares the previous video frame with the current frame.
#      - Finds whether something has moved in front of the camera.
#
#   2. Motion Area Visualization
#      - Finds the largest moving area.
#      - Draws a blue rectangle around the moving region.
#      - This helps us visually confirm where motion occurred.
#
#   3. Face Detection
#      - Detects whether a human face is present.
#
#   4. Arduino Alert
#      - Sends '1' to Arduino when an intruder is detected.
#      - Sends '0' to Arduino when the system becomes safe.
#
# Intruder Alert Condition:
#
#   ALERT happens only when:
#
#       recent_motion == True
#       AND
#       number of detected faces > 0
#
# Why this combined condition is important:
#
#   - Face detection alone can trigger on a photo or screen.
#   - Motion detection alone can trigger on shadows or light changes.
#   - Motion + Face detection gives a smarter and more reliable alert.
#
# ============================================================


# ------------------------------------------------------------
# 📦 Import Required Libraries
# ------------------------------------------------------------

import os.path
# Used for checking whether a folder exists.
# In this project, it checks whether the "captures" folder exists.

import cv2
# OpenCV library.
# Used for:
#   - accessing webcam
#   - processing frames
#   - detecting motion
#   - detecting faces
#   - drawing rectangles and text
#   - displaying live video output

import winsound
# Used for beep sound on Windows.
# In this version, the beep is commented because Arduino buzzer is used.

import time
# Used for:
#   - cooldown timing
#   - motion memory timing
#   - Arduino startup delay

import serial
# Used for serial communication between Python and Arduino.
# Python sends commands through USB to control LED and buzzer.


# ------------------------------------------------------------
# 🔌 Connect Python Program to Arduino
# ------------------------------------------------------------
#
# serial.Serial("COM3", 9600) creates a serial connection.
#
# "COM3":
#   This is the Arduino port on your computer.
#   It may change depending on system.
#   Example: COM4, COM5, COM6, etc.
#
# 9600:
#   This is the baud rate.
#   The same baud rate must be written in Arduino code:
#
#       Serial.begin(9600);
#
# If the COM port or baud rate is wrong, Python will not be able
# to communicate with Arduino.

arduino = serial.Serial("COM3", 9600)

# When Python opens the serial connection, Arduino usually resets.
# This delay gives Arduino time to restart and become ready.
time.sleep(2)


# ------------------------------------------------------------
# 🔌 Function: Send Signal to Arduino
# ------------------------------------------------------------
#
# This function sends a command from Python to Arduino.
#
# signal = 1:
#   Send byte '1' to Arduino.
#   Arduino should turn ON LED and buzzer.
#
# signal = 0:
#   Send byte '0' to Arduino.
#   Arduino should turn OFF LED and buzzer.
#
# Important:
#   arduino.write() sends bytes, not normal strings.
#   That is why we write b'1' and b'0'.

def send_to_arduino(signal):
    if signal == 1:
        arduino.write(b'1')
        print("🔴 Arduino Alert ON")
        print("🔴 LED ON | 🔔 BUZZER ON")
    else:
        arduino.write(b'0')
        print("🟢 Arduino Alert OFF")
        print("🟢 SYSTEM OFF")


# ------------------------------------------------------------
# 📁 Create Folder for Captured Images
# ------------------------------------------------------------
#
# Whenever an intruder is detected, the system saves a frame.
# All images are stored in the "captures" folder.
#
# If the folder does not exist, this code creates it automatically.
# This prevents file-saving errors later.

if not os.path.exists("captures"):
    os.makedirs("captures")


# ------------------------------------------------------------
# 🔢 Initialize System Variables
# ------------------------------------------------------------

image_count = 0
# Used for giving unique names to saved intruder images.
#
# Example:
#   captures/intruder_0.jpg
#   captures/intruder_1.jpg
#   captures/intruder_2.jpg

last_capture_time = 0
# Stores the time when the previous intruder image was saved.

cooldown = 5
# Minimum time gap between saving two images.
#
# Why cooldown is needed:
#   Without cooldown, the system may save many images every second.
#   This would quickly fill storage and create unnecessary duplicate images.

system_active = False
# Tracks whether Arduino alert is currently ON or OFF.
#
# False:
#   Arduino LED/Buzzer is OFF.
#
# True:
#   Arduino LED/Buzzer is ON.
#
# Important:
#   This variable must remain outside the while loop.
#   If placed inside the loop, it would reset every frame,
#   causing repeated ON/OFF commands.

last_motion_time = 0
# Stores the last time when motion was detected.

motion_hold_time = 2
# Motion memory duration in seconds.
#
# Why motion memory is useful:
#   Motion detection can sometimes become False for a very short moment.
#   For example, if the person stops moving for a second.
#
# This variable keeps motion valid for 2 seconds after the last motion.
# It prevents the alert from flickering ON and OFF too quickly.


# ------------------------------------------------------------
# 🧠 STEP 1: Load Face Detection Model
# ------------------------------------------------------------
#
# Haar Cascade is a pre-trained face detection model provided by OpenCV.
#
# It detects face-like patterns such as:
#   - eyes
#   - nose bridge
#   - forehead area
#   - general face structure
#
# Important:
#   This is face detection, not face recognition.
#
# Face detection:
#   "There is a face."
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
# 0 means default camera.
# On most laptops, this opens the built-in webcam.
# If you use an external webcam, sometimes the value may be 1.

cap = cv2.VideoCapture(0)


# ------------------------------------------------------------
# 🖼️ Capture First Frame for Motion Detection
# ------------------------------------------------------------
#
# Motion detection needs two frames:
#   1. previous frame
#   2. current frame
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
#   - detects faces
#   - decides alert status
#   - controls Arduino
#   - displays output
#
# The loop stops when:
#   - webcam frame is not received
#   - user presses 'q'

while True:

    # Capture the current frame from webcam.
    ret, frame = cap.read()

    # ret is True when frame is captured successfully.
    # ret is False when camera fails or frame is unavailable.
    if not ret:
        break


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
    #   Color is not necessary for detecting motion.
    #   Grayscale makes the calculation faster and simpler.


    prev_gray = cv2.GaussianBlur(prev_gray, (9, 9), 0)
    curr_gray = cv2.GaussianBlur(curr_gray, (9, 9), 0)

    # Gaussian blur smooths the image.
    #
    # Why blur is important:
    #   A camera may produce small random noise.
    #   Lighting may slightly change.
    #   Without blur, these small changes can be mistaken as motion.
    #
    # Kernel size (9, 9):
    #   Controls how much smoothing is applied.


    diff = cv2.absdiff(prev_gray, curr_gray)

    # Calculates absolute difference between previous and current frame.
    #
    # Result:
    #   Bright pixels  → changed area
    #   Dark pixels    → unchanged area


    _, thresh = cv2.threshold(diff, 40, 255, cv2.THRESH_BINARY)

    # Threshold converts the difference image into black and white.
    #
    # If pixel difference is greater than 40:
    #   pixel becomes white.
    #
    # If pixel difference is 40 or less:
    #   pixel becomes black.
    #
    # White areas represent motion.


    thresh = cv2.dilate(thresh, None, iterations=2)

    # Dilation expands white motion areas.
    #
    # Why dilation is used:
    #   Motion areas may appear broken into small parts.
    #   Dilation joins nearby white pixels and makes the motion region clearer.


    # --------------------------------------------------------
    # 📦 Motion Area Detection using Contours
    # --------------------------------------------------------
    #
    # A contour is the boundary of a white region in the threshold image.
    #
    # Since white regions represent motion,
    # contours help us locate where motion happened.

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # cv2.RETR_EXTERNAL:
    #   Finds only outer contours.
    #   This avoids unnecessary nested contour detection.
    #
    # cv2.CHAIN_APPROX_SIMPLE:
    #   Compresses contour points to save memory.


    # --------------------------------------------------------
    # 🔵 Draw Only the Largest Motion Area
    # --------------------------------------------------------
    #
    # Many small contours may appear due to noise.
    # Instead of drawing boxes everywhere,
    # we only draw the largest moving area.
    #
    # This keeps the output clean and professional.

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)

        # Check whether largest contour is big enough.
        # This avoids drawing boxes for tiny noise.
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

            # Write "Motion" label above the motion box.
            cv2.putText(
                frame,
                "Motion",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2
            )


    motion_score = cv2.countNonZero(thresh)

    # Counts number of white pixels in threshold image.
    #
    # More white pixels:
    #   More movement.
    #
    # Fewer white pixels:
    #   Less movement.


    motion_detected = motion_score > 7000

    # If motion_score is greater than 7000,
    # the system treats it as real motion.
    #
    # Tuning advice:
    #
    #   If system detects motion too easily:
    #       increase 7000.
    #
    #   If system misses actual movement:
    #       decrease 7000.


    if motion_detected:
        last_motion_time = time.time()

    # Whenever real motion is detected,
    # update the last motion time.


    recent_motion = (time.time() - last_motion_time) < motion_hold_time

    # recent_motion remains True for 2 seconds after motion is detected.
    #
    # This means:
    #
    #   If motion happened recently:
    #       recent_motion = True
    #
    #   If no motion happened for more than motion_hold_time:
    #       recent_motion = False


    print("Motion Score:", motion_score)

    # Prints motion score in terminal.
    # This helps during testing and calibration.


    prev_frame = frame.copy()

    # Update previous frame for the next loop cycle.
    #
    # Current frame now becomes the old frame for the next comparison.


    # --------------------------------------------------------
    # 🔍 STEP 5: Face Detection
    # --------------------------------------------------------
    #
    # detectMultiScale scans the grayscale image and finds faces.
    #
    # It returns coordinates for each detected face:
    #
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
    #   Controls how much the image size is reduced while scanning.
    #   1.2 is a balanced value.
    #
    # minNeighbors:
    #   Controls detection strictness.
    #
    #   Higher value:
    #       fewer false detections, but may miss some faces.
    #
    #   Lower value:
    #       detects more faces, but may create false positives.
    #
    # minSize:
    #   Ignores faces smaller than 60x60 pixels.


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

    # Displays total number of detected faces.


    cv2.putText(
        frame,
        f"Motion: {recent_motion}",
        (10, 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    # Displays whether motion was detected recently.


    # --------------------------------------------------------
    # 🚦 STEP 6: Decide SAFE / ALERT Status
    # --------------------------------------------------------
    #
    # ALERT condition:
    #
    #   recent_motion is True
    #   AND
    #   at least one face is detected

    status = "ALERT" if (recent_motion and len(faces) > 0) else "SAFE"

    color = (0, 0, 255) if status == "ALERT" else (0, 255, 0)

    # BGR color format:
    #
    #   (0, 0, 255) = Red
    #   (0, 255, 0) = Green
    #
    # ALERT uses red.
    # SAFE uses green.


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
    # This section handles:
    #
    #   - Arduino alert ON/OFF
    #   - Intruder image saving
    #
    # State-based logic means:
    #
    #   The alert turns ON only once when intruder appears.
    #   It does not keep sending ON command again and again every frame.
    #
    # Why this matters:
    #
    #   A webcam loop runs many times per second.
    #   Without state handling, Arduino would receive repeated commands
    #   continuously and unnecessarily.

    current_time = time.time()

    if recent_motion and len(faces) > 0:

        # If intruder condition is true
        # and system is currently OFF,
        # turn Arduino alert ON.

        if not system_active:
            print("Intruder Detected!")

            send_to_arduino(1)
            # Sends byte '1' to Arduino.
            # Arduino should turn ON LED and buzzer.

            # winsound.Beep(1000, 500)
            # Optional laptop/PC beep.
            # Currently commented because Arduino buzzer is used.

            system_active = True
            # Remember that system alert is now ON.


        # Save image only if cooldown time has passed.
        if current_time - last_capture_time > cooldown:

            filename = f"captures/intruder_{image_count}.jpg"

            cv2.imwrite(filename, frame)
            # Saves the current frame as image.

            image_count += 1
            # Increases counter for the next image filename.

            last_capture_time = current_time
            # Updates the last saved image time.

    else:

        # If alert condition is false
        # and Arduino alert is currently ON,
        # turn Arduino alert OFF.

        if system_active:
            send_to_arduino(0)
            # Sends byte '0' to Arduino.
            # Arduino should turn OFF LED and buzzer.

            system_active = False
            # Remember that system alert is now OFF.


    # --------------------------------------------------------
    # 🟩 STEP 8: Draw Face Bounding Boxes
    # --------------------------------------------------------
    #
    # For each detected face, draw:
    #   - red "Intruder" label
    #   - green rectangle around face

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
    # Shows the processed frame with:
    #   - face count
    #   - SAFE/ALERT status
    #   - motion status
    #   - motion box
    #   - face box

    cv2.imshow("Face Detection", frame)


    # --------------------------------------------------------
    # ⌨️ Exit Condition
    # --------------------------------------------------------
    #
    # cv2.waitKey(1):
    #   waits 1 millisecond for keyboard input.
    #
    # ord('q'):
    #   ASCII value of q key.
    #
    # If user presses q:
    #   loop breaks and program exits safely.

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# ------------------------------------------------------------
# 🧹 STEP 10: Cleanup and Safe Shutdown
# ------------------------------------------------------------
#
# Cleanup is very important in hardware + camera projects.
# It ensures:
#   - webcam is released
#   - OpenCV windows are closed
#   - Arduino LED/Buzzer is turned OFF
#   - Serial connection is closed

cap.release()
# Releases the webcam so other apps can use it later.

cv2.destroyAllWindows()
# Closes all OpenCV display windows.

send_to_arduino(0)
# Safety OFF command.
# Even if alert was ON before exit, this turns Arduino output OFF.

arduino.close()
# Closes the serial connection with Arduino.