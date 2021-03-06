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
from Algorithms_help_functions import *


def max_sum_function_node(target, for_alg):
    curr_nei = target.get_curr_nei()
    # max_sum_nei_check(curr_nei, Agent)
    mini_iterations = for_alg['mini_iterations']
    for i in range(mini_iterations):
        order_of_message = i + 1
        wait_to_receive(target, order_of_message)

        inbox = target.get_access_to_inbox('copy')
        # print_inbox_len(1, target, inbox)
        fmr_nei = select_FMR_nei(target, curr_nei, for_alg)
        # print('fmr_nei length: ', len(fmr_nei))

        for nei in curr_nei:
            received_message = inbox[nei.get_num_of_agent()][i]
            possible_pos = received_message.keys()
            inside_fmr = nei in fmr_nei
            new_message = max_sum_function_message_to(nei, inbox, possible_pos, inside_fmr,
                                                      target, for_alg['cred'], for_alg['SR'])
            send_message_to(nei, target, new_message)


def max_sum_TAC_variable_node(agent, for_alg, all_real_positions_for_robot):
    curr_nei = agent.get_curr_nei()
    curr_robot_nei = agent.get_curr_robot_nei()
    # max_sum_nei_check(curr_nei, Target)
    mini_iterations = for_alg['mini_iterations']
    order_of_message, order_of_named_message = 1, 1

    possible_pos = get_possible_pos_with_MR_general(agent, all_real_positions_for_robot)
    new_message = max_sum_create_null_variable_message(possible_pos)

    send_and_receive_TAC(agent, new_message, order_of_message, order_of_named_message, possible_pos)
    order_of_named_message += 2
    order_of_message += 1

    for i in range(mini_iterations - 1):

        # var to targets
        for nei in curr_nei:
            message_to_nei = var_message_to_func(nei, agent, possible_pos, i)  # , my_sum_of_all_messages)
            send_message_to(nei, agent, message_to_nei)
        wait_to_receive(agent, order_of_message)
        order_of_message += 1

        # var to func robots
        for nei in curr_robot_nei:
            message_to_nei = var_message_to_func(nei, agent, possible_pos, i)  # , my_sum_of_all_messages)
            send_named_message_to(nei, agent, message_to_nei)
        wait_to_receive_certain_named(agent, curr_robot_nei, order_of_named_message)
        order_of_named_message += 1

        # func to var robots
        inbox = agent.get_access_to_inbox('copy')
        new_message = get_sum_of_all_messages(inbox, possible_pos)
        for nei in curr_robot_nei:
            message_to_nei = robot_func_to_var_message_TAC(nei, agent, new_message, i)
            send_named_message_to(nei, agent, message_to_nei)
        wait_to_receive_certain_named(agent, curr_robot_nei, order_of_named_message)
        order_of_named_message += 1

    sum_of_all_TAC_messages = get_sum_of_all_TAC_messages(agent, possible_pos)
    if max(sum_of_all_TAC_messages.values()) < 0:
        print(agent.get_name(), 'inside max_sum_TAC_variable_node bad!!!!!!!!!', max(sum_of_all_TAC_messages.values()))
        return agent.get_pos()

    set_of_max_pos = get_set_of_max_pos(agent, sum_of_all_TAC_messages, for_alg['pos_policy'])
    next_pos = random.choice(set_of_max_pos)
    return next_pos

def Max_sum_TAC(kwargs):
    """
    :param kwargs:
    :return:
    """
    agent = kwargs['agent']
    for_alg = kwargs['for_alg']
    # agents = kwargs['agents']
    # targets = kwargs['targets']
    # cells = kwargs['cells']

    if 'target' in agent.get_name():
        max_sum_function_node(agent, for_alg)

    if 'agent' in agent.get_name():
        # logging.info("Thread %s : in FOO", threading.get_ident())
        # return max_sum_TAC_variable_node(agent, cells, targets, agents, for_alg)
        return max_sum_TAC_variable_node(agent, for_alg, vars.all_real_positions_for_robot)