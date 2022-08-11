#!/usr/bin/env python
import rospy
import rospkg
from geometry_msgs.msg import Twist
from Tkinter import *
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

values_map={   
    "x": .134,   
    "y": 0,      
    "z": .75,
    "joint4": 0,
    "joint5": 0,
    "joint8": 140
}


buttons, axes = [0,0,0,0,0,0,0], [0,0]
def to_string():
    return str(values_map["x"])

def on_joy(data):
    global buttons, axes
    buttons = data.buttons [:]
    axes = data.axes [:]    
    print(axes[0])
    
rospy.init_node("arm_joystick")
rospy.Subscriber("joy",Joy,on_joy)
pub = rospy.Publisher('goal', String, queue_size=1)
rate = rospy.Rate(20)
while True:
    changed = False
    if axes[0] > 0:
        changed = True
        values_map["x"]+=.5
    elif axes[0] < 0:
        changed = True
        values_map["x"]-=.5
    else:
        changed = False
        
    if changed:
        pub.publish(to_string())
    rate.sleep()


rospy.spin()