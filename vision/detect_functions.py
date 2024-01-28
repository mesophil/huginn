from ultralytics import YOLO
import cv2
import math
import logging
import numpy as np
import time
from typing import List

from config import confThresh, xDim, yDim, classNames, modelPath

from picamera2 import Picamera2



logging.basicConfig(filename='detect.log', format='%(asctime)s : %(levelname)s : %(message)s', encoding='utf-8', level=logging.DEBUG)

# load cams
cam0 = Picamera2(0)
cam1 = Picamera2(1)

# load model
model = YOLO(modelPath)

def findAngle() -> float:
    cam0.start()
    
    time.sleep(1)
    _, img0 = cam0.read()
    
    results = model(img0, stream=True)
    
    for r in results:
        boxes = r.boxes

        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            confidence = math.ceil((box.conf[0]*100))/100
            cls = int(box.cls[0])

            if classNames[cls] == 'keyboard' and confidence >= confThresh:
                mid = (np.mean([x1, x2]), np.mean([y1, y2]))

                theta = calculateAngle(mid[0], mid[1])
                    
                logging.info(f"Theta: {theta}")

                return theta
            
            
def findAngleWithDepth() -> tuple:
    cam0.start()
    cam1.start()
    
    time.sleep(1)
    _, img0 = cam0.read()
    time.sleep(1)
    _, img1 = cam1.read()
    
    results = model(img0, stream=True)
    
    depthMapping = depthMap(img0, img1)
    
    for r in results:
        boxes = r.boxes

        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            confidence = math.ceil((box.conf[0]*100))/100
            cls = int(box.cls[0])

            if classNames[cls] == 'keyboard' and confidence >= confThresh:
                mid = (np.mean([x1, x2]), np.mean([y1, y2]))

                theta = calculateAngle(mid[0], mid[1])
                depth = depthMapping[mid[0], mid[1]]
                    
                logging.info(f"Theta: {theta}")

                return (theta, depth)

def calculateAngle(x : float, y : float) -> float:
    adjustedMid = (x - xDim//2, y - yDim//2)

    angle = math.atan2(adjustedMid[1], adjustedMid[0])
    angleDeg = math.degrees(angle)

    return (angleDeg + 360) % 360

def depthMap(img0 : list, img1 : list) -> List[List[float]]:
    stereo = cv2.StereoBM.create(numDisparities=16, blockSize=15) # optimize this  (specifically the hyperparameters)
    # https://wiki.ros.org/stereo_image_proc/Tutorials/ChoosingGoodStereoParameters
    disparity = stereo.compute(img0, img1)

    return disparity

if __name__ == "__main__":
    logging.info("Why did you call me directly?")
    pass