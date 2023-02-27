import numpy as np
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

def countExercise(count, dir, points, p1, p2, p3):
    angle = findAngle(points, p1, p2, p3)

    percent = np.interp(angle, (210, 310), (0, 100))
    bar = np.interp(angle, (220, 310), (650, 100))

    print('per:',percent, ' dir:', dir, ' count:', count)
    color = (255, 0, 255)
    if percent == 100:
        color = (0, 255, 0)
        if dir == 0:
            count += 0.5
            dir = 1
    if percent == 0:
        color = (0, 255, 0)
        if dir == 1:
            count += 0.5
            dir = 0

    return (dir, count, percent, bar, color)