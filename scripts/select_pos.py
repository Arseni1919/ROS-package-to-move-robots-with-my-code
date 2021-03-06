#!/usr/bin/env python
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import datetime
import math
import random
import vars

# ------------------------------------------------------------------------------
# Variables
# ------------------------------------------------------------------------------
# robot_pos = [
#     [(1, 3, 0.0), (0.0, 0.0, 0.0, 1.0)],
#     [(1, 6, 0.0), (0.0, 0.0, 0.0, 1.0)],
#     [(4, 4, 0.0), (0.0, 0.0, 0.0, 1.0)],
#     [(4, 7, 0.0), (0.0, 0.0, 0.0, 1.0)],
#     [(6, 2, 0.0), (0.0, 0.0, 0.0, 1.0)],
#     [(7, 3, 0.0), (0.0, 0.0, 0.0, 1.0)],
#     [(7, 8, 0.0), (0.0, 0.0, 0.0, 1.0)],
#     [(8, 4, 0.0), (0.0, 0.0, 0.0, 1.0)],
#     [(8, 9, 0.0), (0.0, 0.0, 0.0, 1.0)]
# ]
#
# SR = 3  # meters
#
# targets = [
#     [2, 4, 4],
#     [3, 2, 3],
#     [6, 4, 7],
#     [7, 5, 5],
#     [8, 3, 5],
#     [8, 6, 3]
# ]


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def get_preferred_targets(arr):
    max = 0
    for i in arr:
        if i[2] > max:
            max = i[2]
    curr_arr = []
    for i in arr:
        if i[2] == max:
            curr_arr.append(i)
    return curr_arr


def in_range(position, target, SR):
    if math.sqrt((position[0][0] - target[0]) ** 2 + (position[0][1] - target[1]) ** 2) < SR:
        return True
    return False


def get_targets_within_SR_range(positions, preferred_targets, SR):
    curr_arr = []
    for target in preferred_targets:
        for position in positions:
            if in_range(position, target, SR):
                curr_arr.append(target)
                break
    return curr_arr


def get_possible_pos(positions, target_set, SR):
    curr_arr = []
    maximum_covered_targets = 0
    possible_pos = []
    for position in positions:
        curr_var = [position, 0]
        for target in target_set:
            if in_range(position, target, SR):
                curr_var[1] += 1
        curr_arr.append(curr_var)
        maximum_covered_targets = curr_var[1] if maximum_covered_targets < curr_var[1] else maximum_covered_targets
    for var in curr_arr:
        if var[1] == maximum_covered_targets:
            possible_pos.append(var[0])
    return possible_pos


def get_new_func(possible_pos, funcs, SR):
    funcs_in_range = get_targets_within_SR_range(possible_pos, funcs, SR)
    preferred_targets = get_preferred_targets(funcs)
    new_func = []
    for func in funcs_in_range:
        if func not in preferred_targets:
            new_func.append(func)
    return new_func


def select_pos(positions, funcs, SR):
    if len(positions) == 1:
        return goal_pose(positions[0])  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    target_set = get_targets_within_SR_range(positions, get_preferred_targets(funcs), SR)
    if len(target_set) == 0:
        return goal_pose(random.choice(positions))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    possible_pos = get_possible_pos(positions, target_set, SR)
    new_func = get_new_func(possible_pos, funcs, SR)
    return select_pos(possible_pos, new_func, SR)


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
    rospy.init_node('select_pos')
    client = actionlib.SimpleActionClient('/agent1/move_base', MoveBaseAction)
    client.wait_for_server()
    print "Hello"
    goal = select_pos(vars.robot_pos, vars.targets, vars.SR)
    client.send_goal(goal)
    client.wait_for_result()
    print("Finished")
