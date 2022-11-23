import cv2
import mediapipe as mp
import time


class HandDetector:
    def __init__(
        self, mode=False, maxHands=2, model_compelxity=1, detectionCon=0.2, trackCon=0.5
    ):
        self.mode = mode
        self.maxHands = maxHands
        self.model_complexity = model_compelxity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.mode,
            self.maxHands,
            self.model_complexity,
            self.detectionCon,
            self.trackCon,
        )
        self.mpDraw = mp.solutions.drawing_utils

    # Detecting hands on the video
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS
                    )

        return img

    # Returning the hand landmarks
    def findPosition(self, img, handNo=0, draw=True):

        landmarkList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for (
                id,
                lm,
            ) in enumerate(myHand.landmark):

                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarkList.append([id, cx, cy])
                # print(id, cx, cy)
                if len(landmarkList) != 0:
                    if draw:
                        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        return landmarkList


def main():
    pass


if __name__ == "__main__":
    main()