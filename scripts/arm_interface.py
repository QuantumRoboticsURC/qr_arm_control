#!/usr/bin/env python
import rospy
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

class ArmTeleop:
    def __init__(self):        
        ### Initialize the publisher for the joints        
        self.pub_q1 = rospy.Publisher('inverse_kinematics/q1', Float64, queue_size=1)
        self.pub_q2 = rospy.Publisher('inverse_kinematics/q2', Float64, queue_size=1)
        self.pub_q3 = rospy.Publisher('inverse_kinematics/q3', Float64, queue_size=1)
        self.pub_q4 = rospy.Publisher('inverse_kinematics/q4', Float64, queue_size=1)
        self.pub_q_string = rospy.Publisher('inverse_kinematics/Q', String, queue_size=1)
        self.joint5 = rospy.Publisher('arm_teleop/rotacion_gripper', Int32, queue_size=1)
        self.gripper = rospy.Publisher('arm_teleop/apertura_gripper', Int32, queue_size=1)
        self.gripper_apertur = 100
        self.joint5_position = 321        

        self.values_map = {
            "joint1": 5.2,#.4
            "joint2": 0,#.9
            "joint3": 0,
            "joint4": 0,
            "joint5": 0,
            "joint6": 0
        }

        self.l1 = 0
        self.l2 = 2.6
        self.l3 = 2.6
        self.l4 = .9

        self.limits_map = {
            "q1":(-90,90),
            "q2":(0,170),
            "q3":(-135,90),
            "q4":(-90,90)
        }

        self.angles_map={
            "q1":0,
            "q2":0,
            "q3":0,#
            "q4":0
        }
        self.limit_z = -3
        self.limit_chassis = 1.1
        #11cm del chasis
        
        ### Initialize graph interface
        self.ArmControlWindow = Tk()
        self.ArmControlWindow.title("Arm Teleop")
        self.ArmControlWindow.resizable(True, True)
        self.ArmControlWindow.config(cursor="arrow")
        self.root = Frame(self.ArmControlWindow).grid()
        ##### Grpah Interface #####
        #980px width
        #each width 1 of label is 13px
        self.title = Label(self.root, font=("Consolas", 18), width=72, bg="white", bd=0, justify=CENTER)
        self.title.config(text="qr_arm_control")
        self.title.grid(row=0, column=0, columnspan=4, sticky="nsew")
       ##### Section1: When you hold down the button of a joint, the joint moves with the velocity defined in the slider
        self.labelTitleS1 = Label(self.root, font=("Consolas", 12), width=36, bg="white", bd=0, justify=CENTER)
        self.labelTitleS1.config(text="Section 1: Move each joint")
        self.labelTitleS1.grid(row=1, column=0, columnspan=4, sticky="nsew")
        self.labelS1 = Label(self.root, font=("Consolas", 10), width=36, bg="white", bd=0, justify=CENTER)
        self.labelS1.config(text="\nHold down a button to move a joint\nthe joint moves with the velocity defined in the sliders\n")
        self.labelS1.grid(row=2, column=0, columnspan=4, sticky="nsew")
        self.labelS1Headers = Label(self.root, font=("Consolas", 8), width=36, bg="white", bd=0, justify=RIGHT, anchor=E)
        self.labelS1Headers.config(text="Joint        |     Velocity      |    Button Clockwise   |Button Counterclockwise")
        #self.labelS1Headers.grid(row=3, column=0, columnspan=4, sticky="nsew")                
        self.buttonsSection1(1, 4, 0, "Position X")
        self.S1buttonj1w.bind("<ButtonPress-1>", lambda event: self.pressed(float(self.S1velj1.get()), 1))        
        self.S1buttonj1c.bind("<ButtonPress-1>", lambda event: self.pressed(float("-"+self.S1velj1.get()), 1))
        self.S1buttonj1w.bind("<ButtonRelease-1>", lambda event: self.unpressed())
        self.S1buttonj1c.bind("<ButtonRelease-1>", lambda event: self.unpressed())

        self.buttonsSection1(2, 5, 0, "Position Y")
        self.S1buttonj2c.bind("<ButtonPress-1>", lambda event: self.pressed(float("-"+self.S1velj2.get()), 2),-1)
        self.S1buttonj2w.bind("<ButtonPress-1>", lambda event: self.pressed(float(self.S1velj2.get()), 2))
        self.S1buttonj2w.bind("<ButtonRelease-1>", lambda event: self.unpressed())        
        self.S1buttonj2c.bind("<ButtonRelease-1>", lambda event: self.unpressed())

        self.buttonsSection1(3, 6, 0, "Position Z")
        self.S1buttonj3c.bind("<ButtonPress-1>", lambda event: self.pressed(float("-"+self.S1velj3.get()) , 3))
        self.S1buttonj3w.bind("<ButtonPress-1>", lambda event: self.pressed(float(self.S1velj3.get()), 3))
        self.S1buttonj3w.bind("<ButtonRelease-1>", lambda event: self.unpressed())        
        self.S1buttonj3c.bind("<ButtonRelease-1>", lambda event: self.unpressed())

        self.buttonsSection1(4, 7, 0,"Phi", "5")
        self.S1buttonj4c.bind("<ButtonPress-1>", lambda event: self.pressed(float("-"+self.S1velj4.get()) , 4),-1)
        self.S1buttonj4w.bind("<ButtonPress-1>", lambda event: self.pressed(float(self.S1velj4.get()) , 4))
        self.S1buttonj4w.bind("<ButtonRelease-1>", lambda event: self.unpressed())        
        self.S1buttonj4c.bind("<ButtonRelease-1>", lambda event: self.unpressed())

        self.buttonsSection1(5, 8, 0,"Rotacion del gripper")
        self.S1buttonj5w.bind("<ButtonPress-1>", lambda event: self.pressed(float(self.S1velj5.get()) , 5))
        self.S1buttonj5w.bind("<ButtonRelease-1>", lambda event: self.unpressed())
        self.S1buttonj5c.bind("<ButtonPress-1>", lambda event: self.pressed(float("-"+self.S1velj5.get()) , 5),-1)
        self.S1buttonj5c.bind("<ButtonRelease-1>", lambda event: self.unpressed())

        self.buttonsSection1(6, 9, 0,"Abrir/cerrar")
        self.S1buttonj6c.bind("<ButtonPress-1>", lambda event: self.pressed(float("-"+self.S1velj4.get()) , 6),-1)
        self.S1buttonj6w.bind("<ButtonPress-1>", lambda event: self.pressed(float(self.S1velj6.get()) , 6))
        self.S1buttonj6w.bind("<ButtonRelease-1>", lambda event: self.unpressed())        
        self.S1buttonj6c.bind("<ButtonRelease-1>", lambda event: self.unpressed())
        
                

        self.labelInfo = Label(self.root, font=("Consolas", 10), width=36, bg="white", bd=0, justify=LEFT)
        self.labelInfo.config(text=self.getTxt())
        self.labelInfo.grid(row=10, column=0, columnspan=4, sticky="nsew")

        photo = ImageTk.PhotoImage(Image.open("/home/arihc/catkin_ws/src/qr_arm_control/scripts/qr_arm.png"))
        self.otherButton = Button(self.root, image = photo)
        self.otherButton.config(text = "")
        self.otherButton.grid(row=11, column=0, columnspan=4, sticky="nsew")  
        self.publish_angles()      
        ##### --------------- #####
        self.ArmControlWindow.mainloop()

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
        q1=numpy.rad2deg(Q1)
        q1=self.qlimit(self.limits_map["q1"],q1)
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
        
        acum = math.radians(q2)
        x2 = self.l2*math.cos(acum) 
        y2 = self.l2*math.sin(acum)        
        acum+=math.radians(q3)
        x3 = x2+self.l3*math.cos(acum)
        y3 = y2+self.l3*math.sin(acum)
        acum+=math.radians(q4)
        x4 = x3+self.l4*math.cos(acum)
        y4 = y3+self.l4*math.sin(acum)

        if(y4 > self.limit_z and (x4 > self.limit_chassis or y4 >= 0)):
            self.publish_angles()
            
            self.values_map["joint1"] = x3
            self.values_map["joint3"] = y3
            
            self.angles_map["q1"] = q1
            self.angles_map["q2"] = q2
            self.angles_map["q3"] = q3
            self.angles_map["q4"] = q4
            return True
        else:
            return False

    def publish_angles(self):
        q1 = self.angles_map["q1"]
        q2 = self.angles_map["q2"]
        q3 = self.angles_map["q3"]
        q4 = self.angles_map["q4"]

        txt = str(q1)+" "+str(q2)+" "+str(q3)+" "+str(q4)
        rospy.loginfo(txt)
        self.pub_q1.publish(q1)
        self.pub_q2.publish(q2)
        self.pub_q3.publish(q3)
        self.pub_q4.publish(q4)
        self.pub_q_string.publish(txt)

    def qlimit(self, l, val):
        if (val < l[0]):
            return l[0]
        if (val > l[1]):
            return l[1]
        return val     

    def pressed(self, data, joint, sign = 1):        
        
        #self.lock_drive_teleop()
        ### phase of send the data of the joints
        key = "joint"+str(joint)
        self.values_map[key]+=(data*(sign*-1))    
        if(joint < 5):
            poss = self.ikine_brazo(self.values_map["joint1"], self.values_map["joint2"], self.values_map["joint3"], self.values_map["joint4"])
            if(not poss):
                self.values_map[key]+=(data*(sign))
        if(joint == 1):       
            if(data != 0):
                self.S1labelj1.config(bg="#34eb61")
            else:
                self.S1labelj1.config(bg="white")
        elif(joint == 2):
            if(data != 0):
                self.S1labelj2.config(bg="#34eb61")
            else:
                self.S1labelj2.config(bg="white")
        elif(joint == 3):
            if(data != 0):
                self.S1labelj3.config(bg="#34eb61")
            else:
                self.S1labelj3.config(bg="white")
        elif(joint == 4):            
            if(data != 0):
                self.S1labelj4.config(bg="#34eb61")
            else:
                self.S1labelj4.config(bg="white")
        elif(joint == 5):
            self.joint5.publish(self.values_map[key])
            if(data != 0):
                self.S1labelj5.config(bg="#34eb61")
            else:
                self.S1labelj5.config(bg="white")
        elif(joint == 6):
            self.gripper.publish(self.values_map[key])
            if(data != 0):
                self.S1labelj6.config(bg="#34eb61")
            else:
                self.S1labelj6.config(bg="white")
        
        self.labelInfo.config(text=self.getTxt())
        
        ### phase of unlock_drive_teleop and enable on_joy
        #self.unlock_drive_teleop()
        #time.sleep(.1)   

    def buttonsSection1(self, joint, row, col, desc, val=".2"):
        #exec('self.S1labelj' + str(joint) + ' = Label(self.root, font=("Consolas", 10), width=1, bg="white", bd=0, justify=CENTER, anchor=W)')
        exec('self.S1labelj' + str(joint) + ' = Button(self.root, font=("Consolas", 10), width=1, bg="white", bd=0, anchor=CENTER)')
        exec('self.S1labelj' + str(joint) + '.config(text=" ' +desc + ':")')
        exec('self.S1labelj' + str(joint) + '.grid(row=' + str(row) + ', column=' + str(col) + ', columnspan=1, sticky="nsew")')        

        exec('self.S1buttonj' + str(joint) + 'w = Button(self.root, font=("Consolas", 8, "bold"), width=1, bg="#ff523b", bd=0, justify=CENTER, fg="white")')
        exec('self.S1buttonj' + str(joint) + 'w.config(text="-")')
        exec('self.S1buttonj' + str(joint) + 'w.grid(row=' + str(row) + ', column=' + str(col+1) + ', columnspan=1, sticky="nsew")')

        exec('self.S1velj' + str(joint) + ' = Entry(self.root, font=("Consolas", 10), width=1, bg="white", bd=0, justify=CENTER)')
        exec('self.S1velj' + str(joint) + '.grid(row=' + str(row) + ', column=' + str(col+2) + ', columnspan=1, sticky="nsew")')
        exec('self.S1velj' + str(joint) + '.insert(0, '+val+')')

        exec('self.S1buttonj' + str(joint) + 'c = Button(self.root, font=("Consolas", 8, "bold"), width=1, bg="#ff523b", bd=0, justify=CENTER, fg="white")')
        exec('self.S1buttonj' + str(joint) + 'c.config(text="+")')
        exec('self.S1buttonj' + str(joint) + 'c.grid(row=' + str(row) + ', column=' + str(col+3) + ', columnspan=1, sticky="nsew")')        	

    def unpressed(self):
        self.S1labelj3.config(bg="white")
        self.S1labelj1.config(bg="white")            
        self.S1labelj2.config(bg="white")
        self.S1labelj3.config(bg="white")
        self.S1labelj4.config(bg="white")
        self.S1labelj5.config(bg="white")
        self.S1labelj6.config(bg="white")  
    
    def getTxt(self):
        txt = "Position X = "+str(round(self.values_map["joint1"],2))+"\n" + "Position Y = "+str(round(self.values_map["joint2"],2))+"\n"+"Position Z = "+str(round(self.values_map["joint3"],2))+"\n"
        txt += "Position Phi = "+str(self.values_map["joint4"])+"\n"+"Rotacion del gripper = "+str(self.values_map["joint5"])+"\n"
        txt += "Apertura del Gripper = "+str(self.values_map["joint6"])+"\n"
        txt += "q1:"+str(round(self.angles_map["q1"],2))+" q2:"+str(round(self.angles_map["q2"],2))+"\n"
        txt += "q3:"+str(round(self.angles_map["q3"],2))+" q4:"+str(round(self.angles_map["q4"],2))
        return txt

if __name__ == '__main__':
    try:
        rospy.init_node("sar_arm_velnopos_graph")
        sar_base_arm_test = ArmTeleop()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
