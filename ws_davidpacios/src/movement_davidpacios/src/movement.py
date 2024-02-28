#!/usr/bin/env python3

from __future__ import print_function
import numpy
from six.moves import input
import os
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import trajectory_msgs.msg
from std_msgs.msg import Float32
import franka_gripper.msg

import tf2_ros
import tf2_geometry_msgs  # Importante para realizar la transformación de geometría
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState
import actionlib
import panda_demo.msg


from math import pi, tau, dist, fabs, cos

from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list



def clear_screen():
    # Verifica si el sistema operativo es Windows o no
    if os.name == 'nt':
        # Si es Windows, usa 'cls' para limpiar la pantalla
        os.system('cls')
    else:
        # Si no es Windows, usa 'clear' para limpiar la pantalla
        os.system('clear')

## END_SUB_TUTORIAL


def all_close(goal, actual, tolerance):
    """
    Convenience method for testing if the values in two lists are within a tolerance of each other.
    For Pose and PoseStamped inputs, the angle between the two quaternions is compared (the angle
    between the identical orientations q and -q is calculated correctly).
    @param: goal       A list of floats, a Pose or a PoseStamped
    @param: actual     A list of floats, a Pose or a PoseStamped
    @param: tolerance  A float
    @returns: bool
    """
    if type(goal) is list:
        for index in range(len(goal)):
            if abs(actual[index] - goal[index]) > tolerance:
                return False

    elif type(goal) is geometry_msgs.msg.PoseStamped:
        return all_close(goal.pose, actual.pose, tolerance)

    elif type(goal) is geometry_msgs.msg.Pose:
        x0, y0, z0, qx0, qy0, qz0, qw0 = pose_to_list(actual)
        x1, y1, z1, qx1, qy1, qz1, qw1 = pose_to_list(goal)
        # Euclidean distance
        d = dist((x1, y1, z1), (x0, y0, z0))
        # phi = angle between orientations
        cos_phi_half = fabs(qx0 * qx1 + qy0 * qy1 + qz0 * qz1 + qw0 * qw1)
        return d <= tolerance and cos_phi_half >= cos(tolerance / 2.0)

    return True


class MoveGroupPythonInterfaceTutorial(object):
    """MoveGroupPythonInterfaceTutorial"""

    def __init__(self):
        super(MoveGroupPythonInterfaceTutorial, self).__init__()

        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node("pick_and_place_python", anonymous=True)

    
        robot = moveit_commander.RobotCommander()
        scene = moveit_commander.PlanningSceneInterface()

        move_group = moveit_commander.MoveGroupCommander("panda_arm")
        hand_group = moveit_commander.MoveGroupCommander("panda_hand")


        planning_frame = move_group.get_planning_frame()

        eef_link = move_group.get_end_effector_link()

        group_names = robot.get_group_names()
        
        # Misc variables
        self.box_name = "box"
        self.robot = robot
        self.scene = scene
        self.move_group = move_group
        self.hand_group = hand_group
        self.planning_frame = planning_frame
        self.eef_link = eef_link
        self.group_names = group_names

        self.move_client = actionlib.SimpleActionClient('franka_gripper/move', franka_gripper.msg.MoveAction)
        self.move_client.wait_for_server()

        self.callibration_client = actionlib.SimpleActionClient('gs_action', panda_demo.msg.GsAction)
        self.callibration_client.wait_for_server()

        print("============ Subscribing to topic gs_max_distance ...")
        self.max_dist = None
        rospy.Subscriber("gs_max_distance", Float32, self.cb_gs)
        while self.max_dist  == None and not rospy.is_shutdown():
            rospy.sleep(0.1)

    def get_current_pose(self):
        return self.move_group.get_current_pose().pose

    def openGripper(self, posture, opening):
        posture.joint_names = ["panda_finger_joint1","panda_finger_joint2"]

        posture.points.append(trajectory_msgs.msg.JointTrajectoryPoint())
        posture.points[0].positions = [opening,opening]
        return

    def closedGripper(self, posture, closing):
        posture.joint_names = ["panda_finger_joint1","panda_finger_joint2"]

        posture.points.append(trajectory_msgs.msg.JointTrajectoryPoint())
        posture.points[0].positions = [closing,closing]
        return

    def pick(self,grasp_pose):
        grasp = moveit_msgs.msg.Grasp()

        grasp.grasp_pose.header.frame_id = "panda_link0"
        grasp.grasp_pose.pose = grasp_pose


        grasp.pre_grasp_approach.direction.header.frame_id = "panda_link0"

        grasp.pre_grasp_approach.direction.vector.z = -1.0
        grasp.pre_grasp_approach.min_distance = 0.095
        grasp.pre_grasp_approach.desired_distance = 0.2


        grasp.post_grasp_retreat.direction.header.frame_id = "panda_link0"

        # grasp.post_grasp_retreat.direction.vector.z = 1.0
        # grasp.post_grasp_retreat.min_distance = 0.1
        # grasp.post_grasp_retreat.desired_distance = 0.25

        desired_opening = 0.04  # adjust as needed
        desired_closing = 0.04  # adjust as needed

        self.openGripper(grasp.pre_grasp_posture, desired_opening)
        self.closedGripper(grasp.grasp_posture, desired_closing)

        self.move_group.pick(self.box_name, grasp)

        self.move_group.stop()


        return

    def place(self,place_pose):

        place_location = moveit_msgs.msg.PlaceLocation()

        place_location.place_pose.header.frame_id = "panda_link0"
        place_location.place_pose.pose = place_pose

        place_location.pre_place_approach.direction.header.frame_id = "panda_link0"

        place_location.pre_place_approach.direction.vector.z = -1.0
        place_location.pre_place_approach.min_distance = 0.1
        place_location.pre_place_approach.desired_distance = 0.2


        place_location.post_place_retreat.direction.header.frame_id = "panda_link0"

        place_location.post_place_retreat.direction.vector.z = 1.0
        place_location.post_place_retreat.min_distance = 0.1
        place_location.post_place_retreat.desired_distance = 0.25

        desired_opening = 0.04
        self.openGripper(place_location.post_place_posture, desired_opening)

        self.move_group.place(self.box_name, place_location)

        self.move_group.stop()

        return

    def go_to_joint_state(self, j):
        move_group = self.move_group
        joint_goal = move_group.get_current_joint_values()
        joint_goal[0] = j[0]
        joint_goal[1] = j[1]
        joint_goal[2] = j[2]
        joint_goal[3] = j[3]
        joint_goal[4] = j[4]
        joint_goal[5] = j[5]
        joint_goal[6] = j[6]

        move_group.go(joint_goal, wait=True)

        move_group.stop()

        current_joints = move_group.get_current_joint_values()
        return all_close(joint_goal, current_joints, 0.01)

    def wait_for_state_update(self, box_is_known=False, box_is_attached=False, timeout=4):
        box_name = self.box_name
        scene = self.scene

        start = rospy.get_time()
        seconds = rospy.get_time()
        while (seconds - start < timeout) and not rospy.is_shutdown():
            attached_objects = scene.get_attached_objects([box_name])
            is_attached = len(attached_objects.keys()) > 0

            is_known = box_name in scene.get_known_object_names()

            if (box_is_attached == is_attached) and (box_is_known == is_known):
                return True

            rospy.sleep(0.1)
            seconds = rospy.get_time()

        return False

    def add_box(self, timeout=4):
        box_name = self.box_name
        scene = self.scene

        box_pose = geometry_msgs.msg.PoseStamped()
        box_pose.header.frame_id = "panda_link0"
        box_pose.pose.position.x = 0.4470
        box_pose.pose.position.y = 0.00
        box_pose.pose.position.z = 0.105/2 - 0.03
        box_pose.pose.orientation.x = 0.0
        box_pose.pose.orientation.y = 0.0
        box_pose.pose.orientation.z = 0.0

        scene.add_box(box_name, box_pose, size=(0.030, 0.03, 0.03))

        self.box_name = box_name
        return self.wait_for_state_update(box_is_known=True, timeout=timeout)

    def remove_box(self, timeout=4):
        box_name = self.box_name
        scene = self.scene

        scene.remove_world_object(box_name)
        return self.wait_for_state_update(
            box_is_attached=False, box_is_known=False, timeout=timeout
        )

     # Check if the gellsight is touched

    def check_touch(self):
        print("Data:",self.max_dist)
        return self.max_dist.data >= 5
    
    def cb_gs(self,dist) :
        self.max_dist = dist


    # Send a goal to the gripper
    def move_gripper(self,pose):
        goal = franka_gripper.msg.MoveGoal()
        goal.width = pose
        goal.speed = 0.3    

        self.move_client.send_goal(goal)
        self.move_client.wait_for_result()

    # Open the gripper
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


def main():
    try:
        initial_position = [0.00045490688645574993, -0.7849138098515794, 8.362466942548564e-05, -2.3567824603199075, -0.00021172463217377824, 1.5710602207713658, 0.7850459519227346]
        
        object_position = [-2.104341227623454, -0.4319778308001077, 2.5377667935354666, -2.5344143068273293, 0.8894710473178161, 2.8222173599137195, -1.1655434282617638]
        pose_pick = geometry_msgs.msg.Pose()
        pose_pick.position.x = 0.4161880497314183
        pose_pick.position.y = 0.11825780711004699
        pose_pick.position.z = 0.14369141349788575
        pose_pick.orientation.x = -0.9231143539216148
        pose_pick.orientation.y = -0.3840649074696301
        pose_pick.orientation.z = -0.01819345318830564
        pose_pick.orientation.w = 0.00479944739623474

        final_position = [1.7637484339747513, -0.7131722207323297, -0.09763801533611195, -2.82389828109355, -0.08833917383383795, 2.136842511844892, 0.9294967901285764, 0.03993682563304901, 0.03993682563304901]
        pose_place = geometry_msgs.msg.Pose()
        pose_place.position.y = 0.2
        pose_place.position.z = 0.105/2 - 0.03
        pose_place.orientation.x = 0.0
        pose_place.orientation.y = 0.0
        pose_place.orientation.z = 0.0
        pose_place.orientation.w = 1.0

        #clear_screen()
        print("")
        print("----------------------------------------------------------")
        print("Welcome to the Movement Tutorial, created by David Pacios")
        print("----------------------------------------------------------")
        print("Press Ctrl-D to exit at any time")
        print("")
        m = MoveGroupPythonInterfaceTutorial()
        
        while True:
            print("0. Initial position")
            print("1. Go to object position")
            print("2. Take object")
            print("3. Go to final posicion")
            print("4. Let object")
            print("5. Execute all")
            print("6. Exit")
            
            choice = input("Enter your choice (0-6): ")
            
            if choice == '0':
                if initial_position is not None:
                    m.go_to_joint_state(initial_position)
                else:
                    print("Initial position not set.")

            elif choice == '1':
                if object_position is not None:
                    m.go_to_joint_state(object_position)
                else:
                    print("Object position not set.")

            elif choice == '2':
                if pose_pick is not None:
                    m.pick(pose_pick)
                else:
                    print("Object position not set.")
                
            elif choice == '3':
                if final_position is not None:
                    m.go_to_joint_state(final_position)
                else:
                    print("Object position not set.")

            elif choice == '4':
                if pose_place is not None:
                    m.place(pose_place)
                else:
                    print("Object position not set.")
            elif choice == '5':

                if initial_position is not None and object_position is not None:
                    a = m.add_box()
                    print("Se ha añadido una caja: ", a)
                    print("Starting")
                    m.open_gripper()
                    m.go_to_joint_state(initial_position)
                    # Start calibration action
                    m.callibration_client.send_goal(panda_demo.msg.GsGoal())
                    print("Picking")
                    m.pick(pose_pick)
                    # Wait for the calibration to be done
                    m.callibration_client.wait_for_result()
                    print("Gellsight Mini Callibration Finished")

                    # Close the gripper progressively until the gellsight touches
                    poses = numpy.linspace(0.08,0.0,100)
                    for pose in poses:
                        m.move_gripper(pose)
                        if m.check_touch():
                            print("Toutching ... width =",pose)
                            break
                    print("Picked")

                    m.go_to_joint_state(initial_position)

                    print("Placing")
                    m.place(pose_place)
                    print("Placed")
                    
                    m.go_to_joint_state(initial_position)
                    m.open_gripper()
                    print("Ending")
                    a = m.remove_box()
                    print("Se ha eliminado una caja: ", a)
                else:
                    print("Not set.")

            elif choice == '6':
                if initial_position is not None:
                    m.go_to_joint_state(initial_position)
                else:
                    print("Initial position not set.")
                break
            else:
                print("Invalid choice. Please enter a number between 0 and 5.")

        print("============ Movement tutorial demo complete!")
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()