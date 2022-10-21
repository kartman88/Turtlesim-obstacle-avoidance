#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32

def callback(msg):
    print("Ho sentito: ", msg)
    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("coni", Float32, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()              