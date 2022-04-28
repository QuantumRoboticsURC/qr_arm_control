#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import String

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
    qs = msg.data.split(" ")
    q["q1"] = float(qs[0])
    q["q2"] = float(qs[1])
    q["q3"] = float(qs[2])
    q["q4"] = float(qs[3])    
    plotAgain()


rospy.init_node('arm_inverse_kinematics')
sub = rospy.Subscriber ('/inverse_kinematics/Q', String, doQ1)
plt.show()
#plotAgain()
rospy.spin()