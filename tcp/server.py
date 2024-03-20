from time import sleep
import zmq
import json
from datetime import datetime

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:50165")

import re

def printData():
    sleep(1)
    print("Hello")
    return


while True:
     #  Wait for next request from client
     message = socket.recv()
     message = str(message)

     if "Hello" in message:
        printData()

     sleep(5)
     print(datetime.now(),message)

     #  Send reply back to client
     socket.send(b"Data Recieved")
