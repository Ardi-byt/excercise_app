import cv2

from config import (
    ANGLE_DEFINITIONS,
    CAMERA_INDEX,
    FRAME_HEIGHT,
    FRAME_WIDTH,
    WINDOW_NAME,
)
from exercises.biceps_curl import BicepsCurlExercise
from exercises.squat import SquatExercise
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

def main() -> None:
    #Opens the camera based on the camera_index and sets the width and height of the capture
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not cap.isOpened():
        raise RuntimeError("Could not access webcam. Check permissions or CAMERA_INDEX.")

    detector = PoseDetector() #Creates a MediaPipe object
    exercises = {
        "1": SquatExercise(),   #Squat exercise is set as default and can also be chosen by pressing 1
        "2": BicepsCurlExercise(),  #Key 2 selects the biceps curl exercise
    }
    currentExerciseKey = "1"
    currentExercise = exercises[currentExerciseKey] #Stores the current selected exercise

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
            cv2.putText(frame, "1 Squat | 2 Biceps Curl", (20, 245), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2) #Shows the available exercises

            angles = computeAngles(landmarks) #Calculates joint angles
            currentExercise.update(angles)    #Updates the currently selected exercise using calculated joint angles
            drawAngles(frame, angles) #Draws the angles panel on top right
            cv2.putText(frame, f"Exercise: {currentExercise.name}", (20, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
            cv2.putText(frame, f"Reps: {currentExercise.count}", (20, 165), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
            cv2.putText(frame, f"Stage: {currentExercise.stage}", (20, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            cv2.putText(frame, f"Feedback: {currentExercise.feedback}", (20, 285), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)

            cv2.imshow(WINDOW_NAME, frame) #

            #Reads the current pressed keyboard key
            key = cv2.waitKey(1) & 0xFF 
            if key == ord("q"): #Checks if q was pressed and stops the program
                break
            if key == ord("1"): #Checks if 1 was pressed and stores squat as the selected and current exercise
                currentExerciseKey = "1"
                currentExercise = exercises[currentExerciseKey]
            if key == ord("2"): #Checks if 2 was pressed and stores biceps curl as the selected and current exercise
                currentExerciseKey = "2"
                currentExercise = exercises[currentExerciseKey]
    finally: #Releases all resources
        detector.close()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
