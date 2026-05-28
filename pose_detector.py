"""MediaPipe Pose wrapper for landmark detection and drawing."""

import cv2
import mediapipe as mp

from config import (
    POSE_MIN_DETECTION_CONFIDENCE,
    POSE_MIN_TRACKING_CONFIDENCE,
    POSE_MODEL_COMPLEXITY,
    POSE_SMOOTH_LANDMARKS,
)


class PoseDetector:
    """Class for detecting body pose with MediaPipe """

    def __init__(self):
        self._mp_pose = mp.solutions.pose
        self._mp_drawing = mp.solutions.drawing_utils
        self._mp_drawing_styles = mp.solutions.drawing_styles

        self._pose = self._mp_pose.Pose(
            static_image_mode=False,
            model_complexity=POSE_MODEL_COMPLEXITY,
            smooth_landmarks=POSE_SMOOTH_LANDMARKS,
            min_detection_confidence=POSE_MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=POSE_MIN_TRACKING_CONFIDENCE,
        )

    def detect_pose(self, frame):
        """Run pose detection on a BGR frame and return raw MediaPipe results."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        results = self._pose.process(rgb)
        rgb.flags.writeable = True
        return results

    @staticmethod
    def get_landmarks(results):
        """Convert MediaPipe landmarks into a list of plain dictionaries."""
        if not results or not results.pose_landmarks:
            return None

        landmarks = []
        for lm in results.pose_landmarks.landmark:
            landmarks.append(
                {
                    "x": float(lm.x),
                    "y": float(lm.y),
                    "z": float(lm.z),
                    "visibility": float(lm.visibility),
                }
            )
        return landmarks

    def draw_landmarks(self, frame, results):
        """Draw pose landmarks and connections on a frame."""
        if not results or not results.pose_landmarks:
            return frame

        self._mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            self._mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self._mp_drawing_styles.get_default_pose_landmarks_style(),
        )
        return frame

    def close(self):
        """Release MediaPipe resources."""
        self._pose.close()
