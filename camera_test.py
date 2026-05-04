# Import OpenCV library (cv2)
# This library helps us work with cameras, images, and videos
import cv2


# -------------------------------
# STEP 1: CONNECT TO THE WEBCAM
# -------------------------------

# Create a VideoCapture object to access the webcam
# 0 = default camera (usually your laptop webcam)
# If you have multiple cameras, try 1, 2, etc.
cap = cv2.VideoCapture(0)


# -------------------------------
# STEP 2: START CONTINUOUS VIDEO LOOP
# -------------------------------

# We use an infinite loop because video is just many images (frames) shown continuously
while True:

    # Read a frame from the camera
    # ret → Boolean (True if frame is captured successfully, False if error)
    # frame → The actual image captured from the webcam (like a snapshot)
    ret, frame = cap.read()

    # If frame is not received properly, exit the loop
    # This prevents crashes if camera stops working
    if not ret:
        break


    # -------------------------------
    # STEP 3: DISPLAY THE FRAME
    # -------------------------------

    # Show the captured frame in a window
    # "Camera Feed" is just the window title
    cv2.imshow("Camera Feed", frame)


    # -------------------------------
    # STEP 4: EXIT CONDITION
    # -------------------------------

    # waitKey(1):
    # - Waits for 1 millisecond for a key press
    # - Required for the window to refresh properly

    # ord('q'):
    # - Converts character 'q' into its ASCII value

    # & 0xFF:
    # - Ensures compatibility across different systems

    # If user presses 'q', exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# -------------------------------
# STEP 5: CLEANUP (VERY IMPORTANT)
# -------------------------------

# Release the camera (free the resource so other apps can use it)
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()