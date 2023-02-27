import cv2
import mediapipe as mp

from ExerciseCounter import countExercise, findAngle


# current tutorial: https://youtu.be/4WwSJAKRtcA - using landmarks

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
# cap = cv2.VideoCapture("videos/raises.mp4")
cap = cv2.VideoCapture(0)

up = False
count = .5
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


        exercise = [12,14,16]

        cv2.circle(img, points[exercise[0]], 15, (255,0,0), cv2.FILLED)
        cv2.circle(img, points[exercise[1]], 15, (255,0,0), cv2.FILLED)
        cv2.circle(img, points[exercise[2]], 15, (255,0,0), cv2.FILLED)
        
        dir, count, percent, bar, color = countExercise(count, dir, points, exercise[0], exercise[1], exercise[2])

        # Draw Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(percent)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                    color, 4)

        # Draw Curl Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)
        
    cv2.imshow('frame', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()