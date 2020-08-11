#!/usr/bin/env python
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import datetime

# waypoints = [
# [(2.1, 2.2, 0.0), (0.0, 0.0, 0.0, 1.0)],
# [(6.5, 4.43, 0.0), (0.0, 0.0, -0.984047240305, 0.177907360295)]
# ]

waypoints = [
    [(1, 3, 0.0), (0.0, 0.0, 0.0, 1.0)],
    [(1, 6, 0.0), (0.0, 0.0, 0.0, 1.0)],
    [(7, 8, 0.0), (0.0, 0.0, 0.0, 1.0)],
    [(6, 2, 0.0), (0.0, 0.0, 0.0, 1.0)]
]


def goal_pose(pose):
    print("here in %s" % (datetime.datetime.now()))
    goal_pose = MoveBaseGoal()
    goal_pose.target_pose.header.frame_id = 'map'
    goal_pose.target_pose.pose.position.x = pose[0][0]
    goal_pose.target_pose.pose.position.y = pose[0][1]
    goal_pose.target_pose.pose.position.z = pose[0][2]
    goal_pose.target_pose.pose.orientation.x = pose[1][0]
    goal_pose.target_pose.pose.orientation.y = pose[1][1]
    goal_pose.target_pose.pose.orientation.z = pose[1][2]
    goal_pose.target_pose.pose.orientation.w = pose[1][3]

    return goal_pose


if __name__ == '__main__':
    rospy.init_node('patrol')

    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    # goal = goal_pose(waypoints[0])
    # client.send_goal(goal)
    # client.wait_for_result()

    while True:
        for pose in waypoints:
            goal = goal_pose(pose)
            client.send_goal(goal)
            client.wait_for_result()
