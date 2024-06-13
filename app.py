import cv2
import numpy as np
import math
import time
import argparse
from cvzone.HandTrackingModule import HandDetector
from tensorflow.keras import models

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)

    parser.add_argument("--url",type=str,help="url to presentation")

    args = parser.parse_args()

    return args

def load_model():
    json_file = open('saved_models/model_3.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = models.model_from_json(loaded_model_json)

    loaded_model.built = True

    loaded_model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    loaded_model.load_weights("saved_models/model_weights_3.h5")
    
    return loaded_model


driver = webdriver.Chrome()
loaded_model = load_model()
args = get_args()

labels = ["A", "B", "C", "F", "G", "L", "P", "Q", "R"]
fullscreen = False
offset = 30
img_size = 300

url = args.url
cap_device = args.device
cap_width = args.width
cap_height = args.height

last_manipulation_time = 0
gesture_start_time = None
current_gesture = None

def slides_manipulate(command):
    global fullscreen
    actions = ActionChains(driver) 
    if command == "L":
        if fullscreen:
            driver.maximize_window()
            fullscreen = False
        else:
            driver.fullscreen_window()
            fullscreen = True
    elif command == "A":
        actions.key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys(Keys.F5).key_up(Keys.SHIFT).key_up(Keys.CONTROL)
    elif command == "F":
        actions.key_down(Keys.CONTROL).send_keys(Keys.F5).key_up(Keys.CONTROL)
    elif command == "G":
        actions.key_down(Keys.ARROW_RIGHT).key_up(Keys.ARROW_RIGHT)
    elif command == "P":
        actions.key_down(Keys.ARROW_LEFT).key_up(Keys.ARROW_LEFT)
    elif command == "C":
        actions.key_down(Keys.ESCAPE).key_up(Keys.ESCAPE)
    elif command == "R":
        actions.key_down(Keys.CONTROL).send_keys(Keys.ARROW_UP).key_up(Keys.CONTROL)
    elif command == "Q":
        actions.key_down(Keys.CONTROL).send_keys(Keys.ARROW_DOWN).key_up(Keys.CONTROL)
    elif command == "B":
        exit()
    actions.perform()



cap = cv2.VideoCapture(cap_device)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)

detector = HandDetector(maxHands=1)

def preprocess_image(img, bbox, img_size=300, offset=30):

    x, y, w, h = bbox

    imgCrop = img[y-offset : y+h+offset, x-offset : x+w+offset]
    finalImage = np.ones((img_size, img_size, 3), np.uint8) * 255

    aspectRatio = h / w
    if aspectRatio > 1:
        k = img_size / h
        wCal = math.floor(k * w)
        wGap = math.floor((img_size - wCal) / 2)
        try:
            img_resized = cv2.resize(imgCrop, (wCal, img_size))
            finalImage[:, wGap: wCal + wGap] = img_resized
        except Exception as e:
            print("Error resizing image: ", e)
    else:
        k = img_size / w
        hCal = math.floor(k * h)
        hGap = math.floor((img_size - hCal) / 2)
        try:
            img_resized = cv2.resize(imgCrop, (img_size, hCal))
            finalImage[hGap: hCal + hGap, :] = img_resized
        except Exception as e:
            print("Error resizing image: ", e)
    
    finalImage = cv2.cvtColor(finalImage, cv2.COLOR_BGR2GRAY)
    finalImage = finalImage / 255.0
    return finalImage



try:
    if url is not None:
        driver.get(url=url)
        
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
        hands, imgWithDetection = detector.findHands(img, draw=False)

        if hands: 
            hand = hands[0]
            bbox = hand['bbox']

            finalImage = preprocess_image(img, bbox)

            try:
                prediction = loaded_model.predict(np.array([finalImage]))
                label = np.argmax(prediction[0])
                gesture = labels[label]

                if current_gesture is None or current_gesture != gesture:
                    current_gesture = gesture
                    gesture_start_time = time.time()
                elif time.time() - gesture_start_time >= 1:
                    print(f"Gesture {gesture} recognized")
                    slides_manipulate(gesture)
                    gesture_start_time = None
                    current_gesture = None

                cv2.putText(imgWithDetection, labels[label], (10, 450), 1, 3, (0, 255, 0), 2, cv2.LINE_AA)
                # cv2.imshow("finalImage", finalImage)

            except Exception as e:
                print("error:", e)
        
        cv2.imshow("Broadcast from camera", img)
        
        key = cv2.waitKey(3)
        if key == 27: # ESC
            break

except Exception as ex:
    print(ex)
finally:
    driver.close()
    cap.release()
    cv2.destroyAllWindows()
