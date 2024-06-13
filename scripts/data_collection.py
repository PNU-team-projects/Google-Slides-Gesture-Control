import cv2
import numpy as np
import math
from cvzone.HandTrackingModule import HandDetector


offset = 30
img_size = 300


cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

SIGN = "L"
counter = 0


while True:
    success, img = cap.read()
    hands, imgWithDetection = detector.findHands(img, draw=False)

    if hands: 
        hand = hands[0]
        x,y,w,h = hand['bbox']

        imgCrop = img[y-offset : y+h+offset, x-offset : x+w+offset]
        
        if imgCrop is not None:
            finalImage = np.ones((img_size, img_size, 3), np.uint8)*255

            aspectRation = h/w
            if aspectRation > 1:
                k= img_size/h
                wCal = math.floor(k*w)
                wGap = math.floor((img_size-wCal)/2)

                try:
                    img_resized = cv2.resize(imgCrop, (wCal, img_size))
                    finalImage[:, wGap: wCal+wGap] = img_resized
                except:
                    print("error 2")
            else:
                k= img_size/w
                hCal = math.floor(k*h)
                hGap = math.floor((img_size-hCal)/2)
                
                try:
                    img_resized = cv2.resize(imgCrop, (img_size, hCal))
                    finalImage[hGap: hCal+hGap, :] = img_resized
                except:
                    print("error 2")

            try:
                cv2.imshow("imgCrop", imgCrop)
                cv2.imshow("finalImage", finalImage)
            except:
                print("error")

    cv2.imshow("Image", imgWithDetection)
    key = cv2.waitKey(1)

    if key == ord("s"):
        counter +=1
        cv2.imwrite(f'../data/{SIGN}/{SIGN}_{counter}.jpg', finalImage)
        print(counter)
    elif key == 27: #ESC
        break
