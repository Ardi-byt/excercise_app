import cv2

from config import (
    ANGLE_DEFINITIONS,
    CAMERA_INDEX,
    FRAME_HEIGHT,
    FRAME_WIDTH,
    SQUAT_DOWN_ANGLE,
    SQUAT_UP_ANGLE,
    WINDOW_NAME,
)
from pose_detector import PoseDetector
from utils import safeAngle


def computeAngles(landmarks):
    angles = {}
    for label, (a, b, c) in ANGLE_DEFINITIONS.items():  #Go through each angle from config.py
        value = safeAngle(landmarks, a, b, c)  #Calculate ABC angles
        if value is not None:   #Only store the  angle if all points are not null
            angles[label] = value
    return angles


def drawAngles(frame, angles):
    #Places the panel top right
    panel_x = frame.shape[1] - 360 
    panel_y = 10
    panel_w = 350
    panel_h = 28 + (len(ANGLE_DEFINITIONS) * 24)    #Height based on number of rows

    cv2.rectangle(frame, (panel_x, panel_y), (panel_x + panel_w, panel_y + panel_h), (20, 20, 20), -1)  #Draws the background of the panel
    cv2.putText(frame, "Joint Angles", (panel_x + 10, panel_y + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)    #Draws the title

    y = panel_y + 46
    for label in ANGLE_DEFINITIONS: #Draw every angle
        #If the angle is successfully calculated formats the angle with one decimal
        if label in angles:
            text = f"{label}: {angles[label]:.1f}"
        #If the angle is missing shows that its not available
        else:
            text = f"{label}: N/A"
        cv2.putText(frame, text, (panel_x + 10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 255, 200), 1)
        y += 24

#Updates the squat count and the current stage of the squat
def updateSquatCounter(angles, squatCount, squatStage):
    leftKnee = angles.get("Left Knee") #Gets left knee angle
    rightKnee = angles.get("Right Knee") #Gets right knee angle
    #keeps only the angles that are available
    validKnees = [angle for angle in (leftKnee, rightKnee) if angle is not None]
    if not validKnees: #Checks if neither knees are available
        return squatCount, squatStage   #Returns current count and stage

    kneeAngle = sum(validKnees) / len(validKnees)   #Calculates the average knee angle from the available knees

    if kneeAngle < SQUAT_DOWN_ANGLE:    #Check if user reached the bottom squat position > 90 degrees
        squatStage = "down" 
    elif kneeAngle > SQUAT_UP_ANGLE and squatStage == "down":   #Checks if user returned up after being down
        squatCount += 1     #Adds 1 rep
        squatStage = "up"   #Changes the stage of the squat

    return squatCount, squatStage   #Returns updated count and stage


def main() -> None:
    #Opens the camera based on the camera_index and sets the width and height of the capture
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not cap.isOpened():
        raise RuntimeError("Could not access webcam. Check permissions or CAMERA_INDEX.")

    detector = PoseDetector() #Creates a MediaPipe object
    squatCount = 0  #Stores how many squats were counted
    squatStage = "up"   #Stores the current squat stage starts with "up"

    try:
        while True: #Runs a camera loop infinitely
            success, frame = cap.read() #Reads one frame and checks if it fails
            if not success:
                continue

            results = detector.detectPose(frame)    #Runs the pose detection on that frame
            landmarks = detector.getLandmarks(results)  #Converts the landmarks into a list
            frame = detector.drawLandmarks(frame, results)  #Draws the landmarks and connections

            frame = cv2.flip(frame, 1)  #Flips the frame

            status_text = "Person detected" if landmarks else "No person detected" #Chooses status text
            cv2.putText(frame, status_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)    #Draws the status text on the screen
            cv2.putText(frame, "Press q to quit", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2) #Quit instructions

            angles = computeAngles(landmarks) #Calculates joint angles
            squatCount, squatStage = updateSquatCounter(angles, squatCount, squatStage) #Updates squat count based on knee angles
            drawAngles(frame, angles) #Draws the angles panel on top right
            cv2.putText(frame, f"Squats: {squatCount}", (20, 125), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
            cv2.putText(frame, f"Stage: {squatStage}", (20, 165), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            cv2.imshow(WINDOW_NAME, frame) #

            #Checks if user pressed q and stops the program
            if (cv2.waitKey(1) & 0xFF) == ord("q"):
                break
    finally: #Releases all resources
        detector.close()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
