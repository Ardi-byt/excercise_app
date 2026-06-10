import cv2
import mediapipe as mp

from config import (
    POSE_MIN_DETECTION_CONFIDENCE,
    POSE_MIN_TRACKING_CONFIDENCE,
    POSE_MODEL_COMPLEXITY,
    POSE_SMOOTH_LANDMARKS,
)


class PoseDetector:

    def __init__(self):
        self._mp_pose = mp.solutions.pose
        self._mp_drawing = mp.solutions.drawing_utils
        self._mp_drawing_styles = mp.solutions.drawing_styles

        #Creates a MediaPipe pose detector and uses everything needed from config.py
        self._pose = self._mp_pose.Pose(
            static_image_mode=False,
            model_complexity=POSE_MODEL_COMPLEXITY,
            smooth_landmarks=POSE_SMOOTH_LANDMARKS,
            min_detection_confidence=POSE_MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=POSE_MIN_TRACKING_CONFIDENCE,
        )

    def detectPose(self, frame): #Runs pose detection on one frame
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Converts from OpenCV BGR to RGB for MediaPipe
        rgb.flags.writeable = False #Marks image as not writable
        results = self._pose.process(rgb) #Runs MP pose model on the RGB frame
        rgb.flags.writeable = True #Marks the image as writable after processing
        return results #Returns the detection results

    @staticmethod
    def getLandmarks(results): #Converts the landmarks into a python list
        if not results or not results.pose_landmarks: #Checks if no pose was detected and returns None
            return None

        landmarks = [] #Crate a list for the converted landmarks
        for lm in results.pose_landmarks.landmark: #Loops through every landmark
            landmarks.append( #Adds the converted landmark to the list the x,y,z and visibility
                {
                    "x": float(lm.x),
                    "y": float(lm.y),
                    "z": float(lm.z),
                    "visibility": float(lm.visibility),
                }
            )
        return landmarks

    def drawLandmarks(self, frame, results):
        if not results or not results.pose_landmarks: #Checks if no landmark exists and returns the original frame
            return frame

        self._mp_drawing.draw_landmarks( #Use MP drawing helper
            frame,
            results.pose_landmarks,
            self._mp_pose.POSE_CONNECTIONS, #Official MP skeleton connections
            landmark_drawing_spec=self._mp_drawing_styles.get_default_pose_landmarks_style(),
        )
        return frame

    def close(self):
        """Release MediaPipe resources."""
        self._pose.close()
