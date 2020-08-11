#!/usr/bin/env python
from __future__ import print_function
from std_msgs.msg import String
import random
import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import datetime

# Brings in the SimpleActionClient
import actionlib

# Brings in the messages used by the fibonacci action, including the
# goal message and the result message.
import actionlib_tutorials.msg

def fibonacci_client(num):
    # Creates the SimpleActionClient, passing the type of the action
    # (FibonacciAction) to the constructor.
    client = actionlib.SimpleActionClient('fibonacci', actionlib_tutorials.msg.FibonacciAction)

    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()

    # Creates a goal to send to the action server.
    goal = actionlib_tutorials.msg.FibonacciGoal(order=num)

    # Sends the goal to the action server.
    client.send_goal(goal)

    # rospy.Rate(0.5).sleep()
    # client.cancel_goal()

    # Waits for the server to finish performing the action.
    rospy.loginfo(client.wait_for_result())

    # Prints out the result of executing the action
    return client.get_result()  # A FibonacciResult


def convert_dict(dict_format_string):
    d = {}
    elems = dict_format_string.split(",")
    values = elems[1::2]
    keys = elems[0::2]
    d.update(zip(keys, values))
    return d


def callback(msg):
    rate.sleep()
    message = convert_dict(msg.data)
    if "robot2" in message:
        num = int(message.get("robot2")) + 1
        new_pos = String()
        new_pos.data = "robot1,%s" % num
        rospy.loginfo(new_pos)
        pub.publish(new_pos)


if __name__ == '__main__':
    try:

        pub = rospy.Publisher('position', String, queue_size=10)
        sub = rospy.Subscriber('position', String, callback)
        rospy.init_node('robot1', anonymous=True)
        rate = rospy.Rate(1)

        rospy.loginfo("before 1 sec")
        rate.sleep()
        rospy.loginfo("after 1 sec")

        pos = String()
        pos.data = "robot1,0"
        rospy.loginfo(pos)
        pub.publish(pos)

        rospy.spin()

    except rospy.ROSInterruptException:
        pass
