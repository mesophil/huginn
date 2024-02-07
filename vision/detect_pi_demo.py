from ultralytics import YOLO
import cv2
import math
import logging
import numpy as np
import time

from PIL import Image

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

    logging.info('Loading model')

    model = YOLO(modelPath)
    
    logging.info('Begin capture!')
    
    for _ in range(10):
        time.sleep(1)
        #img0 = cam0.capture_array("main")
        img0 = cam0.capture_image("main")
        time.sleep(1)
        img1 = cam1.capture_image("main")
        
        # cv2.imwrite(f'~/Desktop/c{i}_0.png',img0)
        # cv2.imwrite(f'~/Desktop/c{i}_1.png', img1)

        results = model(img0) #, stream=True)
        
        img0 = cv2.cvtColor(np.array(img0), cv2.COLOR_BGR2RGB)
        img1 = cv2.cvtColor(np.array(img1), cv2.COLOR_BGR2RGB)
        
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


if __name__ == "__main__":
    main()