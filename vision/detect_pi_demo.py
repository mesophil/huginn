from ultralytics import YOLO
import cv2
import math
import logging
import numpy as np
import time

from config import confThresh, xDim, yDim, classNames, modelPath

from picamera2 import Picamera2

logging.basicConfig(filename='my.log', format='%(asctime)s : %(levelname)s : %(message)s', encoding='utf-8', level=logging.DEBUG)

def main():
    logging.info('Loading cameras')

    cam0 = Picamera2(0)
    cam1 = Picamera2(1)
    
    cam0.start()
    cam1.start()

    logging.info('Loading model')

    model = YOLO(modelPath)
    
    logging.info('Begin capture!')
    
    for _ in range(10):
        time.sleep(1)
        img0 = cam0.capture_array("main")
        time.sleep(1)
        img1 = cam1.capture_array("main")
        
        # cv2.imwrite(f'~/Desktop/c{i}_0.png',img0)
        # cv2.imwrite(f'~/Desktop/c{i}_1.png', img1)

        results = model(img0) #, stream=True)
        
        for r in results:
            boxes = r.boxes

            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                confidence = math.ceil((box.conf[0]*100))/100
                cls = int(box.cls[0])
                
                if classNames[cls] == 'keyboard':
                    mid = (np.mean([x1, x2]), np.mean([y1, y2]))
                    theta = calculateAngle(mid[0], mid[1])
                else:
                    mid = theta = 0
                    
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2
                
                cv2.putText(img0, " ".join([classNames[cls], str(confidence), str(theta)], org, font, fontScale, color, thickness))
                
        cv2.imshow('Cam', img0)
        
    cam0.stop()
    cam1.stop()


def readInputs():
    # somehow get the inputs from the flight controller
    mode = 'far'
    needImage = True
    
    return mode, needImage

def calculateAngle(x, y):
    adjustedMid = (x - xDim//2, y - yDim//2)

    angle = math.atan2(adjustedMid[1], adjustedMid[0])
    angleDeg = math.degrees(angle)

    return (angleDeg + 360) % 360

def depthMap(img0, img1):
    stereo = cv2.StereoBM.create(numDisparities=16, blockSize=15) # optimize this  (specifically the hyperparameters)
    # https://wiki.ros.org/stereo_image_proc/Tutorials/ChoosingGoodStereoParameters
    disparity = stereo.compute(img0, img1)

    return disparity

def sendOutputs(angle, depth):
    # somehow send the outputs to the flight controller
    pass

if __name__ == "__main__":
    main()