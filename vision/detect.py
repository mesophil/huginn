from ultralytics import YOLO
import cv2
import math
import logging
import numpy as np

from config import confThresh, xDim, yDim

def main():
    logging.info('Loading cameras')

    cam0 = cv2.VideoCapture(0)
    cam0.set(3, xDim)
    cam0.set(4, yDim)

    cam1 = cv2.VideoCapture(1)
    cam1.set(3, xDim)
    cam1.set(4, yDim)

    logging.info('Loading model')

    model = YOLO("yolo_weights/yolov8s.pt")

    classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                  "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                  "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                  "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                  "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                  "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                  "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                  "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                  "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                  "teddy bear", "hair drier", "toothbrush"]

    logging.info('Begin reading')

    # somehow get this as input
    mode = 'far'
    needImage = True


    while needImage and mode != 'return':
        _, img0 = cam0.read()
        _, img1 =cam1.read()

        results = model(img0, stream=True)

        if mode == 'close':
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
                    depth = -1

                    if mode == 'close':
                        depth = depthMapping[mid[0], mid[1]]

                    # somehow output theta (and depth if mode is close) to the controller and update parameters mode and needImage
                    mode = 'return'
                    needImage = False


        if cv2.waitKey(1) == ord('q'):
            break

    cam0.release()
    cv2.destroyAllWindows()

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

if __name__ == "__main__":
    logging.basicConfig(filename='my.log', format='%(asctime)s : %(levelname)s : %(message)s', encoding='utf-8', level=logging.DEBUG)
    main()