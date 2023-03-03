
import cv2
import mediapipe as mp
from enum import Enum
from Exercise import Exercise
from ExerciseCounter import countDown, countExercise
# current tutorial: https://youtu.be/4WwSJAKRtcA - using landmarks

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
# cap = cv2.VideoCapture("videos/raises.mp4")
cap = cv2.VideoCapture(0)

# class syntax
class PoseType:
    ANGLE = 'ANGLE'
    DISTANCE = 'DISTANCE'
    BINARY = 'BINARY'

upper = [
    Exercise('PULL UP',[6,16,0], [0, 1], 2, 150, True, PoseType.BINARY),
    Exercise('PUSH UP',[14,6,0], [0, 1], 2, 0, False, PoseType.BINARY),
    Exercise('CURLS',[12,14,16], [210, 310], 10, 0, False, PoseType.ANGLE),
    Exercise('SHR PRS',[16,0,0], [0, 1], 10, 100, False, PoseType.BINARY),
    Exercise('SID RAS',[16,12,0], [0, 1], 10, 100, False, PoseType.BINARY),
    Exercise('OVR HED',[16,6,0], [0, 1], 10, 0, True, PoseType.BINARY),
    Exercise('PUL DWN',[16,14,0], [0, 1], 10, 0, True, PoseType.BINARY),
]
lower = [
    Exercise('SQUAT',[24,26,28], [170, 110], 10, 0, False, PoseType.ANGLE),
    Exercise('SPT SQT',[16,12,0], [0, 1], 10, 100, False, PoseType.BINARY),
    Exercise('1LG SQT',[24,26,0], [0, 1], 10, 100, True, PoseType.BINARY),
]

def runExercise(setNumber, exercise):
    anchors = exercise.anchors
    startInverted = exercise.startInverted
    reps = exercise.reps
    name = exercise.name

    count = -.5 if startInverted else .5
    dir = 0

    while True: 
        ret, img = cap.read()
        # Display the resulting frame
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

            points = {}
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                points[id] = (cx, cy)
            
            # Count rep
            dir, count, percent, bar, color = countExercise(count, dir, points, exercise)

            # Draw circles used on body
            cv2.circle(img, points[anchors[0]], 15, (255,0,0), cv2.FILLED)
            cv2.circle(img, points[anchors[1]], 15, (255,0,0), cv2.FILLED)
            cv2.circle(img, points[anchors[2]], 15, (255,0,0), cv2.FILLED)

            # Draw Bar
            cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
            cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
            cv2.putText(img, f'{int(percent)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                        color, 4)

            # Draw Curl Count
            cv2.rectangle(img, (0, 530), (w - 185, 720), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, str(setNumber) + ' : '+ str(int(count)) + ' : ' + name, (45, 670), cv2.FONT_HERSHEY_PLAIN, 8,
                        (0, 0, 0), 25)
            
        cv2.imshow('frame', img)

        if(count > reps):
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def runWorkout():
    for setNumber in range(1, 5):
        for exerciseIndex in range(0, 2):
            runExercise(setNumber, upper[exerciseIndex])
    return

runWorkout()
# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()