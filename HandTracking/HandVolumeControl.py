import cv2
import time
import numpy as np

widthCam, heightCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, widthCam)
cap.set(4, heightCam)
pTime = 0

while True:
    success, img = cap.read()

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(
        img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 255), 4
    )

    cv2.imshow("Img", img)
    cv2.waitKey(1)