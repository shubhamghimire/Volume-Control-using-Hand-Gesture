import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm

prevTime = 0
curTime = 0

cap = cv2.VideoCapture(0)

detector = htm.HandDetector()
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    landmarkList = detector.findPosition(img)
    if len(landmarkList) != 0:
        print(landmarkList[4])
    curTime = time.time()
    fps = 1 / (curTime - prevTime)
    prevTime = curTime

    cv2.putText(
        img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 255), 4
    )
    cv2.imshow("Image", img)
    cv2.waitKey(1)
