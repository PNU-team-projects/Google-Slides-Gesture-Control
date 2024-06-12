import cv2
import numpy as np
import math
import argparse
from cvzone.HandTrackingModule import HandDetector
# from tensorflow.keras import models


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import os

# Google account authentication
options = webdriver.ChromeOptions()
username = os.getenv('username')
options.add_argument(f"user-data-dir=c://Users//{username}//AppData//Local//Google//Chrome//User Data")

driver = webdriver.Chrome(options=options)



def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)

    parser.add_argument("--url",type=str,help="url to presentation")

    args = parser.parse_args()

    return args

fullscreen = False

def slides_manipulate(command):
    global fullscreen
    actions = ActionChains(driver) 
    if command == "A":
        if fullscreen:
            driver.maximize_window()
            fullscreen = False
        else:
            driver.fullscreen_window()
            fullscreen = True
    elif command == "B":
        actions.key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys(Keys.F5).key_up(Keys.SHIFT).key_up(Keys.CONTROL)
    elif command == "C":
        actions.key_down(Keys.CONTROL).send_keys(Keys.F5).key_up(Keys.CONTROL)
    elif command == "D":
        actions.key_down(Keys.ARROW_RIGHT)
    elif command == "E":
        actions.key_down(Keys.ARROW_LEFT)
    elif command == "F":
        actions.key_down(Keys.ESCAPE)
    elif command == "G":
        actions.key_down(Keys.CONTROL).send_keys(Keys.ARROW_UP).key_up(Keys.CONTROL)
    elif command == "H":
        actions.key_down(Keys.CONTROL).send_keys(Keys.ARROW_DOWN).key_up(Keys.CONTROL)
    actions.perform()



# labels = ["A", "B", "C", "F", "G", "L", "P", "Q", "R", "Y"]
# offset = 30
# img_size = 300


# Loading the model from files
# json_file = open('saved_models/model (1).json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# loaded_model = models.model_from_json(loaded_model_json)

# loaded_model.built = True

# loaded_model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
# loaded_model.load_weights("saved_models/model_weights (1).h5")
# Model is loaded 


args = get_args()

url = args.url

last_manipalution_time = 0

cap_device = args.device
cap_width = args.width
cap_height = args.height

cap = cv2.VideoCapture(cap_device)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)

detector = HandDetector(maxHands=1)

try:
    if url is not None:
        driver.get(url = url)
        
        # click to the first slide to correct slides moving up/down
        try:
            first_slide = driver.find_element(By.XPATH, '//*[@id="filmstrip-slide-0-p-bg"]')
            first_slide.click()
        except Exception as ex:
            print("Add some slides to your presentation or try to click manually to any slide")
    else:
        print('URL is not defined. Use "--url yourpresentationlink" when starting program')
        exit()

    while True:
        success, img = cap.read()
        # hands, imgWithDetection = detector.findHands(img, draw=False)

        # if hands: 
        #     hand = hands[0]
        #     x,y,w,h = hand['bbox']

        #     imgCrop = img[y-offset : y+h+offset, x-offset : x+w+offset]
        #     finalImage = np.ones((img_size, img_size, 3), np.uint8)*255

        #     aspectRation = h/w
        #     if aspectRation > 1:
        #         k = img_size/h
        #         wCal = math.floor(k*w)
        #         wGap = math.floor((img_size-wCal)/2)

        #         try:
        #             img_resized = cv2.resize(imgCrop, (wCal, img_size))
        #             finalImage[:, wGap: wCal+wGap] = img_resized
        #         except:
        #             print("error 2")

        #     else:
        #         k = img_size/w
        #         hCal = math.floor(k*h)
        #         hGap = math.floor((img_size-hCal)/2)

        #         try:
        #             img_resized = cv2.resize(imgCrop, (img_size, hCal))
        #             finalImage[hGap: hCal+hGap, :] = img_resized
        #         except:
        #             print("error 2")

        #     try:
        #         prediction = loaded_model.predict(np.array([finalImage/255]))
        #         label = np.argmax(prediction[0])
        #         print(labels[label])

        #         cv2.putText(imgWithDetection,  labels[label], (10,450), 1, 3, (0, 255, 0), 2, cv2.LINE_AA)
        #         cv2.imshow("finalImage", finalImage)
        #     except:
        #         print("error")
        
        # perform actions only once per 3 seconds
        current_time = time.time()  
        if current_time - last_manipalution_time >= 3: 
            command = input()
            if command is not None:
                slides_manipulate(command)
            last_manipalution_time = current_time



        cv2.imshow("Broadcast from camera", img)
        
        key = cv2.waitKey(3)
        if key == 27: #ESC
            break
except Exception as ex:
    print(ex)
finally:
    driver.close()
    cap.release()
    cv2.destroyAllWindows()