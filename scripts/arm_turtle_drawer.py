#!/usr/bin/env python

"""
Team: QUANTUM ROBOTICS

Made by:Raul Lopez Musito
		a01378976@tec.mx
		raulmusito@gmail.com

Modified (DD/MM/YY): 
	Raul Musito 29/06/2022 Creation

Code description:
1. Suscribes to a Joy node
2. Uses de joy topic info to draw into a turtle screen

Notas:
-Beginner code
"""

#dependencies
import rospy
from sensor_msgs.msg import Joy
import turtle

#Turtle params
screen = turtle.getscreen()
tortuga = turtle.Turtle()
x, y = 0, 0

#global variables
buttons, axes = [0,0,0,0,0,0,0], [0,0,0]

#assignation to the global variables
def callback(data):
	global buttons, axes
	buttons = data.buttons [:]
	axes = data.axes [:]


rospy.init_node('arm_turle_drawer')	#creates node
image_sub = rospy.Subscriber("joy",Joy,callback)
rate = rospy.Rate(20)

while not rospy.is_shutdown():
	try:
		if buttons[0] == 0:
			tortuga.penup()
		else:
			tortuga.pendown ()
			
		if buttons[1] == 1:
			tortuga.clear()
		tortuga.pensize((axes[2]+1)*15)
		
		x, y = -axes[0]*300,axes[1]*300
		print ("x: ", x, " y: ", y)
		tortuga.goto(x,y)
		rate.sleep()

	except rospy.ROSInterruptException:
		rospy.logerr("ROS Interrupt Exception, done by User!")
	except rospy.ROSTimeMovedBackwardsException:
		rospy.logerr("ROS Time Backwards! Just ignore it!")
