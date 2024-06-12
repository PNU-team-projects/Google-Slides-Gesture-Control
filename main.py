import cv2
import numpy as np
import math
from cvzone.HandTrackingModule import HandDetector
from tensorflow.keras import models


labels = ["A", "B", "C", "F", "G", "L", "P", "Q", "R", "Y"]
offset = 30
img_size = 300


# Loading the model from files
json_file = open('saved_models/model (1).json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = models.model_from_json(loaded_model_json)

loaded_model.built = True

loaded_model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
loaded_model.load_weights("saved_models/model_weights (1).h5")
# Model is loaded 

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)



while True:
    success, img = cap.read()
    hands, imgWithDetection = detector.findHands(img, draw=False)

    if hands: 
        hand = hands[0]
        x,y,w,h = hand['bbox']

        imgCrop = img[y-offset : y+h+offset, x-offset : x+w+offset]
        finalImage = np.ones((img_size, img_size, 3), np.uint8)*255

        aspectRation = h/w
        if aspectRation > 1:
            k = img_size/h
            wCal = math.floor(k*w)
            wGap = math.floor((img_size-wCal)/2)

            try:
                img_resized = cv2.resize(imgCrop, (wCal, img_size))
                finalImage[:, wGap: wCal+wGap] = img_resized
            except:
                print("error 2")

        else:
            k = img_size/w
            hCal = math.floor(k*h)
            hGap = math.floor((img_size-hCal)/2)

            try:
                img_resized = cv2.resize(imgCrop, (img_size, hCal))
                finalImage[hGap: hCal+hGap, :] = img_resized
            except:
                print("error 2")

        try:
            prediction = loaded_model.predict(np.array([finalImage/255]))
            label = np.argmax(prediction[0])
            print(labels[label])

            cv2.putText(imgWithDetection,  labels[label], (10,450), 1, 3, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("finalImage", finalImage)
        except:
            print("error")

    cv2.imshow("Image", imgWithDetection)
    
    key = cv2.waitKey(3)
    if key == 27: #ESC
        break
