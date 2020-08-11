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
from Max_sum_TAC import *


def callback_end_of_movement(num_robot, x=0, y=0):
    global dict_end_of_movements
    dict_end_of_movements[num_robot] = 'end_of_movement'
    
    
def callback_my_position(num_robot, x='0', y='0'):
    global dict_neighbours_positions
    pos = [(0, 0, 0.0), (0.0, 0.0, 0.0, 1.0)]
    pos[0] = (float(x), float(y), 0.0)
    if dict_neighbours_positions[num_robot] == 'None':
        dict_neighbours_positions[num_robot] = pos


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


def self_callback(msg):
    global curr_pos
    global num_of_robot
    new_pos = String()
    new_pos.data = "%s,my_position,%s,%s" % (num_of_robot, curr_pos[0][0], curr_pos[0][1])
    pub.publish(new_pos)
    self_pub.publish(new_pos)
    rate.sleep()


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


def publish(curr_num_of_robot, message_type, x='x', y='y'):
    s = String()
    s.data = curr_num_of_robot + ',' + message_type + ',' + str(x) + ',' + str(y)
    pub.publish(s)
    
    
def collect_positions_from_neighbours():
    global dict_end_of_movements
    global dict_neighbours_positions
    while 'None' in dict_neighbours_positions.values():
        rate.sleep()
    print 'dict_neighbours_positions: %s' % dict_neighbours_positions

    while 'None' in dict_end_of_movements.values():
        rate.sleep()
    print 'dict_neighbours_positions (real): %s' % dict_end_of_movements


def in_range(position, target, SR):
    return math.sqrt((position[0][0] - target[0]) ** 2 + (position[0][1] - target[1]) ** 2) < SR


def transform(my_pos):
    pos = [(0, 0, 0.0), (0.0, 0.0, 0.0, 1.0)]
    pos[0] = (float(my_pos[0]), float(my_pos[1]), 0.0)
    return pos


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


class Agent:
    def __init__(self, number_of_robot):
        self.number_of_robot = number_of_robot
        self.name = 'agent%s' % number_of_robot
        self.inbox = {}
        self.named_inbox = {}
        
    def get_name(self):
        return self.name

    def get_num_of_agent(self):
        return self.number_of_robot
    
    def get_pos(self):
        return curr_pos

    def get_curr_nei(self):
        pass

    def get_curr_robot_nei(self):
        pass

    def get_MR(self):
        return vars.real_MR

    def get_SR(self):
        return vars.real_SR

    def get_access_to_inbox(self, type_of_requirement, num_of_agent=None, message=None, name=None):
        # logging.info("Thread %s has the lock inside %s", num_of_agent, self.number_of_robot)
        if type_of_requirement == 'message':
            # logging.info("Thread %s has the message: %s", num_of_agent, message)
            if num_of_agent in self.inbox:
                self.inbox[num_of_agent].append(message)
                self.named_inbox[name].append(message)
            else:
                print('[ERROR]: num_of_agent is NOT in self.inbox')
                # print(num_of_agent, ' inside Agent')
            # logging.info("Agent %s after update has the inbox: %s", self.number_of_robot, self.inbox)

        if type_of_requirement == 'copy':
            # logging.info("Thread %s about to release the lock!!!! inbox: %s", num_of_agent, self.inbox)
            return copy.deepcopy(self.inbox)
        # logging.info("Thread %s about to release lock inside %s", num_of_agent, self.number_of_robot)

    def get_access_to_named_inbox(self, type_of_requirement, name_of_agent=None, message=None):

        if type_of_requirement == 'message':
            # print(name_of_agent, 'is inside the ', self.name, '. Here $$$$$$$$$$$$$$$$$$$$$$')
            # print(list(self.named_inbox.keys()))
            if name_of_agent in self.named_inbox:

                self.named_inbox[name_of_agent].append(message)

            else:
                print('[ERROR]: num_of_agent is not in self.inbox')
        if type_of_requirement == 'copy':
            return copy.deepcopy(self.named_inbox)


if __name__ == '__main__':
    # try:
    rospy.init_node('robot%s' % sys.argv[1], anonymous=True)

    # ---------------------------
    # TEMP VARS
    # ---------------------------
    num_of_robot = sys.argv[1]
    curr_pos = vars.robots_start_positions[num_of_robot]
    dict_end_of_movements = {}
    agent = Agent(int(num_of_robot))
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
        new_pos = Max_sum_TAC({'agent': agent, 'for_alg': {'mini_iterations': 5,
                                                          'cred': 30, 
                                                          'SR': vars.real_SR, 
                                                          'pos_policy': 'random_furthest',
                                                          'TAC': True}})
        new_pos = transform(new_pos)
        if new_pos != curr_pos:
            print 'changed'
            curr_pos = new_pos
            # ----------------------------- #
            client.send_goal(goal_pose(curr_pos))
            client.wait_for_result()

        print "%s robot's position in the the end of %s iteration is %s " % (num_of_robot, iteration, curr_pos)
        publish(num_of_robot, 'end_of_movement')

        iteration += 1
        rate.sleep()

    print "Finished Max-sum_MST"