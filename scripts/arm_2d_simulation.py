#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64

import numpy as np
import math
import matplotlib.pyplot as plt
import time

x0 = 0
y0 = 0
l1 = .21
l2 = .21

q = {
    'q1':0, 
    'q2':0,
    'q3':0,
    'q4':0
}
        
def plotAgain():
    #rospy.loginfo()
    x1 = l1*math.cos(q["q1"])
    y1 = l1*math.sin(q["q1"])    
    
    x2 = x1*l2*math.cos(q["q2"]) 
    y2 = y1*l2*math.sin(q["q2"])
    
    plt.clf()
    plt.plot([x0,x1], [y0,y1])
    plt.plot([x1,x2], [y1,y2])
    plt.draw()
    plt.pause(0.00000000001)

def doQ1(msg):
    q["q1"] = msg.data
    plotAgain()
        
def doQ2(msg):
    q["q2"] = msg.data

rospy.init_node('arm_inverse_kinematics')
sub = rospy.Subscriber ('/inverse_kinematics/q1', Float64, doQ1)
sub = rospy.Subscriber ('/inverse_kinematics/q2', Float64, doQ2)
plt.show()
rospy.spin()