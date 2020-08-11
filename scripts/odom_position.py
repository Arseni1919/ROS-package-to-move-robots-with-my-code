#!/usr/bin/env python
from __future__ import print_function
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped
import rospy
import sys


def callback(msg):
    rate.sleep()
    print('x_pose:  %s' % msg.pose.position.x)
    print('y_pose:  %s' % msg.pose.position.y)
    print('---')
    rate.sleep()

def callback_amcl(msg):
    rate.sleep()
    print('---')
    print('x_pose_amcl: %s' % msg.pose.pose.position.x)
    print('y_pose_amcl: %s' % msg.pose.pose.position.y)
    print('---')
    rate.sleep()

if __name__ == '__main__':
    try:

        rospy.init_node('odom_position_of_robot%s' % sys.argv[1], anonymous=True)
        # sub = rospy.Subscriber('/agent%s/pose' % sys.argv[1], PoseStamped, callback)
        sub_amcl = rospy.Subscriber('/agent%s/amcl_pose' % sys.argv[1], PoseWithCovarianceStamped, callback_amcl)


        rate = rospy.Rate(1)

        rospy.spin()

    except rospy.ROSInterruptException:
        pass
