# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 11:17:01 2023

@author: ahuss
"""

from pymavlink import mavutil

master = mavutil.mavlink_connection('udpout:127.0.0.1:14551', source_system=1)
master.mav.statustext_send(mavutil.mavlink.MAV_SEVERITY_NOTICE,"QGC will read this".encode())
