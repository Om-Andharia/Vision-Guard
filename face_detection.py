# ============================================================
# 🛡️ VisionGuard Phase 2
#    AI Intruder Detection System
#    Motion Detection + Face Detection + ESP32 Alert
# ============================================================
#
# This project uses a laptop webcam and Python OpenCV to detect
# possible intruders.
#
# The system checks two things:
#
#   1. Motion
#      - Is something moving in front of the camera?
#
#   2. Face
#      - Is a human face visible?
#
# The system sends an alert to ESP32 only when BOTH conditions are true:
#
#       Motion detected + Face detected = Intruder Alert
#
# ESP32 then controls external hardware such as:
#   - LED
#   - Buzzer
#
# This code also includes safety handling for:
#   - ESP32 not connected
#   - ESP32 disconnected during runtime
#   - Camera not detected
#   - Camera blocked or too dark
#
# ============================================================


# ------------------------------------------------------------
# 📦 Import Required Libraries
# ------------------------------------------------------------

import os.path
# Used for checking whether a folder exists.
# Example:
#   We check if the "captures" folder exists before saving images.

import cv2
# OpenCV library.
# Used for:
#   - opening webcam
#   - reading video frames
#   - image processing
#   - motion detection
#   - face detection
#   - drawing text and rectangles on screen

# import winsound
# winsound is used for playing beep sounds on Windows.
# It is commented because this version uses ESP32 buzzer instead.

import time
# Used for:
#   - delay after connecting ESP32
#   - cooldown timing
#   - motion memory timing

import serial
# Used for USB serial communication between Python and ESP32.
# Python sends '1' or '0' to ESP32 through this library.


# ------------------------------------------------------------
# 🔌 ESP32 Serial Configuration
# ------------------------------------------------------------

ESP32_PORT = "COM4"
# This is the COM port where ESP32 is connected.
#
# On Windows, ESP32 usually appears as:
#   COM3, COM4, COM5, etc.
#
# If your ESP32 is connected to another port,
# change this value.

BAUD_RATE = 9600
# Baud rate means communication speed.
#
# This value must match the ESP32 code:
#
#   Serial.begin(9600);
#
# If Python and ESP32 use different baud rates,
# communication will not work properly.


# ------------------------------------------------------------
# 🔌 Connect Python Program to ESP32
# ------------------------------------------------------------
#
# We use try-except because ESP32 may not always be connected.
#
# Without try-except:
#   If ESP32 is unplugged, Python will crash.
#
# With try-except:
#   Python continues running.
#   Camera detection still works.
#   Only hardware alert is skipped.

try:
    esp32 = serial.Serial(ESP32_PORT, BAUD_RATE, timeout=1)

    # ESP32 may restart when serial connection opens.
    # So we wait 2 seconds to let ESP32 become ready.
    time.sleep(2)

    print("ESP32 connected successfully.")

except Exception as e:
    esp32 = None

    # If ESP32 connection fails, show the reason clearly.
    print("ESP32 connection failed:", e)


# ------------------------------------------------------------
# 🔌 Function: Send Signal to ESP32
# ------------------------------------------------------------
#
# This function sends alert commands to ESP32.
#
# signal = 1:
#   Send ON command to ESP32.
#   ESP32 should turn ON LED and buzzer.
#
# signal = 0:
#   Send OFF command to ESP32.
#   ESP32 should turn OFF LED and buzzer.
#
# Why b'1' and b'0'?
#   Serial communication sends bytes.
#   So we send byte values, not normal strings.

def send_to_esp32(signal):
    global esp32

    # First check whether ESP32 is connected.
    if esp32 is not None:

        try:
            if signal == 1:
                esp32.write(b'1')
                print("ESP32 Alert ON")

            else:
                esp32.write(b'0')
                print("ESP32 Alert OFF")

        except Exception as e:
            # This block runs if ESP32 disconnects while the program is running.
            print("ESP32 disconnected or write failed:", e)

            # Mark ESP32 as unavailable so future alerts are skipped safely.
            esp32 = None

    else:
        # If ESP32 is not connected, do not crash.
        # Only print message and continue AI detection.
        print("ESP32 not connected. Alert skipped.")


# ------------------------------------------------------------
# 📁 Create Folder for Captured Images
# ------------------------------------------------------------
#
# Intruder images will be saved inside the "captures" folder.
#
# If the folder does not exist, create it automatically.

if not os.path.exists("captures"):
    os.makedirs("captures")


# ------------------------------------------------------------
# 🔢 Initialize Important Variables
# ------------------------------------------------------------

image_count = 0
# Used to create unique image names.
#
# Example:
#   captures/intruder_0.jpg
#   captures/intruder_1.jpg
#   captures/intruder_2.jpg

last_capture_time = 0
# Stores the time when the last intruder image was saved.

cooldown = 5
# Minimum time gap between saving two images.
#
# Why cooldown is needed:
#   Without cooldown, the system may save many images every second.
#   That would waste storage and create duplicate images.

system_active = False
# Tracks whether ESP32 alert is currently ON or OFF.
#
# False:
#   Alert is OFF.
#
# True:
#   Alert is ON.
#
# Why this is important:
#   The webcam loop runs many times per second.
#   Without this variable, Python would repeatedly send ON commands
#   to ESP32 again and again.

last_motion_time = 0
# Stores the most recent time when motion was detected.

motion_hold_time = 2
# Keeps motion active for 2 seconds after detection.
#
# Why this helps:
#   Motion detection can flicker.
#   A person may stop moving for a moment.
#   This prevents alert from turning ON/OFF too quickly.

was_camera_blocked = False
# Stores whether the camera was previously blocked or too dark.
#
# This is useful because when the camera becomes visible again,
# we reset the motion baseline to avoid false motion alerts.


# ------------------------------------------------------------
# 🧠 STEP 1: Load Face Detection Model
# ------------------------------------------------------------
#
# Haar Cascade is a pre-trained OpenCV model.
# It detects human faces in an image.
#
# Important:
#   This is face detection, not face recognition.
#
# Face detection means:
#   "A face is present."
#
# Face recognition means:
#   "This face belongs to Omi or another known person."

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)


# ------------------------------------------------------------
# 📷 STEP 2: Start Webcam
# ------------------------------------------------------------
#
# cv2.VideoCapture(0) opens the default webcam.
#
# 0 usually means:
#   laptop built-in camera
#
# If using external camera, sometimes you may need:
#   cv2.VideoCapture(1)

cap = cv2.VideoCapture(0)


# ------------------------------------------------------------
# ✅ Check Whether Camera Opened Successfully
# ------------------------------------------------------------
#
# cap.isOpened() checks if OpenCV successfully opened the camera.
#
# If camera is not available:
#   - show clear message
#   - turn ESP32 alert OFF
#   - close ESP32 safely
#   - exit program

if not cap.isOpened():
    print("Camera not detected or cannot be opened.")
    print("Please check camera permission, webcam connection, or camera index.")

    send_to_esp32(0)

    if esp32 is not None:
        try:
            esp32.close()
        except Exception as e:
            print("ESP32 close failed:", e)

    exit()


# ------------------------------------------------------------
# 🖼️ Capture First Frame for Motion Detection
# ------------------------------------------------------------
#
# Motion detection needs two frames:
#
#   1. Previous frame
#   2. Current frame
#
# Before starting the loop, we capture the first frame.
# This becomes the first previous frame.

ret, prev_frame = cap.read()


# ------------------------------------------------------------
# ✅ Check Whether First Frame Was Captured
# ------------------------------------------------------------
#
# Sometimes camera opens, but frame is not received.
# This can happen if:
#   - camera is blocked
#   - camera is disabled
#   - camera is being used by another app
#   - permission issue exists

if not ret or prev_frame is None:
    print("Camera opened, but first frame could not be captured.")
    print("Please check if the camera is blocked, used by another app, or disabled.")

    cap.release()
    cv2.destroyAllWindows()

    send_to_esp32(0)

    if esp32 is not None:
        try:
            esp32.close()
        except Exception as e:
            print("ESP32 close failed:", e)

    exit()


# ------------------------------------------------------------
# 🔄 STEP 3: Main Video Processing Loop
# ------------------------------------------------------------
#
# This loop continuously:
#   - captures webcam frames
#   - checks if camera is blocked
#   - detects motion
#   - detects face
#   - decides SAFE or ALERT
#   - sends command to ESP32
#   - saves intruder image
#   - displays output window
#
# The loop ends when:
#   - camera fails
#   - user presses q

while True:

    # Capture current webcam frame.
    ret, frame = cap.read()

    # If frame is not received, stop safely.
    if not ret or frame is None:
        print("Camera frame not received. Please check webcam connection.")

        cap.release()
        cv2.destroyAllWindows()

        send_to_esp32(0)

        if esp32 is not None:
            try:
                esp32.close()
            except Exception as e:
                print("ESP32 close failed:", e)

        exit()


    # --------------------------------------------------------
    # 🚫 Camera Blocked / Too Dark Detection
    # --------------------------------------------------------
    #
    # Important point:
    #   Even if the camera is blocked, OpenCV may still receive frames.
    #
    # Example:
    #   If you cover the webcam with your hand or tape,
    #   OpenCV still gets a black/dark image.
    #
    # So ret may still be True.
    # That is why we check brightness separately.

    gray_check = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert frame to grayscale because brightness is easier to measure
    # in a single-channel gray image.

    average_brightness = cv2.mean(gray_check)[0]

    # cv2.mean(gray_check)[0] gives average brightness.
    #
    # Very low brightness means:
    #   camera may be blocked
    #   or room may be too dark.

    camera_blocked = average_brightness < 10

    # If average brightness is below 10,
    # treat it as camera blocked or too dark.
    #
    # You can tune this value:
    #   Increase it if camera block is not detected.
    #   Decrease it if dark room is wrongly treated as blocked.


    if camera_blocked:
        print("Camera may be blocked or too dark.")

        was_camera_blocked = True

        # If alert was ON, turn it OFF immediately.
        if system_active:
            send_to_esp32(0)
            system_active = False

        # Display warning directly on camera output window.
        cv2.putText(
            frame,
            "CAMERA BLOCKED / TOO DARK",
            (10, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

        cv2.imshow("Face Detection", frame)

        # Update previous frame so the blocked frame does not create
        # strange motion behavior later.
        prev_frame = frame.copy()

        # Allow user to exit even while camera is blocked.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Skip the rest of the loop.
        # No motion detection, no face detection, no alert.
        continue


    # --------------------------------------------------------
    # ✅ Camera Restored Handling
    # --------------------------------------------------------
    #
    # If camera was blocked earlier and is now visible again,
    # we reset the motion baseline.
    #
    # Why?
    #   The first visible frame after blockage may look very different
    #   from the blocked frame.
    #   Without reset, it may create a false motion alert.

    if was_camera_blocked:
        print("Camera view restored. Resetting motion baseline.")

        was_camera_blocked = False
        prev_frame = frame.copy()

        cv2.putText(
            frame,
            "CAMERA RESTORED",
            (10, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.imshow("Face Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Skip this one frame after restore.
        # Next frame will use a clean baseline.
        continue


    # --------------------------------------------------------
    # 🎨 STEP 4: Motion Detection using Frame Difference
    # --------------------------------------------------------
    #
    # Motion detection idea:
    #
    #   If previous frame and current frame are different,
    #   something has moved.
    #
    # We compare:
    #   prev_frame  → old frame
    #   frame       → current frame

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert both frames to grayscale.
    #
    # Why grayscale?
    #   Motion detection does not need color.
    #   Grayscale is faster and simpler.


    prev_gray = cv2.GaussianBlur(prev_gray, (9, 9), 0)
    curr_gray = cv2.GaussianBlur(curr_gray, (9, 9), 0)

    # Gaussian blur smooths the image.
    #
    # Why blur is useful:
    #   It reduces camera noise and small light changes.
    #   This helps avoid false motion detection.


    diff = cv2.absdiff(prev_gray, curr_gray)

    # Calculates difference between old and current frame.
    #
    # Bright areas:
    #   changed pixels
    #
    # Dark areas:
    #   unchanged pixels


    _, thresh = cv2.threshold(diff, 40, 255, cv2.THRESH_BINARY)

    # Threshold converts the difference image into black and white.
    #
    # If difference > 40:
    #   pixel becomes white.
    #
    # If difference <= 40:
    #   pixel becomes black.
    #
    # White pixels represent motion.


    thresh = cv2.dilate(thresh, None, iterations=2)

    # Dilation expands white regions.
    #
    # Why?
    #   Motion regions may appear broken into small parts.
    #   Dilation joins them and makes motion area clearer.


    # --------------------------------------------------------
    # 📦 Motion Area Detection using Contours
    # --------------------------------------------------------
    #
    # Contours are outlines/boundaries of white regions.
    #
    # Since white regions represent motion,
    # contours help us locate the moving area.

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )


    # --------------------------------------------------------
    # 🔵 Draw Largest Motion Area
    # --------------------------------------------------------
    #
    # Instead of drawing many small boxes,
    # we draw only the largest motion area.
    #
    # This makes the output clean and easy to understand.

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)

        if cv2.contourArea(largest_contour) > 3000:
            # Ignore tiny movement/noise below 3000 area.

            x, y, w, h = cv2.boundingRect(largest_contour)

            # Draw blue rectangle around motion area.
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2
            )

            # Add "Motion" label.
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
    # More white pixels = more motion.
    # Fewer white pixels = less motion.

    motion_detected = motion_score > 7000

    # If motion score is greater than 7000,
    # treat it as significant motion.
    #
    # Tuning:
    #   Increase 7000 if false alerts happen.
    #   Decrease 7000 if real movement is missed.


    if motion_detected:
        last_motion_time = time.time()

    # Store the time when motion was detected.


    recent_motion = (time.time() - last_motion_time) < motion_hold_time

    # Motion memory:
    #   Keeps motion active for 2 seconds after detection.
    #
    # This prevents flickering when motion briefly drops.

    print("Motion Score:", motion_score)

    # Shows motion score in terminal for testing.

    prev_frame = frame.copy()

    # Update previous frame for next loop.
    # Current frame becomes previous frame in the next cycle.


    # --------------------------------------------------------
    # 🔍 STEP 5: Face Detection
    # --------------------------------------------------------
    #
    # Face detection is done after motion processing.
    #
    # detectMultiScale returns face boxes:
    #   x = left position
    #   y = top position
    #   w = width
    #   h = height

    faces = face_cascade.detectMultiScale(
        curr_gray,
        scaleFactor=1.2,
        minNeighbors=4,
        minSize=(60, 60)
    )

    # scaleFactor:
    #   Controls how the image is resized during face scanning.
    #
    # minNeighbors:
    #   Controls strictness of detection.
    #
    # minSize:
    #   Ignores very small face-like objects.


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

    cv2.putText(
        frame,
        f"Motion: {recent_motion}",
        (10, 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )


    # --------------------------------------------------------
    # 🚦 STEP 6: Decide SAFE / ALERT Status
    # --------------------------------------------------------

    status = "ALERT" if (recent_motion and len(faces) > 0) else "SAFE"

    # ALERT only when:
    #   recent motion is True
    #   and at least one face is detected.

    color = (0, 0, 255) if status == "ALERT" else (0, 255, 0)

    # OpenCV uses BGR format:
    #   Red   = (0, 0, 255)
    #   Green = (0, 255, 0)

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
    # This part controls:
    #   - ESP32 alert ON/OFF
    #   - image saving
    #
    # State-based logic means:
    #   Send ON signal only once when intruder appears.
    #   Send OFF signal only once when intruder disappears.

    current_time = time.time()

    if recent_motion and len(faces) > 0:

        if not system_active:
            print("Intruder Detected!")

            send_to_esp32(1)
            # Sends ON command to ESP32.

            # winsound.Beep(1000, 500)
            # Optional laptop beep if needed.

            system_active = True

        # Save image only after cooldown.
        if current_time - last_capture_time > cooldown:
            filename = f"captures/intruder_{image_count}.jpg"

            cv2.imwrite(filename, frame)

            image_count += 1
            last_capture_time = current_time

    else:

        if system_active:
            send_to_esp32(0)
            # Sends OFF command to ESP32.

            system_active = False


    # --------------------------------------------------------
    # 🟩 STEP 8: Draw Face Bounding Boxes
    # --------------------------------------------------------

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

    cv2.imshow("Face Detection", frame)


    # --------------------------------------------------------
    # ⌨️ Exit Condition
    # --------------------------------------------------------
    #
    # Press q to quit.

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# ------------------------------------------------------------
# 🧹 STEP 10: Cleanup and Safe Shutdown
# ------------------------------------------------------------
#
# This runs when program ends.
#
# It safely:
#   - releases webcam
#   - closes display windows
#   - turns ESP32 alert OFF
#   - closes ESP32 serial connection

cap.release()
cv2.destroyAllWindows()

send_to_esp32(0)

if esp32 is not None:
    try:
        esp32.close()
    except Exception as e:
        print("ESP32 close failed:", e)
