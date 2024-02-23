#!/usr/bin/env python

from __future__ import print_function
from six.moves import input

import sys
import rospy

import panda_demo.msg

import actionlib

if __name__ == "__main__":

    rospy.init_node("callibration_test", anonymous=True)

    callibration_client = actionlib.SimpleActionClient('gs_action', panda_demo.msg.GsAction)
    callibration_client.wait_for_server()

    goal = panda_demo.msg.GsGoal()

    callibration_client.send_goal(goal)

    callibration_client.wait_for_result()
    print(callibration_client.get_result())
