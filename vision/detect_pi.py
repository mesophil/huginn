from ultralytics import YOLO
import cv2
import math
import logging
import numpy as np

from config import confThresh, xDim, yDim, classNames, modelPath


logging.basicConfig(filename='my.log', format='%(asctime)s : %(levelname)s : %(message)s', encoding='utf-8', level=logging.DEBUG)

def main():
    logging.info('Loading cameras')

    cam0 = cv2.VideoCapture('/dev/video0')
    cam0.set(3, xDim)
    cam0.set(4, yDim)

    # cam1 = cv2.VideoCapture('/dev/video1')
    # cam1.set(3, xDim)
    # cam1.set(4, yDim)

    # model = YOLO(modelPath)

    i = 0
    
    while i < 3:
        _, img0 = cam0.read()
        
        cv2.imwrite(f'~/Desktop/c{i}.png',img0)

        # results = model(img0, stream=True)

        # for r in results:
        #     boxes = r.boxes

        #     for box in boxes:
        #         x1, y1, x2, y2 = box.xyxy[0]
        #         x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

        #         confidence = math.ceil((box.conf[0]*100))/100
        #         cls = int(box.cls[0])

        i += 1
    
    cv2.destroyAllWindows()


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