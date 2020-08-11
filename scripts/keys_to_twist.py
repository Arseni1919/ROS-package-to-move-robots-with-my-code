#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

key_mapping = { 
'w': [ 0, 1], 
'x': [0, -1],
'a': [-1, 0], 
'd': [1, 0],
's': [ 0, 0] 
}

def keys_cb(msg):#twist_pub
	if len(msg.data) == 0 or not key_mapping.has_key(msg.data[0]):
		return # unknown key
	else:
		print(msg)
		vels = key_mapping[msg.data[0]]
		t = Twist()
		t.angular.z = vels[0]
		t.linear.x = vels[1]
		print(4343)
		twist_pub.publish(t)

if __name__ == '__main__':
	rospy.init_node('keys_to_twist')
	#twist_pub = rospy.Publisher('agent1/ackermann_cmd', Twist, queue_size=1)
	rospy.Subscriber('keys', String, keys_cb)#twist_pub
	#rospy.Subscriber('/agent1/scan', String, keys_cb, twist_pub)
	print('hello')
	rospy.spin()
