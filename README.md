# huginn
## ECE 494/495 Capstone Project for Dr. Myatt

Authors:
- Nico Schiavone
- Yeh-In Kang
- Hariharan Krishnan

## Why huginn and not a prebuilt object detection camera?
Object detection cameras start at ~[US$300](https://www.alibaba.com/product-detail/Object-recognition-data-management-AI-tracking_1600119050822.html "One example we found"), while our system can be assembled for ~CA$160 ($100 raspberry pi, and two $30 pi cameras).

## Docker Image used to run ROS on Rasberry Pi 5
https://hub.docker.com/repository/docker/hariharankrishnan/capstone-ubuntu20/general
run with: sudo docker run --name capstone --network host -p 50165:50165/tcp --privileged -ti --rm -v ~/Docker_Share:/data -v /opt/vc:/opt/vc -v /dev/:/dev/ -v /run/udev:/run/udev -v /run/dbus/:/run/dbus myubuntu2 /bin/bash
