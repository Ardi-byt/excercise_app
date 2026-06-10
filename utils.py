import numpy as np

try:
    from config import LANDMARK_INDEX
except ImportError:
    LANDMARK_INDEX = {}


def calculateAngle(a, b, c):
    #Converts the points into a Numpy array
    a_arr = np.array(a, dtype=float)
    b_arr = np.array(b, dtype=float)
    c_arr = np.array(c, dtype=float)

    radians = np.arctan2(c_arr[1] - b_arr[1], c_arr[0] - b_arr[0]) - np.arctan2(
        a_arr[1] - b_arr[1], a_arr[0] - b_arr[0]
    )
    angle = abs(radians * 180.0 / np.pi) #Converts from radians to degrees and takes the absolute number

    if angle > 180.0:
        angle = 360.0 - angle

    return float(angle)

#Converts landmark name or index into an int
def getLandmarkIndex(landmark, landmark_index=None):
    if isinstance(landmark, int): #If the landmark is already int it just returns it
        return landmark

    if not isinstance(landmark, str):   #If landmark is a string it returns null
        return None

    #Uses index map or else it uses the default LANDMARK_INDEX
    index_map = landmark_index if landmark_index is not None else LANDMARK_INDEX 
    return index_map.get(landmark) #Returns the index of the landmark or None if it doesnt exist

#Returns the x,y coordinates of the landmark
def getLandmarkPoint(landmarks, landmark, min_visibility=0.5, landmark_index=None):
    if not landmarks: #Checks if there are no landmarks and returns none if that is true
        return None
    #Converts the landmark into an index
    idx = getLandmarkIndex(landmark, landmark_index=landmark_index)
    if idx is None or idx < 0 or idx >= len(landmarks): #Checks if index is missing or it is outside of the range and return None
        return None

    point = landmarks[idx]
    visibility = float(point.get("visibility", 1.0)) #Safety fallback if visibility doesnt exist it sets it to 1.0
    if visibility < min_visibility: #Checks if the landmark is not visible enough and returns None
        return None

    return float(point["x"]), float(point["y"]) #Returns the x,y coordinates


def safeAngle(
    landmarks,
    point_a,
    point_b,
    point_c,
    min_visibility=0.5,
    landmark_index=None,
):
    #Tries to get coordinates for a,b and c
    a = getLandmarkPoint(
        landmarks, point_a, min_visibility=min_visibility, landmark_index=landmark_index
    )
    b = getLandmarkPoint(
        landmarks, point_b, min_visibility=min_visibility, landmark_index=landmark_index
    )
    c = getLandmarkPoint(
        landmarks, point_c, min_visibility=min_visibility, landmark_index=landmark_index
    )
    #If one of the coordinates doesnt exist it doesnt return anything
    if a is None or b is None or c is None:
        return None

    return calculateAngle(a, b, c) #Calculates the angle with the function

