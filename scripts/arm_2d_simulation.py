#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64

import numpy as np
import math
import matplotlib.pyplot as plt
import time

x0 = 0
y0 = 0
l1 = 0
l2 = 2.6
l3 = 2.6
l4 = .9

q = {
    'q1':90, 
    'q2':0,
    'q3':0,
    'q4':0
}
        
def plotAgain():
    print(q["q1"],q["q2"],q["q3"],q["q4"])
    #x1 = l1*math.cos(math.radians(q["q1"]))
    #y1 = l1*math.sin(math.radians(q["q1"]))    
    #plt.show()
    acum = math.radians(q["q2"])
    x2 = l2*math.cos(acum) 
    y2 = l2*math.sin(acum)

    acum+=math.radians(q["q3"])
    x3 = x2+l3*math.cos(acum)
    y3 = y2+l3*math.sin(acum)

    acum+=math.radians(q["q4"])
    x4 = x3+l4*math.cos(acum) 
    y4 = y3+l4*math.sin(acum)
    #print(x4,y4)
    plt.clf()
    #plt.plot([x0,x1], [y0,y1])   
    plt.plot([x0,x2], [y0,y2])
    plt.plot([x2,x3], [y2,y3])
    plt.plot([x3,x4], [y3,y4])
    plt.plot([-7,7], [-4.2,-4.2])
    plt.axis([-7.0,7.0, -7.0,7.0])
    plt.grid()
    plt.draw()
    plt.pause(0.00000000001)
    #rospy.loginfo()

def doQ1(msg):
    q["q1"] = msg.data    
        
def doQ2(msg):
    q["q2"] = msg.data

def doQ3(msg):
    q["q3"] = msg.data

def doQ4(msg):
    q["q4"] = msg.data
    plotAgain()


rospy.init_node('arm_inverse_kinematics')
sub = rospy.Subscriber ('/inverse_kinematics/q1', Float64, doQ1)
sub = rospy.Subscriber ('/inverse_kinematics/q2', Float64, doQ2)
sub = rospy.Subscriber ('/inverse_kinematics/q3', Float64, doQ3)
sub = rospy.Subscriber ('/inverse_kinematics/q4', Float64, doQ4)
plt.show()
#plotAgain()
rospy.spin()