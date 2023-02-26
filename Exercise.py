import math

def findAngle(points, p1, p2, p3):

    # Get the landmarks
    x1, y1 = points[p1]
    x2, y2 = points[p2]
    x3, y3 = points[p3]

    # Calculate the Angle
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                          math.atan2(y1 - y2, x1 - x2))
    if angle < 0:
        angle += 360

    # print(angle)
    return angle
