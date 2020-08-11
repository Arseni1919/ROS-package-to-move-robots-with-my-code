#!/usr/bin/env python
from __future__ import print_function
from std_msgs.msg import String
import random
import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import datetime
import sys

# Brings in the SimpleActionClient
import actionlib

# Brings in the messages used by the fibonacci action, including the
# goal message and the result message.
import actionlib_tutorials.msg

no_action_in_process = True
num_of_robot = sys.argv[1]
iteration = 1


def fibonacci_client(num):
    # Creates the SimpleActionClient, passing the type of the action
    # (FibonacciAction) to the constructor.
    client = actionlib.SimpleActionClient('fibonacci%s' % num_of_robot, actionlib_tutorials.msg.FibonacciAction)

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
    client.wait_for_result()

    # Prints out the result of executing the action
    return client.get_result()  # A FibonacciResult


def convert(format_string):
    return format_string.split(",")


def callback(msg):
    global no_action_in_process
    global iteration
    rate.sleep()
    message = convert(msg.data)
    if "robot%s" % num_of_robot not in message:
        if no_action_in_process:
            iteration += 1
            no_action_in_process = False


if __name__ == '__main__':
    try:

        rospy.init_node('robot%s' % num_of_robot, anonymous=True)

        pub = rospy.Publisher('position', String, queue_size=10)
        sub = rospy.Subscriber('position', String, callback)
        rate = rospy.Rate(1)

        if num_of_robot == "1":
            rospy.loginfo("before 1 sec")
            rate.sleep()
            rospy.loginfo("after 1 sec")

        while not rospy.is_shutdown():
            if not no_action_in_process:
                if sys.argv[1] == '1':
                    result = fibonacci_client(5)
                else:
                    result = fibonacci_client(7)
                print("Result:", ', '.join([str(n) for n in result.sequence]))
                no_action_in_process = True

            rate.sleep()
            new_pos = String()
            new_pos.data = "robot%s,%s" % (num_of_robot, iteration)
            rospy.loginfo(new_pos)
            pub.publish(new_pos)

        # rospy.spin()

    except rospy.ROSInterruptException:
        pass
