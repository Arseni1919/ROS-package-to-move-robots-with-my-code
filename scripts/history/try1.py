#!/usr/bin/env python
# import rospy
# from std_msgs.msg import String
#
#
# def callback(msg):
#     print msg.data
#     new_msg = String()
#     new_msg.data = str(int(msg.data) + 1)
#     pub.publish(new_msg)
#     with open("example.txt", 'a') as mfile:  # Use file to refer to the file object
#         mfile.write('%s, %s, ' % ('dhbfgbhfgb', 'b'))
#         print "bla"
#     rate.sleep()
#
#
# if __name__ == '__main__':
#     rospy.init_node('my_node', anonymous=True)
#     pub = rospy.Publisher('my_topic', String, queue_size=10)
#     sub = rospy.Subscriber('my_topic', String, callback)  #
#     rate = rospy.Rate(1)
#     rate.sleep()
#     msg = String()
#     print "hello"
#     msg.data = "1"
#     pub.publish(msg)
#     rospy.spin()


# with open("example.txt", 'a') as file:  # Use file to refer to the file object
#     file.write('%s, %s, ' % ('a', 'b'))
# with open("example.txt", 'r') as file:  # Use file to refer to the file object
#     data = file.read()
#     print data
import numpy as np
import vars
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
    return new_pos

print(pos_after_checking_intersections({'1': vars.b_1}, {'1': vars.a_1}, '4', vars.a_4, vars.b_4))