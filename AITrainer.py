import cv2
import mediapipe as mp


# current tutorial: https://youtu.be/4WwSJAKRtcA - using landmarks

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

cap = cv2.VideoCapture("videos/curls.mp4")

while True: 
    ret, img = cap.read()
  
    # Display the resulting frame
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    if results.pose_landmarks:
        print(results.pose_landmarks)
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

    cv2.imshow('frame', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()