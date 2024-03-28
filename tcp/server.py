from time import sleep
import zmq
import json
from datetime import datetime

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:50165")

import re

def printData(message):
    sleep(1)
    print(message)
    return


while True:
    #  Wait for next request from client
    message = socket.recv()
    message = str(message)

    if "Angle" in message:
        test = 1.05
        socket.send(str(test).encode())
        printData(str(test))
    elif "XY" in message:
        socket.send(b"20,30")
        printData(str(message))
    else:
        #  Send reply back to client
        socket.send(b"error")

    sleep(5)
    print(datetime.now(),message)

     
