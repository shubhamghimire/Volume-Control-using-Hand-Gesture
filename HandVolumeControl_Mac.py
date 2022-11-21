import cv2
import time
import numpy as np
import math
import HandTrackingModule as htm
import osascript


# Setting camera width and height
widthCam, heightCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, widthCam)
cap.set(4, heightCam)
pTime = 0

# Initializing the object of hand tracking module class
detector = htm.HandDetector(detectionCon=0.65)

# Volume settings on Mac
minVol = 0
maxVol = 100
vol = 0
volBar = 400
volPer = 0

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

        # Hand Range 32 ~ 300
        # Volume Range 0 ~ 100

        vol = np.interp(length, [32, 280], [minVol, maxVol])
        volBar = np.interp(length, [32, 280], [400, 150])
        volPer = np.interp(length, [32, 280], [0, 100])
        # print(length, vol)

        # Executing the volume according to the finger index length
        vol = "set volume output volume " + str(vol)
        osascript.osascript(vol)

        if length < 32:
            cv2.circle(img, (cx, cy), 6, (0, 0, 0), cv2.FILLED)

    # Creating a Volume bar on the screen
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(
        img, f"{int(volPer)} %", (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 250, 0), 4
    )

    # Calculating and printing the FPS in live video
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(
        img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3
    )

    cv2.imshow("Img", img)
    cv2.waitKey(1)