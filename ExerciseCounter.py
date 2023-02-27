import numpy as np
import math

def handleReverse(startAngle, angle, endAngle):
    if(endAngle < startAngle):
        angle = angle * -1
        startAngle = startAngle * -1
        endAngle = endAngle * -1

    return (startAngle, angle, endAngle)

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

    return angle

def findDistance(points, p1, p2, p3):
    # Get the landmarks
    x1, y1 = points[p1]
    x2, y2 = points[p2]
    x3, y3 = points[p3]

    print('y1:' + str(y1) + ' y2:' + str(y2) + ' y3:' + str(y3))

    y1 = y1 * -1
    y2 = y2 * -1
    y3 = y3 * -1

    totalDistance = y1 - y3
    distanceTraveled = y2 - y3 - 100

    if(totalDistance <= 0 or distanceTraveled <= 0):
        return 0

    if(distanceTraveled / totalDistance > 1):
        return 1

    return distanceTraveled / totalDistance

def countExercise(count, dir, points, anchors, startEndAngles, isAngle):
    p1, p2, p3 = (anchors[0], anchors[1], anchors[2])
    startAngle, endAngle = startEndAngles

    if isAngle:
        angle = findAngle(points, p1, p2, p3)
    else: 
        angle = findDistance(points, p1, p2, p3)

    startAngle, angle, endAngle = handleReverse(startAngle, angle, endAngle)

    percent = np.interp(angle, (startAngle, endAngle), (0, 100))
    bar = np.interp(angle, (startAngle, endAngle), (550, 100))

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

    print('count' + str(count) + 'angle:' + str(angle))
    return (dir, count, percent, bar, color)