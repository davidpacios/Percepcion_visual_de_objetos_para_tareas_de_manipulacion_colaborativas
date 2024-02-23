#!/usr/bin/env python3
from __future__ import print_function
from six.moves import input

import sys
import rospy
import moveit_commander

try:
    from math import pi, tau
except ImportError:  # For Python 2 compatibility
    from math import pi

    tau = 2.0 * pi


class Movement(object):

    def __init__(self):
        super(Movement, self).__init__()

        moveit_commander.roscpp_initialize(sys.argv)

        # Establecer la dirección IP del robot como un parámetro global de ROS
        #rospy.set_param('/robot_ip', '172.16.0.2')

        rospy.init_node("movement", anonymous=True)

        robot = moveit_commander.RobotCommander(robot_description="robot_description", ns="")

        move_group = moveit_commander.MoveGroupCommander("panda_arm", robot_description="robot_description", ns="")

        self.robot = robot
        self.move_group = move_group

    def get_current_joint_state(self):
        move_group = self.move_group

        current_joint_state = move_group.get_current_joint_values()

        return current_joint_state
    
    def get_current_pose(self):
        return self.move_group.get_current_pose().pose

    def main(self):
        try:
            print("")
            print("----------------------------------------------------------")
            print("Welcome to the Movement Tutorial, created by David Pacios")
            print("----------------------------------------------------------")
            print("Press Enter to get the current joint state of the robot")
            print("Type 'exit' to quit")

            while True:
                # Wait for Enter to be pressed
                user_input = input("Press Enter to continue or 'exit' to quit: ")

                if user_input.lower() == 'exit':
                    print("Exiting the program.")
                    break

                # Get the current joint state of the robot
                current_joint_state = self.get_current_joint_state()
                # Get the current joint state of the robot
                current_pose = self.get_current_pose()

                print("Current joint state of the robot:", current_joint_state)
                print("Current pose of the robot:", current_pose)
        except KeyboardInterrupt:
            return

if __name__ == "__main__":
    movement = Movement()
    movement.main()
