import cv2
import time
import numpy as np
import math
import HandTrackingModule as htm

# Setting camera width and height
widthCam, heightCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, widthCam)
cap.set(4, heightCam)
pTime = 0

# Initializing the object of hand tracking module class
detector = htm.HandDetector(detectionCon=0.65)

while True:
    success, img = cap.read()

    # finding the hand on the image
    img = detector.findHands(img)

    # Getting all the landmark points of the hands
    landmarkList = detector.findPosition(img, draw=False)

    # Getting the value number 4 and 8 ---> 4 is the tip of thumb and 8 is the tip of index finger
    if len(landmarkList) != 0:

        x1, y1 = landmarkList[4][1], landmarkList[4][2]
        x2, y2 = landmarkList[8][1], landmarkList[8][2]

        # getting the centre point between the landmark 4 and 8
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Creating the circle around the 4 and 8 point
        cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)

        # Creating a line to join the two circles
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 4)

        # Circling the middle point between landmark 4 and 8
        cv2.circle(img, (cx, cy), 6, (255, 255, 0), cv2.FILLED)

        # Finding the length of the line between landmark 4 and 8
        length = math.hypot(x2 - x1, y2 - y1)
        print(length)

    # Calculating and printing the FPS in live video
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(
        img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 255), 4
    )

    cv2.imshow("Img", img)
    cv2.waitKey(1)