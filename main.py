import cv2

from config import (
    ANGLE_DEFINITIONS,
    CAMERA_INDEX,
    FRAME_HEIGHT,
    FRAME_WIDTH,
    WINDOW_NAME,
)
from exercises.biceps_curl import BicepsCurlExercise
from exercises.push_up import PushUpExercise
from exercises.squat import SquatExercise
from pose_detector import PoseDetector
from renderer import renderOverlay
from utils import safeAngle


def computeAngles(landmarks):
    angles = {}
    for label, (a, b, c) in ANGLE_DEFINITIONS.items():  #Go through each angle from config.py
        value = safeAngle(landmarks, a, b, c)  #Calculate ABC angles
        if value is not None:   #Only store the  angle if all points are not null
            angles[label] = value
    return angles


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
        "3": PushUpExercise(),  #Key 3 selects the push-up exercise
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

            angles = computeAngles(landmarks) #Calculates joint angles
            currentExercise.update(angles)    #Updates the currently selected exercise using calculated joint angles
            renderOverlay(frame, landmarks, angles, currentExercise) #Draws all text overlays on the frame

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
            if key == ord("3"): #Checks if 3 was pressed and stores push up as the selected and current exercise
                currentExerciseKey = "3"
                currentExercise = exercises[currentExerciseKey]
    finally: #Releases all resources
        detector.close()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
