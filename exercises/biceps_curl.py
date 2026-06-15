from config import BICEPS_CURLED_ANGLE, BICEPS_EXTENDED_ANGLE


class BicepsCurlExercise:
    def __init__(self):
        self.name = "Biceps Curl"
        self.count = 0
        self.leftCount = 0
        self.rightCount = 0
        self.leftStage = "down"
        self.rightStage = "down"
        self.stage = "L:down R:down"
        self.feedback = "Start curl"
        self.leftFeedback = "Start curl"
        self.rightFeedback = "Start curl"

    def update(self, angles):
        leftElbow = angles.get("Left Elbow")    #Gets the left elbow angle
        rightElbow = angles.get("Right Elbow")  #Gets the right elbow angle
        #Updates left arm count stage and feedback
        self.leftCount, self.leftStage, self.leftFeedback = self.updateArm(
            leftElbow,  #Sends the left elbow angle into the updateArm
            self.leftCount, #Sends the current left arm count
            self.leftStage, #Sends the current left arm stage
        )
        #Updates right arm count stage and feedback
        self.rightCount, self.rightStage, self.rightFeedback = self.updateArm(
            rightElbow,
            self.rightCount,
            self.rightStage,
        )

        self.count = self.leftCount + self.rightCount #Calculates total reps from left plus right arm
        self.stage = f"L:{self.leftStage} R:{self.rightStage}"  #Creates display text for both arm stages
        self.feedback = f"L:{self.leftFeedback} | R:{self.rightFeedback}"   #Creates one display text for both arm feedback messages

    def updateArm(self, elbowAngle, count, stage):
        if elbowAngle is None:  #Checks if elbow angle cant be calculated
            return count, stage, "Make elbow visible"   #Keeps the count and stage and returns visibility feedback

        feedback = "Curl higher"    #Default feedback when the arm is between down and fully curled

        if elbowAngle < BICEPS_CURLED_ANGLE:    #Checks if arm is curled high enough
            stage = "up"    #Sets the stage to up
            feedback = "Good curl"  #Shows that the curl reached the top position
        elif elbowAngle > BICEPS_EXTENDED_ANGLE and stage == "up":  #Checks if the arm returned down after being up
            count += 1  #Adds one rep to the arm
            stage = "down"  #Sets the stage back to down
            feedback = "Good rep"   #Shows that the rep was counted
        elif elbowAngle > BICEPS_EXTENDED_ANGLE:    #Checked if the arm is extended but was never up
            feedback = "Start curl"
        elif stage == "up": #Checks if the arm was curled and is moving down
            feedback = "Lower arm"

        return count, stage, feedback   #Returns updated count stage feedback for the arm
