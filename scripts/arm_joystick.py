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

class ArmTeleop:
    def __init__(self):        
        ### Initialize the publisher for the joints        
        self.pub_q1 = rospy.Publisher('arm_teleop/joint1', Float64, queue_size=1)
        self.pub_q2 = rospy.Publisher('arm_teleop/joint2', Float64, queue_size=1)
        self.prospy.Publisher('arm_teleop/joint3', Float64, queue_size=1)
        self.pub_q4 = rospy.Publisher('arm_teleop/joint4', Float64, queue_size=1)
        self.pub_q_string = rospy.Publisher('inverse_kinematics/Q', String, queue_size=1)
        self.joint5 = rospy.Publisher('arm_teleop/joint5', Int32, queue_size=1) #rotation gripper 
        self.gripper = rospy.Publisher('arm_teleop/gripper', Float64, queue_size=1) #lineal 
        self.lineal = rospy.Publisher('arm_teleop/prism', Float64, queue_size=1) #lineal 
        self.camera = rospy.Publisher('arm_teleop/cam', Int32, queue_size=1) #lineal 
        self.image_sub = rospy.Subscriber("joy",Joy,self.on_joy)
        
        self.gripper_apertur = 60 #0 y 60
        self.values_map = {
            "x": 0,#.4
            "y": 0,#.9
            "z": 0,
            "phi": 0,#phi
            "rotation": 0,#rotation
            "camera": 0,#camera
        }

        self.l1 = 0
        self.l2 = 2.6
        self.l3 = 2.6
        self.l4 = .9

        self.limits_map = {
            "q1":(-90,90),
            "q2":(0,161),
            "q3":(-165.4,0),
            "q4":(-135,90),
            "rotation":(-90,90),
            "camera":(100,140)
        }

        self.angles_map={
            "q1":0,
            "q2":161,
            "q3":-165.4,#
            "q4":0
        }
        self.limit_z = -4.2
        self.limit_chassis = 1.1

    def ikine_brazo(self, xm, ym, zm, phi_int):        
        if (xm != 0 or ym != 0 or zm != 0):
            if(xm == 0):
                if(ym>0):
                    xm = ym
                    Q1 = math.pi/2
                elif ym<0:
                    xm = ym
                    Q1 = -math.pi/2
                elif ym == 0:
                    Q1 = 0
            elif (xm < 0):
                if (ym == 0):
                    Q1 = 0
                elif ym<0:
                    Q1 = numpy.real(math.atan2(xm, ym))#real
                else:
                    Q1 = numpy.real(math.atan2(-xm,-ym))#real
            else:
                Q1 = numpy.real(math.atan2(ym,xm))#real
        #Para q1
        q1=self.angles_map["q1"]
        #Para q2      
        hip=math.sqrt(xm**2+(zm-self.l1)**2)
        phi = math.atan2(zm-self.l1, xm)
        beta=cmath.acos((-self.l3**2+self.l2**2+hip**2)/(2*self.l2*hip))
        Q2=numpy.real(phi+beta)        
        q2=numpy.rad2deg(Q2) 
        q2=self.qlimit(self.limits_map["q2"],q2)
        #Para q3
        gamma=cmath.acos((self.l2**2+self.l3**2-hip**2)/(2*self.l2*self.l3))        
        Q3=numpy.real(gamma-math.pi)        
        q3=numpy.rad2deg(Q3)
        q3=self.qlimit(self.limits_map["q3"],q3)
        q4 = phi_int - q2 -q3  
        q4=self.qlimit(self.limits_map["q4"],q4)    
        self.values_map["phi"] = q4+q3+q2        
        
        acum = math.radians(q2)
        x2 = self.l2*math.cos(acum) 
        y2 = self.l2*math.sin(acum)        
        acum+=math.radians(q3)
        x3 = x2+self.l3*math.cos(acum)
        y3 = y2+self.l3*math.sin(acum)
        acum+=math.radians(q4)
        x4 = x3+self.l4*math.cos(acum)
        y4 = y3+self.l4*math.sin(acum)
        
        self.values_map["x"] = x3
        self.values_map["y"] = y3

        self.angles_map["q2"] = q2
        self.angles_map["q3"] = q3
        self.angles_map["q4"] = q4
        self.publish_angles()
        

    def publish_angles(self):
        q1 = self.angles_map["q1"]
        q2 = self.angles_map["q2"]
        q3 = self.angles_map["q3"]
        q4 = self.angles_map["q4"]

        #txt = str(q1)+" "+str(q2)+" "+str(q3)+" "+str(q4)
        txt = str(self.values_map["x"]) + " " + str(self.values_map["y"]) + " " + str(self.values_map["z"])
        rospy.loginfo(txt)
        """self.pub_q1.publish(q1)
        self.pub_q2.publish(q2)
        self.pub_q3.publish(q3)
        self.pub_q4.publish(q4)
        self.pub_q_string.publish(txt)"""

    def qlimit(self, l, val):
        if (val < l[0]):
            return l[0]
        if (val > l[1]):
            return l[1]
        return val   

    def my_map(self,in_min, in_max, out_min, out_max, x):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def on_joy(self, data):
        if data.axes[1] != 0:
            up = data.axes[1] > 0
            if up:
                self.values_map["z"] += 1
            else:
                self.values_map["z"] -= 1
        self.ikine_brazo(self.values_map["x"], self.values_map["y"], self.values_map["z"], self.values_map["phi"])

        if data.buttons[7] != 0:
            x = 0
            y = 0
            z = 3.677
            phi = 0
            self.values_map["joint1"] = x
            self.values_map["joint2"] = y
            self.values_map["joint3"] = z
            self.values_map["joint4"] = phi
            self.ikine_brazo(self.values_map["joint1"], self.values_map["joint2"], self.values_map["joint3"], self.values_map["joint4"])
        elif data.buttons[8] != 0:
            x = .134
            y =  0
            z =  .75#.647 
            phi = 0
            self.values_map["joint1"] = x
            self.values_map["joint2"] = y
            self.values_map["joint3"] = z
            self.values_map["joint4"] = phi
            self.ikine_brazo(self.values_map["joint1"], self.values_map["joint2"], self.values_map["joint3"], self.values_map["joint4"])




if __name__ == '__main__':
    try:
        rospy.init_node("arm_joystick")
        sar_base_arm_test = ArmTeleop()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
