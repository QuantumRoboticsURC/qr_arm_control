#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
import math
import numpy

        
values_map = {}
def ikine_brazo(xm, ym, zm, phi = 0):
    l1 = 0.11329
    l2 = .21
    l3 = .21
    #Para q1
    Q1 = 50
    if(xm == 0):
        if(ym>0):
            xm = ym
            Q1 = math.pi/2
        elif ym<0:
            xm = ym
            Q1 = -math.pi/2
    elif (xm < 0):
        if (ym == 0):
            Q1 = math.pi
            xm = -xm
        elif ym<0:
            Q1 = math.atan2(xm, ym)
        else:
            Q1 = math.atan2(-xm,-ym)
    else:
        Q1 = math.atan2(ym,xm)
    q1=numpy.rad2deg(Q1)
    #Para q2     
    hip=math.sqrt(xm**2+(zm-l1)**2)
    delta=math.atan2(zm-l1,xm)
    beta=math.acos((-l3**2+l2**2+hip**2)/(2*l2*hip))
    Q2=delta+beta
    q2=numpy.rad2deg(Q2) 
    #Para q3
    gamma=math.acos((l2**2+l3**2-hip**2)/(2*l2*l3))
    Q3=gamma-math.pi
    q3=numpy.rad2deg(Q3)
    q4 = phi - q2 -q3
    pub_q1.publish(q1)
    pub_q2.publish(q2)
    pub_q3.publish(q3)
    pub_q4.publish(q4)
    txt = ""
    for i in [q1,q2,q3,q4]:
        txt+=str(q1)+" "    
    rospy.loginfo(txt)

def doX(msg):
    values_map["x"] = msg.data
    ikine_brazo(values_map["x"], values_map["y"], values_map["z"], values_map["phi"])

def doY(msg):
    values_map["y"] = msg.data
    ikine_brazo(values_map["x"], values_map["y"], values_map["z"], values_map["phi"])

def doZ(msg):
    values_map["z"] = msg.data
    ikine_brazo(values_map["x"], values_map["y"], values_map["z"], values_map["phi"])

def doPhi(msg):
    values_map["phi"] = msg.data
    ikine_brazo(values_map["x"], values_map["y"], values_map["z"], values_map["phi"])

#ikine_brazo(0.25,0,0.2)

rospy.init_node('arm_inverse_kinematics')
pub_q1 = rospy.Publisher('inverse_kinematics/q1', Float64, queue_size=1)
pub_q2 = rospy.Publisher('inverse_kinematics/q2', Float64, queue_size=1)
pub_q3 = rospy.Publisher('inverse_kinematics/q3', Float64, queue_size=1)
pub_q4 = rospy.Publisher('inverse_kinematics/q4', Float64, queue_size=1)


values_map = {
    "x": 0,
    "y": 0,
    "z": 0,
    "phi": 0,            
}

sub = rospy.Subscriber ('/arm_teleop/x', Float64, doX)
sub = rospy.Subscriber ('/arm_teleop/y', Float64, doY)
sub = rospy.Subscriber ('/arm_teleop/z', Float64, doZ)
sub = rospy.Subscriber ('/arm_teleop/phi', Float64, doPhi)

rospy.spin()