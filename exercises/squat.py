from config import SQUAT_DOWN_ANGLE, SQUAT_UP_ANGLE


class SquatExercise:
    def __init__(self):
        self.name = "Squat"
        self.count = 0
        self.stage = "up"
        self.feedback = "Start squat"

    #Updates the squat count and the current stage of the squat
    def update(self, angles):
        leftKnee = angles.get("Left Knee") #Gets left knee angle
        rightKnee = angles.get("Right Knee") #Gets right knee angle
        #keeps only the angles that are available
        validKnees = [angle for angle in (leftKnee, rightKnee) if angle is not None]
        if not validKnees: #Checks if neither knees are available
            self.feedback = "Make knees visible"
            return

        kneeAngle = sum(validKnees) / len(validKnees)   #Calculates the average knee angle from the available knees
        self.feedback = "Go lower"

        if kneeAngle < SQUAT_DOWN_ANGLE:    #Check if user reached the bottom squat position > 90 degrees
            self.stage = "down"
            self.feedback = "Good depth"
        elif kneeAngle > SQUAT_UP_ANGLE and self.stage == "down":   #Checks if user returned up after being down
            self.count += 1     #Adds 1 rep
            self.stage = "up"   #Changes the stage of the squat
            self.feedback = "Good squat"
        elif kneeAngle > SQUAT_UP_ANGLE:
            self.feedback = "Start squat"
        elif self.stage == "down":
            self.feedback = "Stand up"
