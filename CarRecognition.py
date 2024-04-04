from yolo import yolo_car_checker
import numpy as np
import cv2

def getCarsImages(size = 1024):
    cap = cv2.VideoCapture('https://docs.google.com/uc?export=download&confirm=&id=1pz68D1Gsx80MoPg-_q-IbEdESEmyVLm-')
    # while True:
    # yolo work
    # cv_img, car_detected_cv = yolo_car_checker(cap)
    while True:
        _, frame = cap.read()
    # Combine detected car array
        arraycar, cv_img = yolo_car_checker(frame)
        car_detected_cv = arraycar[1]
        buf = []
        for i in car_detected_cv:
            buf.append(cv2.resize(i, (64,64)))
        union = np.hstack(buf)
        # Show result
        cv2.imshow('1', cv2.resize(cv_img, (1024, 576)))
        cv2.imshow('2', union)
        if cv2.waitKey(1) == ord('q'):
            break
        # ret, cv_img = frame.read()

getCarsImages()