#!/usr/bin/env python3

from adafruit_servokit import ServoKit
import rospy
from std_msgs.msg import Int64, Int32
import time

def servo_arm(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    print ("entre a callback")
    #kit.servo[servo_dos].angle= data.data
    if (data.data >= -90 and data.data <= 90):
        kit.servo[servo_dos].angle=int(map(data.data, -90, 90, 236, 416))
        kit.servo[servo_dos].duty_cycle = 0
    
def listener():
    rospy.init_node('arm_servo', anonymous=True)
    subscriber_gripper = rospy.Subscriber("arm_teleop/joint5", Int32, servo_arm, queue_size = 10)
    print ("ready")
    rospy.spin()

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

if __name__ == '__main__':
    kit = ServoKit(channels=16)
    servo_arm = 15
    kit.servo[servo_arm].angle=180
    listener()
