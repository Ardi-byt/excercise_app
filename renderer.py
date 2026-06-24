import cv2

from config import ANGLE_DEFINITIONS


def drawStatus(frame, landmarks):
    statusText = "Person detected" if landmarks else "No person detected"
    cv2.putText(frame, statusText, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)


def drawInstructions(frame):
    cv2.putText(frame, "Press q to quit", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, "1 Squat | 2 Biceps Curl | 3 Push-up", (20, 285), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)


def drawExerciseInfo(frame, exercise):
    cv2.putText(frame, f"Exercise: {exercise.name}", (20, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

    if exercise.name == "Biceps Curl":
        cv2.putText(frame, f"Left reps: {exercise.leftCount} | Right reps: {exercise.rightCount}", (20, 165), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 255, 255), 2)
        cv2.putText(frame, f"Stage: {exercise.stage}", (20, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)
        cv2.putText(frame, f"Feedback: {exercise.feedback}", (20, 245), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)
    else:
        cv2.putText(frame, f"Reps: {exercise.count}", (20, 165), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
        cv2.putText(frame, f"Stage: {exercise.stage}", (20, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(frame, f"Feedback: {exercise.feedback}", (20, 245), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)


def drawAngles(frame, angles):
    panelX = frame.shape[1] - 360
    panelY = 10
    panelW = 350
    panelH = 28 + (len(ANGLE_DEFINITIONS) * 24)

    cv2.rectangle(frame, (panelX, panelY), (panelX + panelW, panelY + panelH), (20, 20, 20), -1)
    cv2.putText(frame, "Joint Angles", (panelX + 10, panelY + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

    y = panelY + 46
    for label in ANGLE_DEFINITIONS:
        if label in angles:
            text = f"{label}: {angles[label]:.1f}"
        else:
            text = f"{label}: N/A"

        cv2.putText(frame, text, (panelX + 10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 255, 200), 1)
        y += 24


def renderOverlay(frame, landmarks, angles, exercise):
    drawStatus(frame, landmarks)
    drawInstructions(frame)
    drawAngles(frame, angles)
    drawExerciseInfo(frame, exercise)
