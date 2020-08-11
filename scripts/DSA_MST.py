#!/usr/bin/env python
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from tf.transformations import quaternion_from_euler
from geometry_msgs.msg import *
import datetime
import math
import random
import vars
import sys
import numpy as np


# from geometry_msgs.msg import Twist


# ------------------------------------------------------------------------------
# ARGS [int] -> number of Robot
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# SELECT_POS
# ------------------------------------------------------------------------------
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
    return math.sqrt((position[0][0] - target[0]) ** 2 + (position[0][1] - target[1]) ** 2) < SR


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
        return positions[0]
    target_set = get_targets_within_SR_range(positions, get_preferred_targets(funcs), SR)
    if len(target_set) == 0:
        return random.choice(positions)
    possible_pos = get_possible_pos(positions, target_set, SR)
    new_func = get_new_func(possible_pos, funcs, SR)
    return select_pos(possible_pos, new_func, SR)


def goal_pose(pose):
    # print("in goal_pose %s" % (datetime.datetime.now()))
    goal_pose = MoveBaseGoal()
    goal_pose.target_pose.header.frame_id = 'map'
    goal_pose.target_pose.pose.position.x = pose[0][0]
    goal_pose.target_pose.pose.position.y = pose[0][1]
    goal_pose.target_pose.pose.position.z = pose[0][2]
    goal_pose.target_pose.pose.orientation.x = pose[1][0]
    goal_pose.target_pose.pose.orientation.y = pose[1][1]
    goal_pose.target_pose.pose.orientation.z = pose[1][2]
    goal_pose.target_pose.pose.orientation.w = pose[1][3]

    # orient = Quaternion(*quaternion_from_euler(0, 0, yaw))
    # goal_pose.target_pose.pose.orientation = orient

    return goal_pose


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# calculate_improvement
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
def calculate_improvement(temp_REQ, curr_pos, new_pos, SR, my_cred):
    def get_val(pos):
        val = 0
        for target in temp_REQ:
            if in_range(pos, target, SR):
                val += min(target[2], my_cred)
        return val

    curr_cov = get_val(curr_pos)
    new_cov = get_val(new_pos)
    print('calculate_improvement: %s' % (new_cov >= curr_cov))
    return new_cov >= curr_cov
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


def near_by(robot_possible_positions, curr_pos):
    near_pos = robot_possible_positions[0]
    min = math.sqrt((near_pos[0][0] - curr_pos[0][0]) ** 2 + (near_pos[0][1] - curr_pos[0][1]) ** 2)
    for pos in robot_possible_positions:
        if math.sqrt((pos[0][0] - curr_pos[0][0]) ** 2 + (pos[0][1] - curr_pos[0][1]) ** 2) < min:
            near_pos = pos
    return near_pos


def collect_positions_from_neighbours():
    global dict_end_of_movements
    global dict_neighbours_positions
    while 'None' in dict_neighbours_positions.values():
        rate.sleep()
    print 'dict_neighbours_positions: %s' % dict_neighbours_positions

    while 'None' in dict_end_of_movements.values():
        rate.sleep()
    print 'dict_neighbours_positions (real): %s' % dict_end_of_movements


def collect_possible_new_positions_from_neighbours():
    global dict_neighbours_positions
    while 'None' in dict_neighbours_positions.values():
        rate.sleep()
    print 'dict_neighbours_positions (possible): %s' % dict_neighbours_positions


def get_reachable_positions(num_robot, curr_pos):
    all_positions = vars.robots_possible_positions[num_robot]
    curr_possible_positions = []
    for pos in all_positions:
        dist = math.sqrt(((pos[0][0] - curr_pos[0][0])**2) + ((pos[0][1] - curr_pos[0][1])**2))
        if dist <= vars.real_MR:
            curr_possible_positions.append(pos)
    print 'reachable_positions: %s' % curr_possible_positions
    return curr_possible_positions


def get_temp_REQ(targets, sr):
    global dict_neighbours_positions
    temp_req_targets = []
    for target in targets:
        new_target = [target[0], target[1], target[2]]
        for key in dict_neighbours_positions.keys():
            if in_range(dict_neighbours_positions[key], target, sr):
                if new_target[2] < vars.credibility[key]:
                    new_target[2] = 0
                else:
                    new_target[2] = new_target[2] - vars.credibility[key]
        temp_req_targets.append(new_target)
    print "temp_req_targets: %s" % temp_req_targets
    return temp_req_targets


def replacement_decision(prob, temp_REQ, curr_pos, new_pos, SR, my_cred):
    if calculate_improvement(temp_REQ, curr_pos, new_pos, SR, my_cred):
        return random.random() < prob
    return False


def publish(curr_num_of_robot, message_type, x='x', y='y'):
    s = String()
    s.data = curr_num_of_robot + ',' + message_type + ',' + str(x) + ',' + str(y)
    pub.publish(s)


def callback(msg):
    """
    :param msg: '[robot],[message type],[x],[y]'
    message type:
    1. end_of_movement - my end of movement
    2. my_position - sending my current position
    :return: none
    """
    global num_of_robot
    message = msg.data.split(',')
    if message[0] != num_of_robot:
        {
            'end_of_movement': callback_end_of_movement,
            'my_position': callback_my_position,
        }[message[1]](message[0], message[2], message[3])


def callback_end_of_movement(num_robot, x=0, y=0):
    global dict_end_of_movements
    dict_end_of_movements[num_robot] = 'end_of_movement'


def callback_my_position(num_robot, x='0', y='0'):
    global dict_neighbours_positions
    pos = [(0, 0, 0.0), (0.0, 0.0, 0.0, 1.0)]
    pos[0] = (float(x), float(y), 0.0)
    if dict_neighbours_positions[num_robot] == 'None':
        dict_neighbours_positions[num_robot] = pos


def self_callback(msg):
    global curr_pos
    global num_of_robot
    new_pos = String()
    new_pos.data = "%s,my_position,%s,%s" % (num_of_robot, curr_pos[0][0], curr_pos[0][1])
    pub.publish(new_pos)
    self_pub.publish(new_pos)
    rate.sleep()


def calc_remaining_coverage_req(num_of_robot, curr_pos, dict_neighbours_positions):
    remaining_coverage_req = 0
    for target in vars.real_targets:
        total = target[2]
        if in_range(curr_pos, target, vars.real_SR):
            total = max(0, total - vars.credibility.get(num_of_robot))
        for rob_num, pos in dict_neighbours_positions.iteritems():
            if in_range(pos, target, vars.real_SR):
                total = max(0, total - vars.credibility.get(rob_num))
        remaining_coverage_req += total
    return remaining_coverage_req


def pos_after_checking_intersections(old_dict_neighbours_positions, dict_neighbours_positions, num_of_robot, old_pose,
                                     new_pos):
    for intersection_with in vars.dict_intersections_with.get(num_of_robot):
        q = [old_pose[0][0], old_pose[0][1]]
        p = [old_dict_neighbours_positions.get(intersection_with)[0][0],
             old_dict_neighbours_positions.get(intersection_with)[0][1]]
        s = [new_pos[0][0] - old_pose[0][0], new_pos[0][1] - old_pose[0][1]]
        r = [dict_neighbours_positions.get(intersection_with)[0][0] -
             old_dict_neighbours_positions.get(intersection_with)[0][0],
             dict_neighbours_positions.get(intersection_with)[0][1] -
             old_dict_neighbours_positions.get(intersection_with)[0][1]]
        if np.cross(r, s) != 0:
            t = np.cross(list(np.array(q) - np.array(p)), s)/np.cross(r, s)
            if 0 <= t <= 1:
                u = np.cross(list(np.array(q) - np.array(p)), r)/np.cross(r, s)
                if 0 <= u <= 1:
                    if int(intersection_with) < int(num_of_robot):
                        print "robot %s draw back (ustupaet) to %s" % (num_of_robot, intersection_with)
                        return old_pose
        # --------------------------------------------- #
        for val in dict_neighbours_positions.values():
            if new_pos[0][0] == val[0][0]:
                if new_pos[0][1] == val[0][1]:
                    return old_pose
        # --------------------------------------------- #
    return new_pos


if __name__ == '__main__':
    # try:

    rospy.init_node('robot%s' % sys.argv[1], anonymous=True)

    # ---------------------------
    # TEMP VARS
    # ---------------------------
    num_of_robot = sys.argv[1]
    curr_pos = vars.robots_start_positions[num_of_robot]
    dict_end_of_movements = {}
    end_of_movement = False
    dict_neighbours_positions = {key: 'None' for key in vars.neighbours.get(num_of_robot)}
    # ---------------------------

    pub = rospy.Publisher('rob_messages', String, queue_size=10)
    sub = rospy.Subscriber('rob_messages', String, callback)
    self_pub = rospy.Publisher('self_pos_of_%s' % sys.argv[1], String, queue_size=10)
    self_sub = rospy.Subscriber('self_pos_of_%s' % sys.argv[1], String, self_callback)

    rate = rospy.Rate(1)

    client = actionlib.SimpleActionClient('agent%s/move_base' % sys.argv[1], MoveBaseAction)
    client.wait_for_server()

    print "All subs, pubs, vars and clients are in action"
    print "In this experiment the targets are: %s" % vars.real_targets

    client.send_goal(goal_pose(curr_pos))
    client.wait_for_result()
    new_pos = String()
    new_pos.data = "%s,my_position,%s,%s" % (num_of_robot, curr_pos[0][0], curr_pos[0][1])
    self_pub.publish(new_pos)
    publish(num_of_robot, 'end_of_movement')

    # ------------------------------------------------------------------------------------------------------------------
    # ITERATIONS
    # ------------------------------------------------------------------------------------------------------------------
    iteration = 0
    # while not rospy.is_shutdown():
    while iteration < vars.num_of_iterations:
        print("robot %s beginning of %s iteration" % (num_of_robot, iteration))
        dict_neighbours_positions = {key: 'None' for key in vars.neighbours.get(num_of_robot)}
        collect_positions_from_neighbours()
        dict_end_of_movements = {key: 'None' for key in vars.neighbours.get(num_of_robot)}

        print(' ---\n for_graph:\n %s, %s,\n ---\n' % (
            str(iteration), str(calc_remaining_coverage_req(num_of_robot, curr_pos, dict_neighbours_positions))))

        print("robot %s start calculating" % num_of_robot)
        possible_positions = get_reachable_positions(num_of_robot, curr_pos)
        temp_REQ = get_temp_REQ(vars.real_targets, vars.real_SR)
        new_pos = select_pos(possible_positions, temp_REQ, vars.real_SR)

        if replacement_decision(0.8, temp_REQ, curr_pos, new_pos, vars.real_SR, vars.credibility[num_of_robot]):
            print "robot %s in replacement_decision" % num_of_robot
            old_pose = curr_pos
            # ----- for intersections ----- #
            old_dict_neighbours_positions = dict(dict_neighbours_positions)
            dict_neighbours_positions = {key: 'None' for key in vars.neighbours.get(num_of_robot)}
            collect_possible_new_positions_from_neighbours()
            curr_pos = pos_after_checking_intersections(old_dict_neighbours_positions, dict_neighbours_positions,
                                                        num_of_robot, old_pose, new_pos)
            if old_pose != curr_pos:
                print 'changed'
            # ----------------------------- #
            client.send_goal(goal_pose(curr_pos))
            client.wait_for_result()

        print "%s robot's position in the the end of %s iteration is %s " % (num_of_robot, iteration, curr_pos)
        publish(num_of_robot, 'end_of_movement')

        iteration += 1
        rate.sleep()

    print "Finished DSA_MST"

    # except rospy.ROSInterruptException:
    #    pass
