#!/usr/bin/env python
# coding=utf-8
"""Environment Information.

# Authors:  MohammadHossein GohariNejad <hoseingohari76@gmail.com>
# License:  BSD 3 clause

"""


import rospy;
import tf;
from geometry_msgs.msg import *;
from nav_msgs.msg import *;
from std_msgs.msg import *;
import threading;

t_lock=threading.Lock();
explored_percent=0;

def call_back(map_data):
    global explored_percent;
    global t_lock;
    t_lock.acquire();
    explored_percent=0;
    for i in map_data.data:
        if i>=0 :
            explored_percent+=1;
    t_lock.release();



def talker():
    global explored_percent;
    global t_lock;
    rospy.init_node('map_percent', anonymous=True)
    robot_name_space = rospy.get_param("robot_name", default="sos1");
    rospy.Subscriber("/"+robot_name_space+"/map", OccupancyGrid, call_back)
    pub = rospy.Publisher("/"+robot_name_space+"/percent_of_map", Float64, queue_size=10)
    rate = rospy.Rate(1.5) # 10hz
    while not rospy.is_shutdown():
        temp_data=Float64();
        t_lock.acquire();
        temp_data.data=explored_percent/10000.0;
        t_lock.release();
        pub.publish(temp_data)
        rate.sleep()
    rospy.spin()

talker();
