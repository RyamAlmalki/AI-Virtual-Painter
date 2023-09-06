import os
import cv2
import numpy as np
import HandTrackingModule as htm


# Here we will the folder path of the top image
folderPath = "paint"
myList = os.listdir(folderPath)

brushThickness = 15
xp, yp = 0, 0

# here we will loop to get the image inside the folder
overlaylist = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlaylist.append(image)
header = overlaylist[0]

drawColor = (255, 0, 255)
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)


detector = htm.handDetector(detectionCon=0.85)


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)

    if len(lmlist) != 0:
        # tip of index
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]

        fingers = detector.fingersUp()

        if fingers[1] and fingers[2]:
            if y1 < 125:
                if 0 < x1 < 100:
                    drawColor = (255,0,255)
                if 200 < x1 < 300:
                    drawColor = (255,0,0)
                if 500 < x1 < 600:
                    drawColor = (0, 255,0)
            cv2.rectangle(img, (x1, y1 - 15), (x2, y2 + 15), drawColor, cv2.FILLED)

        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            if xp==0 and yp ==0:
                xp, yp = x1, y1
            cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
            cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1

    img[0:98, 0:635] = header
    cv2.imshow("Video", img)
    cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1)







