from config import BICEPS_CURLED_ANGLE, BICEPS_EXTENDED_ANGLE


class BicepsCurlExercise:
    def __init__(self):
        self.name = "Biceps Curl"
        self.count = 0
        self.stage = "down"
        self.feedback = "Start curl"

    def update(self, angles):
        leftElbow = angles.get("Left Elbow")    #Gets the left elbow angle
        rightElbow = angles.get("Right Elbow")  #Gets the right elbow angle
        #Keeps only the available and seen elbow angles
        validElbows = [angle for angle in (leftElbow, rightElbow) if angle is not None]
        if not validElbows: #Checks if neither elbows are visible
            self.feedback = "Make elbows visible"   #Live feedback to make them visible if they are not 
            return
        #Calculates average elbow angle from the visible elbows
        elbowAngle = sum(validElbows) / len(validElbows)
        self.feedback = "Curl higher"   #Default feedback when the user did not curl high enough
        #Checks if the arm has reached the top position
        if elbowAngle < BICEPS_CURLED_ANGLE:
            self.stage = "up"   #Updates the stage to up
            self.feedback = "Good curl" #Shows that the curl is good enough
        #Checks if arm returned down after being curled    
        elif elbowAngle > BICEPS_EXTENDED_ANGLE and self.stage == "up": 
            self.count += 1 #Adds 1 after completed rep
            self.stage = "down" #Sets the stage back to down
            self.feedback = "Good rep"  #Shows that one rep was counted
        #Checks if arm is already extended
        elif elbowAngle > BICEPS_EXTENDED_ANGLE:
            self.feedback = "Start curl"    #Tells the user to start the curl
        elif self.stage == "up":    #Checks if user is coming down after the up position
            self.feedback = "Lower arm" #Tells the user to lower the arm
