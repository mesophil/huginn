from ultralytics import YOLO
import cv2
import math
import logging
import numpy as np
import time

from config import confThresh, xDim, yDim, classNames, modelPath

from picamera2 import Picamera2

from detect_functions import findAngle, findAngleWithDepth, calculateAngle, depthMap

logging.basicConfig(filename='my.log', format='%(asctime)s : %(levelname)s : %(message)s', encoding='utf-8', level=logging.DEBUG)

def main():
    logging.info('Loading cameras')

    cam0 = Picamera2(0)
    cam1 = Picamera2(1)
    
    cam0.start()
    cam1.start()

    model = YOLO(modelPath)

    i = 0
    
    while i < 3:
        time.sleep(1)
        img0 = cam0.capture_array("main")
        time.sleep(1)
        img1 = cam1.capture_array("main")
        
        # cv2.imwrite(f'~/Desktop/c{i}_0.png',img0)
        # cv2.imwrite(f'~/Desktop/c{i}_1.png', img1)

        results = model(img0, stream=True)

        for r in results:
            boxes = r.boxes

            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                confidence = math.ceil((box.conf[0]*100))/100
                cls = int(box.cls[0])

        i += 1
        
    cam0.stop()
    cam1.stop()


def readInputs():
    # somehow get the inputs from the flight controller
    mode = 'far'
    needImage = True
    
    return mode, needImage

def sendOutputs(angle, depth):
    # somehow send the outputs to the flight controller
    pass

if __name__ == "__main__":
    main()