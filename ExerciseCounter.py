import os
import time
import numpy as np
import math

def countDown(start):
    while(start > 0):
        os.system('say "%s"' % int(start))
        time.sleep(1)
        start = start - 1

    os.system('say "start"')

def handleReverse(startAngle, angle, endAngle, reduceTop = 0):
    if(endAngle < startAngle):
        angle = angle * -1
        startAngle = startAngle * -1
        endAngle = endAngle * -1
        # reduceTop = reduceTop * -1
    else: 
        reduceTop = reduceTop * -1

    return (startAngle, angle, endAngle, reduceTop)

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

def findDistance(points, dir, reduceTop, p1, p2, p3):
    # Get the landmarks
    x1, y1 = points[p1]
    x2, y2 = points[p2]
    x3, y3 = points[p3]

    y3, y2, y1, reduceTop = handleReverse(y3, y2, y1, reduceTop)

    totalDistance = y1 - y3
    distanceTraveled = y2 - y3
    if dir == 0:
        distanceTraveled = distanceTraveled - reduceTop

    if(totalDistance <= 0 or distanceTraveled <= 0):
        return 0

    if(distanceTraveled / totalDistance > 1):
        return 1

    return distanceTraveled / totalDistance

def findBinary(points, p1, p2):
    x1, y1 = points[p1]
    x2, y2 = points[p2]
    if(y1 > y2):
        return 0
    else: 
        return 100

def countExercise(count, dir, points, exercise):
    anchors = exercise.anchors
    startEndAngles = exercise.startEndAngles
    poseType = exercise.poseType
    reduceTop = exercise.reduceTop
    
    p1, p2, p3 = (anchors[0], anchors[1], anchors[2])
    startAngle, endAngle = startEndAngles

    if poseType == 'ANGLE':
        angle = findAngle(points, p1, p2, p3)
    elif poseType == 'DISTANCE': 
        angle = findDistance(points, dir, reduceTop, p1, p2, p3)
    else: 
        angle = findBinary(points, p1, p2)

    startAngle, angle, endAngle, reduceTop = handleReverse(startAngle, angle, endAngle)
    print('count:' + str(count) + ' dir:' + str(dir) + ' p1:' + str(points[p1])+ ' p2:' + str(points[p2]) + ' p3:' + str(points[p3]) +  '   startAngle:' + str(startAngle) + ' angle:' + str(angle) + ' endAngle:' + str(endAngle))

    percent = np.interp(angle, (startAngle, endAngle), (0, 100))
    bar = np.interp(angle, (startAngle, endAngle), (550, 100))

    color = (255, 0, 255)
    if percent == 100:
        color = (0, 255, 0)
        if dir == 0:
            count += 0.5
            # os.system('say "%s"' % int(count))
            dir = 1
    if percent == 0:
        color = (0, 255, 0)
        if dir == 1:
            count += 0.5
            dir = 0

    return (dir, count, percent, bar, color)