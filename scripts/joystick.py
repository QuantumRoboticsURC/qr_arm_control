#!/usr/bin/env python
import rospy
import rospkg
from geometry_msgs.msg import Twist
#from Tkinter import *
from PIL import ImageTk, Image
import time
import os
import serial
import struct
import threading
from std_msgs.msg import *
from geometry_msgs.msg import Twist
import math
import numpy
import cmath
from sensor_msgs.msg import Joy
import sys



values_map={   
    "x": 0,
    "y": 0,      
    "z": 0,
    "phi": 0,
    "joint5":0,
    "joint8":0
}

def change_value(arr, index, val):
    if axes[index] > 0.3:
        return val
    elif axes[index] < -0.3:
        return val*-1
    else:
        return 0
def change_value2(arr, indexb,indexa, val):
    if buttons[indexb] == 1.0:
        return val
    elif axes[indexa] == -1.0:
        return val*-1
    else:
        return 0


def triggers(val):
    global axes
    if axes[2] < 0:
        return val*-1
    elif axes[5] < 0:
        return val
    return 0
    
        
buttons, axes = [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]
def to_string():
    print(values_map)
    return str(values_map["x"]) + " " + str(values_map["y"]) + \
    " " + str(values_map["z"]) + " " + str(values_map["phi"]) +" "+str(values_map["joint5"])+" "+str(values_map["joint8"])

def on_joy(data):
    global buttons, axes
    buttons = list(data.buttons [:])
    axes = list(data.axes [:])
   
    if buttons[0] == 1:
        pub_predefined.publish("FLOOR")
    elif buttons[1] == 1:
        pub_predefined.publish("HOME")
    elif buttons[2] == 1:
        pub_predefined.publish("INTERMEDIATE")

def servo_mover(b):
    if axes[b] == 1.0:
        return 1.0
    elif axes[b]==-1:
        return -1.0
    else:
        return 0

def pause():
    global buttons
    if(buttons[9]==1):
        sys.exit()

rospy.init_node("arm_joystick")
rospy.Subscriber("joy",Joy,on_joy)
pub = rospy.Publisher('goal', String, queue_size=1)
pub_predefined = rospy.Publisher('predefined', String, queue_size=1)
pub_prism = rospy.Publisher('arm_teleop/prism', Float64, queue_size=1)

last_prism = 0

rate = rospy.Rate(20)

while not rospy.is_shutdown():
    pause()
    changed = False
    values_map["x"] = change_value(axes,2,.02)*-1
    values_map["y"] = change_value(axes, 0, .22)*-1
    values_map["z"] = change_value(axes, 1, .05)
    values_map["phi"] = change_value(axes, 5, .8)
    #values_map["rotation"] = change_value2(axes, 4,3, .05)
    values_map["joint5"]=servo_mover(6)
    values_map["joint8"]=servo_mover(7)
    if axes[-1] != last_prism:
        pub_prism.publish(axes[-1])
        last_prism = axes[-1]

    pub.publish(to_string())
    rate.sleep()