#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

cmd_vel_pub = rospy.Publisher('agent1/cmd_vel', Twist, queue_size=1)
rospy.init_node('kadima')
rate = rospy.Rate(10)  # hz

while not rospy.is_shutdown():
    twist = Twist()
    twist.linear.x = 1
    cmd_vel_pub.publish(twist)
    print('here')

    rate.sleep()
