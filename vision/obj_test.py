from ultralytics import YOLO
import cv2
import math
import logging
import numpy as np
import time

from config import confThresh, classNames, modelPath

xDim = 1280
yDim = 720


logging.basicConfig(filename='my.log', format='%(asctime)s : %(levelname)s : %(message)s', encoding='utf-8', level=logging.DEBUG)

def main():
    logging.info('Loading cameras')

    cam0 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam0.set(3, xDim)
    cam0.set(4, yDim)

    logging.info('Loading model')

    model = YOLO(modelPath)

    logging.info('Begin reading')

    while True:
        time.sleep(0.2)
        _, img0 = cam0.read()

        results = model(img0, stream=True)

        for r in results:
            boxes = r.boxes

            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values
                cv2.rectangle(img0, (x1, y1), (x2, y2), (255, 0, 255), 3)

                confidence = math.ceil((box.conf[0]*100))/100
                cls = int(box.cls[0])

                mid = (np.mean([x1, x2]), np.mean([y1, y2]))
                theta = calculateAngle(mid[0], mid[1])
                    
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 0.5
                color = (255, 0, 0)
                thickness = 2
                
                cv2.putText(img0, f"{classNames[cls]}; Conf {confidence}; Angle {theta:.2f}; Midpoint {mid[0]}, {mid[1]}", org, font, fontScale, color, thickness)

        cv2.imshow('Cam', img0)

        if cv2.waitKey(1) == ord('q'):
            break

    cam0.release()
    cv2.destroyAllWindows()

def calculateAngle(x, y):
    adjustedMid = (x - xDim//2, y - yDim//2)

    angle = math.atan2(adjustedMid[1], adjustedMid[0])
    angleDeg = math.degrees(angle)

    return (angleDeg + 90 + 360) % 360

def depthMap(img0, img1):
    stereo = cv2.StereoBM.create(numDisparities=16, blockSize=15) # optimize this  (specifically the hyperparameters)
    # https://wiki.ros.org/stereo_image_proc/Tutorials/ChoosingGoodStereoParameters
    disparity = stereo.compute(img0, img1)

    return disparity

if __name__ == "__main__":
    main()