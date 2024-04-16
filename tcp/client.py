import zmq
from time import sleep
context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:50165")

sleep(2)
#  Do 10 requests, waiting each time for a response
#for request in range(10):
print("Sending request %s …" % 1)
socket.send(b"1Hello")
sleep(0.01)
#  Get the reply.
message = socket.recv()
print("Received reply %s [ %s ]" % (1, message))
                            
