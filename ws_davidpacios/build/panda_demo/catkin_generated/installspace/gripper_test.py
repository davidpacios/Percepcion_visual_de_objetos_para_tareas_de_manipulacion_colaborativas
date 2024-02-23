#!/usr/bin/env python3

from __future__ import print_function
from six.moves import input

import sys
import copy
import numpy as np
import rospy

import franka_gripper.msg
from std_msgs.msg import Float32

import actionlib


class checkCondition:
    def __init__(self):
        rospy.Subscriber("gs_max_distance", Float32, self.listen)

    def listen(self,max_dist):
        self.max_dist = max_dist

    def check_condition(self):
        print(self.max_dist)
        return self.max_dist.data >= 3

if __name__ == "__main__":

    rospy.init_node("gripper_test", anonymous=True)
    condition_checker = checkCondition()

    gripper_client = actionlib.SimpleActionClient('franka_gripper/grasp', franka_gripper.msg.GraspAction)
    gripper_client.wait_for_server()

    move_client = actionlib.SimpleActionClient('franka_gripper/move', franka_gripper.msg.MoveAction)
    move_client.wait_for_server()

    stop_client = actionlib.SimpleActionClient('franka_gripper/stop', franka_gripper.msg.StopAction)
    stop_client.wait_for_server()

    goal = franka_gripper.msg.MoveGoal()
    goal.width = 0.08
    goal.speed = 0.1

    move_client.send_goal(goal)

    move_client.wait_for_result()
    print(move_client.get_result())

    input("Next")

    poses = np.linspace(0.08,0.0,100)
    for pose in poses:
        goal = franka_gripper.msg.MoveGoal()
        goal.width = pose
        goal.speed = 0.1

        move_client.send_goal(goal)
        move_client.wait_for_result()

        if condition_checker.check_condition():
            print("Toutching ... width =",pose)
            break

    input("Next")

    goal = franka_gripper.msg.MoveGoal()
    goal.width = 0.08
    goal.speed = 0.1

    move_client.send_goal(goal)

    move_client.wait_for_result()
    print(move_client.get_result())