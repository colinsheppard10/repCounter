import cv2
import mediapipe as mp


# current tutorial: https://youtu.be/4WwSJAKRtcA - using landmarks

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
# cap = cv2.VideoCapture("videos/raises.mp4")
cap = cv2.VideoCapture(0)

up = False
counter = 0

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

        cv2.circle(img, points[12], 15, (255,0,0), cv2.FILLED)
        cv2.circle(img, points[14], 15, (255,0,0), cv2.FILLED)
        cv2.circle(img, points[11], 15, (255,0,0), cv2.FILLED)
        cv2.circle(img, points[13], 15, (255,0,0), cv2.FILLED)

        if not up and points[14][1] + 40 < points[12][1]:
            print("UP")
            up = True
            counter += 1
        elif points[14][1] > points[12][1]:
            print("Down")
            up = False

    cv2.putText(img, str(counter), (100,150),cv2.FONT_HERSHEY_PLAIN, 12, (255,0,0),12)
    cv2.imshow('frame', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()