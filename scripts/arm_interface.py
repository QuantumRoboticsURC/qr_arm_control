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

class ArmTeleop:
    def __init__(self):        
        ### Initialize the publisher for the joints        
        self.pub_q1 = rospy.Publisher('arm_teleop/joint1', Float64, queue_size=1)
        self.pub_q2 = rospy.Publisher('arm_teleop/joint2', Float64, queue_size=1)
        self.pub_q3 = rospy.Publisher('arm_teleop/joint3', Float64, queue_size=1)
        self.pub_q4 = rospy.Publisher('arm_teleop/joint4', Float64, queue_size=1)
        self.pub_q_string = rospy.Publisher('inverse_kinematics/Q', String, queue_size=1)
        self.joint5 = rospy.Publisher('arm_teleop/joint5', Int32, queue_size=1) #gripper rotacion
        self.gripper = rospy.Publisher('arm_teleop/gripper', Float64, queue_size=1) #lineal 
        self.lineal = rospy.Publisher('arm_teleop/prism', Float64, queue_size=1) #lineal 
        self.camera = rospy.Publisher('arm_teleop/cam', Int32, queue_size=1) #lineal 
        
        self.gripper_apertur = 60 #0 y 60
        self.blueTec = "#466cbe"#466cbe
        self.released = "#466cbe"
        self.values_map = {
            "joint1": 0,#.4
            "joint2": 0,#.9
            "joint3": .75,
            "joint4": 0,#phi
            "joint5": 0,#rotacion
            "joint8": 140,#camera
        }
        self.rospack = rospkg.RosPack()

        self.l1 = 0
        self.l2 = 2.6
        self.l3 = 2.6
        self.l4 = .9

        self.limits_map = {
            "q1":(-90,90),
            "q2":(0,161),
            "q3":(-165.4,0),
            "q4":(-135,90),
            "joint5":(-90,90),
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

        self.buttonsSection1(2, 5, 0, "Position Y","5")
        self.S1buttonj2c.bind("<ButtonPress-1>", lambda event: self.pressed(float("-"+self.S1velj2.get()), 2),-1)
        self.S1buttonj2w.bind("<ButtonPress-1>", lambda event: self.pressed(float(self.S1velj2.get()), 2))
        self.S1buttonj2w.bind("<ButtonRelease-1>", lambda event: self.unpressed())        
        self.S1buttonj2c.bind("<ButtonRelease-1>", lambda event: self.unpressed())

        self.buttonsSection1(3, 6, 0, "Position Z")
        self.S1buttonj3c.bind("<ButtonPress-1>", lambda event: self.pressed(float("-"+self.S1velj3.get()) , 3))
        self.S1buttonj3w.bind("<ButtonPress-1>", lambda event: self.pressed(float(self.S1velj3.get()), 3))
        self.S1buttonj3w.bind("<ButtonRelease-1>", lambda event: self.unpressed())        
        self.S1buttonj3c.bind("<ButtonRelease-1>", lambda event: self.unpressed())

        #self.buttonsSection1(4, 7, 0,"Phi", "5")
        self.S1labelj4 = Button(self.root, font=("Consolas", 10), width=1, bg="white", bd=0, anchor=CENTER)
        self.S1labelj4.config(text="Phi")
        self.S1labelj4.grid(row=7, column=0, columnspan=1, sticky="nsew")            
        self.S1velj4 = Entry(self.root, font=("Consolas", 10), width=1, bg="white", bd=0, justify=CENTER)
        self.S1velj4.grid(row=7, column=1, columnspan=1, sticky="nsew")
        self.S1velj4.insert(0,0)        
        self.S1buttonj4c = Button(self.root, font=("Consolas", 8, "bold"), width=1, bg=self.blueTec, bd=0, justify=CENTER, fg="white")
        self.S1buttonj4c.config(text = "Go")
        self.S1buttonj4c.grid(row=7, column=2, columnspan=2, sticky="nsew")
        self.S1buttonj4c.bind("<ButtonPress-1>", lambda event: self.pressed(float(self.S1velj4.get()) , 4),-1)
        self.S1buttonj4c.bind("<ButtonRelease-1>", lambda event: self.unpressed())

        """exec('self.S1buttonj' + str(joint) + 'c = Button(self.root, font=("Consolas", 8, "bold"), width=1, bg=self.blueTec, bd=0, justify=CENTER, fg="white")')
        exec('self.S1buttonj' + str(joint) + 'c.config(text="+")')
        exec('self.S1buttonj' + str(joint) + 'c.grid(row=' + str(row) + ', column=' + str(col+3) + ', columnspan=1, sticky="nsew")')        	"""


        self.S1labelj5 = Button(self.root, font=("Consolas", 10), width=1, bg="white", bd=0, anchor=CENTER)
        self.S1labelj5.config(text="Rotacion del gripper")
        self.S1labelj5.grid(row=8, column=0, columnspan=1, sticky="nsew")            
        self.S1velj5 = Entry(self.root, font=("Consolas", 10), width=1, bg="white", bd=0, justify=CENTER)
        self.S1velj5.grid(row=8, column=1, columnspan=1, sticky="nsew")
        self.S1velj5.insert(0,0)        
        self.S1buttonj5c = Button(self.root, font=("Consolas", 8, "bold"), width=1, bg=self.blueTec, bd=0, justify=CENTER, fg="white")
        self.S1buttonj5c.config(text = "Go")
        self.S1buttonj5c.grid(row=8, column=2, columnspan=2, sticky="nsew")
        self.S1buttonj5c.bind("<ButtonPress-1>", lambda event: self.pressed(float(self.S1velj5.get()) , 5),-1)
        self.S1buttonj5c.bind("<ButtonRelease-1>", lambda event: self.unpressed())        

       # self.buttonsSection1(6, 9, 0,"Gripper","30")
        self.S1labelj6 = Button(self.root, font=("Consolas", 10), width=1, bg="white", bd=0, anchor=CENTER)
        self.S1labelj6.config(text="Gripper")
        self.S1labelj6.grid(row=9, column=0, columnspan=1, sticky="nsew")            

        self.S1buttonj6w = Button(self.root, font=("Consolas", 8, "bold"), width=1, bg=self.blueTec, bd=0, justify=CENTER, fg="white")
        self.S1buttonj6w.config(text = "Cerrar")
        self.S1buttonj6w.grid(row=9, column=2, columnspan=1, sticky="nsew")
        self.S1buttonj6c = Button(self.root, font=("Consolas", 8, "bold"), width=1, bg=self.blueTec, bd=0, justify=CENTER, fg="white")
        self.S1buttonj6c.config(text = "Abrir")
        self.S1buttonj6c.grid(row=9, column=3, columnspan=1, sticky="nsew")
        self.S1buttonj6w.bind("<ButtonPress-1>", lambda event: self.pressed(int("-1") , 6),-1)
        self.S1buttonj6c.bind("<ButtonPress-1>", lambda event: self.pressed(int(1) , 6))
        self.S1buttonj6c.bind("<ButtonRelease-1>", lambda event: self.unpressedj6())        
        self.S1buttonj6w.bind("<ButtonRelease-1>", lambda event: self.unpressedj6())






        #self.buttonsSection1(7, 10, 0,"Actuador prismatico","30")
        self.S1labelj7 = Button(self.root, font=("Consolas", 10), width=1, bg="white", bd=0, anchor=CENTER)
        self.S1labelj7.config(text="Actuador prismatico")
        self.S1labelj7.grid(row=10, column=0, columnspan=1, sticky="nsew")            
        self.S1buttonj7w = Button(self.root, font=("Consolas", 8, "bold"), width=1, bg=self.blueTec, bd=0, justify=CENTER, fg="white")
        self.S1buttonj7w.config(text = "Cerrar")
        self.S1buttonj7w.grid(row=10, column=2, columnspan=1, sticky="nsew")
        self.S1buttonj7c = Button(self.root, font=("Consolas", 8, "bold"), width=1, bg=self.blueTec, bd=0, justify=CENTER, fg="white")
        self.S1buttonj7c.config(text = "Abrir")
        self.S1buttonj7c.grid(row=10, column=3, columnspan=1, sticky="nsew")
        self.S1buttonj7c.bind("<ButtonPress-1>", lambda event: self.pressed(int("-1") , 7),-1)
        self.S1buttonj7w.bind("<ButtonPress-1>", lambda event: self.pressed(int(1) , 7))
        self.S1buttonj7w.bind("<ButtonRelease-1>", lambda event: self.unpressedj7())        
        self.S1buttonj7c.bind("<ButtonRelease-1>", lambda event: self.unpressedj7())

        #CAMERA
        self.buttonsSection1(8, 11, 0,"Camera","10")
        self.S1buttonj8w.bind("<ButtonPress-1>", lambda event: self.pressed(float(self.S1velj8.get()) , 8))
        self.S1buttonj8w.bind("<ButtonRelease-1>", lambda event: self.unpressed())
        self.S1buttonj8c.bind("<ButtonPress-1>", lambda event: self.pressed(float("-"+self.S1velj8.get()) , 8),-1)
        self.S1buttonj8c.bind("<ButtonRelease-1>", lambda event: self.unpressed())


        #POSICIONES
        self.labelTitleS2 = Label(self.root, font=("Consolas", 12), width=36, bg="white", bd=0, justify=CENTER)
        self.labelTitleS2.config(text="Posiciones directas")
        self.labelTitleS2.grid(row=1, column=5, columnspan=4, sticky="nsew")        

        self.labelTitleS2 = Label(self.root, font=("Consolas", 12), width=36, bg="white", bd=0, justify=CENTER)
        self.labelTitleS2.config(text="Home")
        self.labelTitleS2.grid(row=2, column=5, columnspan=4, sticky="nsew")

        self.S2buttonp2 = Button(self.root, font=("Consolas", 8, "bold"), width=1, bg=self.blueTec, bd=0, justify=CENTER, fg="white")
        self.S2buttonp2.config(text = "intermedio")
        self.S2buttonp2.grid(row=4, column=5, columnspan=4, sticky="nsew", padx=50)
        self.S2buttonp2.bind("<ButtonPress-1>", lambda event: self.PresionadoDerecha("INTERMEDIO"))

        self.S2buttonp3 = Button(self.root, font=("Consolas", 8, "bold"), width=1, bg=self.blueTec, bd=0, justify=CENTER, fg="white")
        self.S2buttonp3.config(text = "home")
        self.S2buttonp3.grid(row=5, column=5, columnspan=4, sticky="nsew", padx=50)
        self.S2buttonp3.bind("<ButtonPress-1>", lambda event: self.PresionadoDerecha("HOME"))

        self.S2buttonp4 = Button(self.root, font=("Consolas", 8, "bold"), width=1, bg=self.blueTec, bd=0, justify=CENTER, fg="white")
        self.S2buttonp4.config(text = "storage")
        self.S2buttonp4.grid(row=6, column=5, columnspan=4, sticky="nsew", padx=50)
        self.S2buttonp4.bind("<ButtonPress-1>", lambda event: self.PresionadoDerecha("STORAGE"))


        self.labelTitleS2 = Label(self.root, font=("Consolas", 12), width=36, bg="white", bd=0, justify=CENTER)
        self.labelTitleS2.config(text=" ")
        self.labelTitleS2.grid(row=7, column=5, columnspan=4, sticky="nsew", padx=50)  

        self.S2buttonp2 = Button(self.root, font=("Consolas", 8, "bold"), width=1, bg=self.blueTec, bd=0, justify=CENTER, fg="white")
        self.S2buttonp2.config(text = "Pull")
        self.S2buttonp2.grid(row=8, column=5, columnspan=4, sticky="nsew", padx=50)
        self.S2buttonp2.bind("<ButtonPress-1>", lambda event: self.PresionadoDerecha("PULL"))

        self.S2buttonp3 = Button(self.root, font=("Consolas", 8, "bold"), width=1, bg=self.blueTec, bd=0, justify=CENTER, fg="white")
        self.S2buttonp3.config(text = "Write")
        self.S2buttonp3.grid(row=9, column=5, columnspan=4, sticky="nsew", padx=50)
        self.S2buttonp3.bind("<ButtonPress-1>", lambda event: self.PresionadoDerecha("WRITE"))

        self.S2buttonp4 = Button(self.root, font=("Consolas", 8, "bold"), width=1, bg=self.blueTec, bd=0, justify=CENTER, fg="white")
        self.S2buttonp4.config(text = "Floor")
        self.S2buttonp4.grid(row=10, column=5, columnspan=4, sticky="nsew", padx=50)
        self.S2buttonp4.bind("<ButtonPress-1>", lambda event: self.PresionadoDerecha("FLOOR"))            


        #self.entryandlabelsSection2(1, 4, 4)

        self.labelInfo = Label(self.root, font=("Consolas", 11), width=36, bg="white", bd=0, justify=LEFT)
        txt = "Position X = "+str(round(self.values_map["joint1"],2))+"\n" + "Position Y = "+str(round(self.values_map["joint2"],2))+"\n"+"Position Z = "+str(round(self.values_map["joint3"],2))+"\n"
        txt += "Position Phi = "+str(self.values_map["joint4"])+"\n"+"Rotacion del gripper = "+str(self.values_map["joint5"])+"\n"
        txt += "Camera = " + str(self.values_map["joint8"])+"\n"
        txt += "q1:"+str(round(self.angles_map["q1"],2))+"\nq2:"+str(round(self.angles_map["q2"],2))+"\n"
        txt += "q3:"+str(round(self.angles_map["q3"],2))+"\nq4:"+str(round(self.angles_map["q4"],2))
        self.labelInfo.config(text=txt)
        self.labelInfo.grid(row=12, column=0, columnspan=4, sticky="nsew")
        
        photo = ImageTk.PhotoImage(Image.open(self.rospack.get_path('qr_arm_control')+"/scripts/qr_arm.png")) 
        self.otherButton = Button(self.root, image = photo)
        self.otherButton.config(text = "")        
        self.otherButton.grid(row=13, column=0, columnspan=4, sticky="nsew")
        #self.publish_angles()      
        ##### --------------- #####
        self.ArmControlWindow.mainloop()

    def PresionadoDerecha(self, id):
        #print("presionado", id)
        x = self.values_map["joint1"]
        y = self.values_map["joint2"]
        z = self.values_map["joint3"]
        phi = self.values_map["joint4"]
        if(id == "HOME"):
            x = .134
            y =  0
            z =  .75#.647 
            phi = 0
        elif(id == "INTERMEDIO"):
            x = 0
            y = 0
            z = 3.677
            phi = 0
        elif(id == "PULL"):
            x = 3.33
            y = 0
            z = 3.35
        elif (id == "WRITE"):
            x = 3.33
            y = 0
            z = 1.35
        elif (id == "FLOOR"):
            x = 3.28
            y = 0
            z = -2.37
            phi = 0
        elif (id == "STORAGE"):
            x = .134
            y =  0
            z =  .84
            phi = 90
        self.values_map["joint1"] = x
        self.values_map["joint2"] = y
        self.values_map["joint3"] = z
        self.values_map["joint4"] = phi
        self.ikine_brazo(self.values_map["joint1"], self.values_map["joint2"], self.values_map["joint3"], self.values_map["joint4"])
        self.labelInfo.config(text=self.getTxt())
        


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
            #self.publish_angles()
            self.values_map["joint1"] = x3
            self.values_map["joint3"] = y3

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

    def my_map(self,in_min, in_max, out_min, out_max, x):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def pressed(self, data, joint, sign = 1):        
        
        #self.lock_drive_teleop()
        ### phase of send the data of the joints
        key = "joint"+str(joint)
        if(joint == 6):
            data*=-1
            self.gripper.publish(data)        
            if(data != 0):
                self.S1labelj6.config(bg="#34eb61")
            else:
                self.S1labelj6.config(bg="white")
            return None
        if(joint == 7):
            data*=-1
            self.lineal.publish(data)
            return None

        if(joint == 4):
            prev = self.values_map[key]
            self.values_map[key] = data
            poss = self.ikine_brazo(self.values_map["joint1"], self.values_map["joint2"], self.values_map["joint3"], self.values_map["joint4"])            
            if(not poss):
                print("Ya valio x1")
                self.values_map[key] = prev
        elif (joint == 5):
            self.values_map[key] = self.qlimit(self.limits_map["joint5"],data)
            self.joint5.publish(self.my_map(-90,90,1230,1770,self.values_map[key]))
        else:    
            self.values_map[key]+=(data*(sign*-1))    
        if(joint == 2):
            self.angles_map["q1"]+=(data*(sign*-1))    
            self.angles_map["q1"] = self.qlimit(self.limits_map["q1"],self.angles_map["q1"])
            
        if(joint < 4 and joint != 2):
            poss = self.ikine_brazo(self.values_map["joint1"], self.values_map["joint2"], self.values_map["joint3"], self.values_map["joint4"])            
            if(not poss):
                print("ya valio x2")
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
        elif(joint == 8):
            self.values_map[key] = self.qlimit(self.limits_map["camera"], self.values_map[key])
            self.camera.publish(self.values_map[key])            
            if(data != 0):
                self.S1labelj8.config(bg="#34eb61")
            else:
                self.S1labelj8.config(bg="white")
        self.labelInfo.config(text=self.getTxt())
        
        ### phase of unlock_drive_teleop and enable on_joy
        #self.unlock_drive_teleop()
        #time.sleep(.1)   

    def buttonsSection1(self, joint, row, col, desc, val=".2"):
        #exec('self.S1labelj' + str(joint) + ' = Label(self.root, font=("Consolas", 10), width=1, bg="white", bd=0, justify=CENTER, anchor=W)')
        exec('self.S1labelj' + str(joint) + ' = Button(self.root, font=("Consolas", 10), width=1, bg="white", bd=0, anchor=CENTER)')
        exec('self.S1labelj' + str(joint) + '.config(text=" ' +desc + ':")')
        exec('self.S1labelj' + str(joint) + '.grid(row=' + str(row) + ', column=' + str(col) + ', columnspan=1, sticky="nsew")')        

        exec('self.S1buttonj' + str(joint) + 'w = Button(self.root, font=("Consolas", 8, "bold"), width=1, bg=self.blueTec, bd=0, justify=CENTER, fg="white")')
        exec('self.S1buttonj' + str(joint) + 'w.config(text="-")')
        exec('self.S1buttonj' + str(joint) + 'w.grid(row=' + str(row) + ', column=' + str(col+1) + ', columnspan=1, sticky="nsew")')

        exec('self.S1velj' + str(joint) + ' = Entry(self.root, font=("Consolas", 10), width=1, bg="white", bd=0, justify=CENTER)')
        exec('self.S1velj' + str(joint) + '.grid(row=' + str(row) + ', column=' + str(col+2) + ', columnspan=1, sticky="nsew")')
        exec('self.S1velj' + str(joint) + '.insert(0, '+val+')')

        exec('self.S1buttonj' + str(joint) + 'c = Button(self.root, font=("Consolas", 8, "bold"), width=1, bg=self.blueTec, bd=0, justify=CENTER, fg="white")')
        exec('self.S1buttonj' + str(joint) + 'c.config(text="+")')
        exec('self.S1buttonj' + str(joint) + 'c.grid(row=' + str(row) + ', column=' + str(col+3) + ', columnspan=1, sticky="nsew")')        	


    def unpressedj7(self):
        self.S1labelj7.config(bg="white")
        self.lineal.publish(0.0)    

    def unpressedj6(self):
        self.S1labelj6.config(bg="white")
        self.gripper.publish(0.0)    

    def unpressed(self):
        self.S1labelj3.config(bg="white")
        self.S1labelj1.config(bg="white")            
        self.S1labelj2.config(bg="white")
        self.S1labelj3.config(bg="white")
        self.S1labelj4.config(bg="white")
        self.S1labelj5.config(bg="white")
        self.S1labelj6.config(bg="white")  
        self.S1labelj8.config(bg="white") 
    
    def getTxt(self):
        self.publish_angles()
        txt = "Position X = "+str(round(self.values_map["joint1"],2))+"\n" + "Position Y = "+str(round(self.values_map["joint2"],2))+"\n"+"Position Z = "+str(round(self.values_map["joint3"],2))+"\n"
        txt += "Position Phi = "+str(self.values_map["joint4"])+"\n"+"Rotacion del gripper = "+str(self.values_map["joint5"])+"\n"
        txt += "Camera = " + str(self.values_map["joint8"])+"\n"
        txt += "q1:"+str(round(self.angles_map["q1"],2))+"\nq2:"+str(round(self.angles_map["q2"],2))+"\n"
        txt += "q3:"+str(round(self.angles_map["q3"],2))+"\nq4:"+str(round(self.angles_map["q4"],2))
        return txt

if __name__ == '__main__':
    try:
        rospy.init_node("sar_arm_velnopos_graph")
        sar_base_arm_test = ArmTeleop()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass