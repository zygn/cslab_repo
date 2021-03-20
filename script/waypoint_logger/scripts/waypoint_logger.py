#!/usr/bin/env python
import rospy
import numpy as np
import atexit
import tf
import sensor_msgs.msg
import message_filters

from os.path import expanduser
from time import gmtime, strftime
from numpy import linalg as LA
from tf.transformations import euler_from_quaternion
from nav_msgs.msg import Odometry

home = expanduser('~')


file = open(strftime(home+'/map_temp/wps/wp-%Y-%m-%d-%H-%M-%S',gmtime())+'.csv', 'w')


def save_waypoint(joy, odom):
    # print(joy)
    # print(odom)
    

    if joy.axes[1] != 0.0 and joy.buttons[4] == 1:
        
        data = odom

        quaternion = np.array([data.pose.pose.orientation.x, 
                            data.pose.pose.orientation.y, 
                            data.pose.pose.orientation.z, 
                            data.pose.pose.orientation.w])

        euler = tf.transformations.euler_from_quaternion(quaternion)
        speed = LA.norm(np.array([data.twist.twist.linear.x, 
                                data.twist.twist.linear.y, 
                                data.twist.twist.linear.z]),2)
        if data.twist.twist.linear.x>0.:
            print data.twist.twist.linear.x

        file.write('%f, %f, %f, %f\n' % (data.pose.pose.position.x,
                                        data.pose.pose.position.y,
                                        euler[2],
                                        speed))
    else:
        pass 


def shutdown():
    file.close()
    print('Goodbye')
 
def listener():
    rospy.init_node('waypoints_logger', anonymous=True)
    

    joy_sub = message_filters.Subscriber('/vesc/joy', sensor_msgs.msg.Joy)
    odom_sub = message_filters.Subscriber('/vesc/odom', Odometry)

    ts = message_filters.ApproximateTimeSynchronizer([joy_sub, odom_sub], 10, 0.1, allow_headerless=True)
    ts.registerCallback(save_waypoint)

    rospy.spin()


if __name__ == '__main__':
    atexit.register(shutdown)
    print('Saving waypoints...')
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
