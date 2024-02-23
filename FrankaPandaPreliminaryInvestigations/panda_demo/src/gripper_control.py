#!/usr/bin/env python

from __future__ import print_function
from six.moves import input

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import trajectory_msgs.msg

from std_srvs.srv import Empty

import tf2_ros
import tf2_geometry_msgs

from math import pi, tau, dist, fabs, cos
import numpy as np

from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list


class RobotInterface(object):

    def __init__(self):
        super(RobotInterface, self).__init__()

        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node("gripper_control", anonymous=True)

        robot = moveit_commander.RobotCommander()
        scene = moveit_commander.PlanningSceneInterface()

        group_name = "panda_arm"
        move_group = moveit_commander.MoveGroupCommander(group_name)
        hand_group = moveit_commander.MoveGroupCommander("panda_hand")

        # hand_group.set_goal_position_tolerance(0.08)
        print(hand_group.get_goal_tolerance())

        self.robot = robot
        self.scene = scene
        self.move_group = move_group
        self.hand_group = hand_group

    def open_gripper(self):

        plan = moveit_msgs.msg.RobotTrajectory()

        plan.joint_trajectory.header.frame_id="panda_link0"
        plan.joint_trajectory.joint_names = ["panda_finger_joint1","panda_finger_joint2"]

        point1 = trajectory_msgs.msg.JointTrajectoryPoint()
        point1.positions = self.hand_group.get_current_state().joint_state.position[7:9]
        point1.effort = [0,0]
        point1.time_from_start = rospy.Duration.from_sec(0.0)

        point2 = trajectory_msgs.msg.JointTrajectoryPoint()
        point2.positions = [0.04,0.04]
        point2.effort = [0,0]
        point2.time_from_start = rospy.Duration.from_sec(0.5)

        plan.joint_trajectory.points.append(point1)
        plan.joint_trajectory.points.append(point2)

        self.hand_group.execute(plan, wait=True)
        self.hand_group.stop()
    
    def close_gripper(self):

        plan = moveit_msgs.msg.RobotTrajectory()

        plan.joint_trajectory.header.frame_id="panda_link0"
        plan.joint_trajectory.joint_names = ["panda_finger_joint1","panda_finger_joint2"]

        point1 = trajectory_msgs.msg.JointTrajectoryPoint()
        point1.positions = self.hand_group.get_current_state().joint_state.position[7:9]
        point1.effort = [0,0]
        point1.time_from_start = rospy.Duration.from_sec(0.0)

        point2 = trajectory_msgs.msg.JointTrajectoryPoint()
        point2.positions = [0.0,0.0]
        point2.effort = [0,0]
        point2.time_from_start = rospy.Duration.from_sec(0.5)

        plan.joint_trajectory.points.append(point1)
        plan.joint_trajectory.points.append(point2)

        self.hand_group.execute(plan, wait=True)
        self.hand_group.stop()

    def gripper_goto(self,pose):

        plan = moveit_msgs.msg.RobotTrajectory()

        plan.joint_trajectory.header.frame_id="panda_link0"
        plan.joint_trajectory.joint_names = ["panda_finger_joint1","panda_finger_joint2"]

        point1 = trajectory_msgs.msg.JointTrajectoryPoint()
        point1.positions = self.hand_group.get_current_state().joint_state.position[7:9]
        point1.effort = [0,0]
        point1.time_from_start = rospy.Duration.from_sec(0.0)

        point2 = trajectory_msgs.msg.JointTrajectoryPoint()
        point2.positions = [pose,pose]
        point2.effort = [1,1]
        point2.time_from_start = rospy.Duration.from_sec(2)

        plan.joint_trajectory.points.append(point1)
        plan.joint_trajectory.points.append(point2)

        self.hand_group.execute(plan, wait=True)
    

def main():
    try:
        print("----------------------------------------------------------")
        print("Starting test")
        print("----------------------------------------------------------")
        print("Press Ctrl-D to exit at any time")
        print("")
        
        interface = RobotInterface()

        interface.open_gripper()
        poses = np.linspace(0.04,0.00,100)
        print(poses)
        for p in poses:
            interface.gripper_goto(p)
        print("============ Python test complete!")
    except rospy.ROSInterruptException:
        return
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
