# ------------------------------------------------------------------------------
# Variables For Real Robots
# ------------------------------------------------------------------------------
vel = 0.3
key_mapping = {
    'w': [0, vel],
    'x': [0, -vel],
    'a': [vel, vel],
    'd': [-vel, vel],
    's': [0, 0]
}
# points of robots
p_1 = [(1, 1, 0.0), (0.0, 0.0, 0.0, 1.0)]
p_2 = [(2, 1, 0.0), (0.0, 0.0, 0.0, 1.0)]
p_3 = [(3, 1, 0.0), (0.0, 0.0, 0.0, 1.0)]
p_4 = [(1, -1, 0.0), (0.0, 0.0, 0.0, 1.0)]
p_5 = [(2, -1, 0.0), (0.0, 0.0, 0.0, 1.0)]
p_6 = [(3, -1, 0.0), (0.0, 0.0, 0.0, 1.0)]
p_7 = [(4, -1, 0.0), (0.0, 0.0, 0.0, 1.0)]
p_8 = [(2, -2, 0.0), (0.0, 0.0, 0.0, 1.0)]
p_9 = [(3, -2, 0.0), (0.0, 0.0, 0.0, 1.0)]
p_10 = [(4, -2, 0.0), (0.0, 0.0, 0.0, 1.0)]
p_11 = [(5, -2, 0.0), (0.0, 0.0, 0.0, 1.0)]
p_12 = [(2, -3, 0.0), (0.0, 0.0, 0.0, 1.0)]
p_13 = [(4, -3, 0.0), (0.0, 0.0, 0.0, 1.0)]
p_14 = [(3, -4, 0.0), (0.0, 0.0, 0.0, 1.0)]
p_15 = [(2, 0, 0.0), (0.0, 0.0, 0.0, 1.0)]
all_real_positions_for_robot = [p_1, p_2, p_3, p_4, p_5, p_6, p_7, p_8, p_9, p_10, p_11, p_12, p_13, p_14, p_15]

robots_start_positions = {
    '1': p_1,
    '3': p_7,
    '4': p_10,
    '5': p_8,
}

robots_possible_positions = {
    '1': all_real_positions_for_robot,
    '3': all_real_positions_for_robot,
    '4': all_real_positions_for_robot,
    '5': all_real_positions_for_robot,
}

neighbours = {
    '1':  # robot1
        ['3', '4', '5'],
    '3':  # robot3
        ['1', '4', '5'],
    '4':  # robot4
        ['1', '3', '5'],
    '5':  # robot 5
        ['1', '3', '4'],
}
# targets
target1 = [1, 0, 100]
target2 = [3, 0, 100]
target3 = [3, 3, 100]
# target4 = [2.4, 1, 2]
# target5 = [2.4, -2.1, 4]

real_targets = [target1, target2, target3]

real_SR = 1.35  # meters
real_MR = 1.35

credibility = {
    '1': 30,
    '2': 30,
    '3': 30,
    '4': 30,
    '5': 30,
    '6': 30,
    '7': 30,
    '8': 30,
    '9': 30,
}

dict_intersections_with = {
    '1': ['4'],
    '2': [],
    '3': ['5'],
    '4': ['1'],
    '5': ['3'],
    '6': [],
    '7': [],
    '8': [],
    '9': [],
}

num_of_iterations = 15
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Variables For Simulation
# ------------------------------------------------------------------------------
robot_pos = [
    [(1, 3, 0.0), (0.0, 0.0, 0.0, 1.0)],
    [(1, 6, 0.0), (0.0, 0.0, 0.0, 1.0)],
    [(4, 4, 0.0), (0.0, 0.0, 0.0, 1.0)],
    [(4, 7, 0.0), (0.0, 0.0, 0.0, 1.0)],
    [(6, 2, 0.0), (0.0, 0.0, 0.0, 1.0)],
    [(7, 3, 0.0), (0.0, 0.0, 0.0, 1.0)],
    [(7, 8, 0.0), (0.0, 0.0, 0.0, 1.0)],
    [(8, 4, 0.0), (0.0, 0.0, 0.0, 1.0)],
    [(8, 9, 0.0), (0.0, 0.0, 0.0, 1.0)]
]

SR = 3  # meters
MR = 10

targets = [
    [2, 4, 4],
    [3, 2, 3],
    [6, 4, 7],
    [7, 5, 5],
    [8, 3, 5],
    [8, 6, 3]
]

no_action_in_process = True
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------