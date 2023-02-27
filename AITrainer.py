import cv2
import mediapipe as mp
from Exercise import Exercise
from ExerciseCounter import countExercise
# current tutorial: https://youtu.be/4WwSJAKRtcA - using landmarks

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
# cap = cv2.VideoCapture("videos/raises.mp4")
cap = cv2.VideoCapture(0)

# anchor [1,2,3] (2 is pivot), [startAngle, endAngle], [startAbove, startBelow]

#curl / press
# fly / overhead
# shrug / row
# pulldown / situp

# band squat / jump lung
# hip thrust / 

upper = [
    Exercise('crls',[12,14,16], [210, 310], True),
    Exercise('sh p',[6,16,12], [0, 1], False),
]

lower = [
    Exercise('sqts',[24,26,28], [170, 110], True),
    Exercise('sp s',[12,16,24], [0, 1], False)
]

def runExercise(setNumber, exercise):
    count = .5
    dir = 0
    while True: 

        anchors = exercise.anchors
        startEndAngles = exercise.startEndAngles
        isAngle = exercise.isAngle
        reps = exercise.reps
        name = exercise.name

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

            cv2.circle(img, points[anchors[0]], 15, (255,0,0), cv2.FILLED)
            cv2.circle(img, points[anchors[1]], 15, (255,0,0), cv2.FILLED)
            cv2.circle(img, points[anchors[2]], 15, (255,0,0), cv2.FILLED)
            
            dir, count, percent, bar, color = countExercise(count, dir, points, anchors, startEndAngles, isAngle)

            # Draw Bar
            cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
            cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
            cv2.putText(img, f'{int(percent)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                        color, 4)

            # Draw Curl Count
            cv2.rectangle(img, (0, 450), (w - 185, 720), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, str(setNumber) + ':'+ str(int(count)) + ':' + name, (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                        (0, 0, 0), 25)
            
        cv2.imshow('frame', img)

        if(count > reps):
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def runWorkout():
    # curls and press
    runExercise(1, upper[1])
    return


runWorkout()
# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()