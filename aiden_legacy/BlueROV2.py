# -*- coding: utf-8 -*-

from pymavlink import mavutil
import sys
import time

#establish the connection to the ROV
master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')
#verify the connection is good
master.wait_heartbeat()

#Pick guided mode so we can control the ROV using GPS location information
mode = 'GUIDED'

#Check to see if guided exists as a valid mode
if mode not in master.mode_mapping():
    print('Unknown mode: {}'.format(mode))
    print('Try:', list(master.mode_mapping.keys()))
    sys.exit(1)
    
#Get mode ID from preset list
mode_id = master.mode_mapping()[mode]
#Set new mode
master.mav.command_long_send(
    master.target_system, 
    master.target_component,
    mavutil.mavlink.MAV_CMD_DO_SET_MODE,
    0,
    1, mode_id, 0, 0, 0, 0, 0)

#wait for mode change rersponse from system
while True:
    ack_msg = master.recv_match(type='COMMAND_ACK', blocking=True)
    ack_msg = ack_msg.to_dict()
    
    if ack_msg['command'] != mavutil.mavlink.MAV_CMD_DO_SET_MODE:
        continue
    print(mavutil.mavlink.enums['MAV_RESULT'][ack_msg['result']].description)
    break

#Arm the ROV
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    1, 0, 0, 0, 0, 0, 0)
#Wait for the motors to be armed
master.motors_armed_wait()

#Make loops to send control messages and check location to desired location
time.sleep(5)
#

#Disarm the ROV when mission is complete
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    0, 0, 0, 0, 0, 0, 0)
#Wait for the motors to be disarmed
master.motors_disarmed_wait()