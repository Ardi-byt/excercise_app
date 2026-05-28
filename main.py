import cv2

from config import CAMERA_INDEX, FRAME_HEIGHT, FRAME_WIDTH, WINDOW_NAME
from pose_detector import PoseDetector


def main() -> None:
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not cap.isOpened():
        raise RuntimeError("Could not access webcam. Check permissions or CAMERA_INDEX.")

    detector = PoseDetector()

    try:
        while True:
            success, frame = cap.read()
            if not success:
                continue

            frame = cv2.flip(frame, 1)

            results = detector.detect_pose(frame)
            landmarks = detector.get_landmarks(results)
            frame = detector.draw_landmarks(frame, results)

            status_text = "Person detected" if landmarks else "No person detected"
            cv2.putText(frame, status_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.putText(frame, "Press q to quit", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            cv2.imshow(WINDOW_NAME, frame)

            if (cv2.waitKey(1) & 0xFF) == ord("q"):
                break
    finally:
        detector.close()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
