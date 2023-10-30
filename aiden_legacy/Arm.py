# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 14:58:42 2023

@author: ahuss
"""

from pymavlink import mavutil
import time

master = mavutil.mavlink_connection('udpin:127.0.0.1:14551')
master.wait_heartbeat()
#Arm command
master.arducopter_arm()
master.arducopter_arm()
#master.mav.command_long_send(
#    master.target_system,
#    master.target_component,
#    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
#    0,
#    1, 0, 0, 0, 0, 0, 0)
print("Waiting for the vehicle to arm")
master.motors_armed_wait()
print('Armed!')

time.sleep(5)

#Disarm command
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    0, 0, 0, 0, 0, 0, 0)
master.motors_disarmed_wait()