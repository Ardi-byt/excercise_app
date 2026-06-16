from config import PUSHUP_BODY_STRAIGHT_ANGLE, PUSHUP_DOWN_ANGLE, PUSHUP_UP_ANGLE


class PushUpExercise:
    def __init__(self):
        self.name = "Push-up"
        self.count = 0
        self.stage = "up"
        self.feedback = "Start push-up"

    def update(self, angles):
        leftElbow = angles.get("Left Elbow")    #Gets left elbow angle
        rightElbow = angles.get("Right Elbow")  #Gets right elbow angle 
        leftBody = angles.get("Left Body")      #Gets left body angle, shoulder, hip, ankle
        rightBody = angles.get("Right Body")    #Gets right body angle, shoulder, hip, ankle
        #Keeps only the elbow and body angles that were successfully calculated 
        validElbows = [angle for angle in (leftElbow, rightElbow) if angle is not None]
        validBodyAngles = [angle for angle in (leftBody, rightBody) if angle is not None]
        #Checks if neither elbow angle is visible
        if not validElbows:
            self.feedback = "Make elbows visible"
            return
        #Checks if neither body angle is visible
        if not validBodyAngles:
            self.feedback = "Make body visible"
            return
        #Calculates the average elbow and body angle from the visible elbows or body
        elbowAngle = sum(validElbows) / len(validElbows)
        bodyAngle = sum(validBodyAngles) / len(validBodyAngles)
        bodyIsStraight = bodyAngle > PUSHUP_BODY_STRAIGHT_ANGLE #Check if the body angle is straight enough

        if not bodyIsStraight:  #Checks if body is not straight enough
            self.feedback = "Keep body straight"  #Gives feedback to straighten body
            return

        self.feedback = "Go lower"  #Default feedback when the user hasnt reached the bottom position

        if elbowAngle < PUSHUP_DOWN_ANGLE:  #Checks if elbows are bent enough for bottom position
            self.stage = "down" #Sets the stage to down
            self.feedback = "Good depth"    #Gives feedback that the user went down enough
        elif elbowAngle > PUSHUP_UP_ANGLE and self.stage == "down": #Check if user returned up after being down
            self.count += 1 #Adds one rep
            self.stage = "up"   #Sets the stage to up
            self.feedback = "Good push-up"  #Feedback that the rep was counted
        elif elbowAngle > PUSHUP_UP_ANGLE:  #Check if user is already in top position but has not gone down yet
            self.feedback = "Start push-up" #Tells the user to start the push up
        elif self.stage == "down":  #Checks if user is currently coming back up from the down stage
            self.feedback = "Push up"   #Tells the user to push back up
