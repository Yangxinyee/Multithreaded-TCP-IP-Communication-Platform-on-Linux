import math
import random
import cvzone
import numpy as np
import cv2
from cvzone.HandTrackingModule import HandDetector
cap= cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)


class SnakeGameClass:

    def __init__(self, pathFood):
        self.points = []  # a list of all points of the snake
        self.lengths = []  # distance between each point
        self.currentLength = 0  # total length of the snake
        self.allowedLength = 150  # total allowed length of the snake
        self.previousHead = 0, 0  # previous head point
        self.gameOver = 0

        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoints = 0, 0
        self.randomFoodLocation()
        self.score = 0

    def randomFoodLocation(self):
        self.foodPoints = random.randint(100, 1000), random.randint(100, 600)

    def update(self, imgMain, currentHead):
        if self.gameOver == 0:
            cvzone.putTextRect(imgMain, "VisionGame-Snake", [140, 320], scale=7, thickness=6, offset=20)
            cvzone.putTextRect(imgMain, "Start Game", [380, 480], scale=5, thickness=4, offset=20)
            cvzone.putTextRect(imgMain, "Press s or S", [350, 620], scale=5, thickness=4, offset=20)
        if self.gameOver == 1:
            cvzone.putTextRect(imgMain, "Game Over", [300, 330], scale=7, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f"Your Scores:{self.score}", [200, 460], scale=7, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, "Press r to restart", [450, 600], scale=2, thickness=3, offset=10)
            cvzone.putTextRect(imgMain, "Press x to exit", [480, 650], scale=2, thickness=3, offset=10)
        elif self.gameOver == 2:
            px, py = self.previousHead
            cx, cy = currentHead
            self.points.append([cx, cy])
            distance = math.hypot(cx - px, cy - py)
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = cx, cy
            # Length reduction
            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.points.pop(i)
                    self.lengths.pop(i)
                    if self.currentLength < self.allowedLength:
                        break
            # Check if snake eat the food
            rx, ry = self.foodPoints
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                self.randomFoodLocation()
                self.allowedLength += 50
                self.score += 1
                print(self.score)
            # Draw snake
            if self.points:
                for i, points in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, self.points[i - 1], self.points[i], (0, 0, 255), 20)
                cv2.circle(imgMain, self.points[-1], 20, (200, 0, 200), cv2.FILLED)
            # Draw food
            rx, ry = self.foodPoints
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood, (rx - self.wFood // 2, ry - self.hFood // 2))
            cvzone.putTextRect(imgMain, f"Scores:{self.score}", [50, 80], scale=3, thickness=3, offset=10)
            # Check for collision
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imgMain, [pts], False, (0, 200, 0), 3)
            minDist = cv2.pointPolygonTest(pts, (cx, cy), True)
            if -1 <= minDist <= 1:
                print("游戏结束！")
                self.gameOver = 1
                self.points = []  # a list of all points of the snake
                self.lengths = []  # distance between each point
                self.currentLength = 0  # total length of the snake
                self.allowedLength = 150  # total allowed length of the snake
                self.previousHead = 0, 0  # previous head point
                self.randomFoodLocation()
        return imgMain


game = SnakeGameClass('Dount.png')
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        img = game.update(img, pointIndex)
    cv2.imshow("VisionGameSnake", img)
    key = cv2.waitKey(1)
    if key == ord('r') or key == ord('R'):
        game.gameOver = 2
    if key == ord('s') or key == ord('S'):
        game.gameOver = 2
    if key == ord('x') or key == ord('X') or cv2.getWindowProperty('VisionGameSnake', cv2.WND_PROP_VISIBLE) < 1.0:
        break
cap.release()
cv2.destroyAllWindows()
