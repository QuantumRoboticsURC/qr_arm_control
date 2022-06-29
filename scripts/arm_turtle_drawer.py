#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
import turtle

screen = turtle.getscreen()
tortuga = turtle.Turtle()
x, y = 0, 0

buttons, axes = [0,0,0,0,0,0,0], [0,0,0]

def callback(data):
	global buttons, axes
	buttons = data.buttons [:]
	axes = data.axes [:]


rospy.init_node('arm_turle_drawer')
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
