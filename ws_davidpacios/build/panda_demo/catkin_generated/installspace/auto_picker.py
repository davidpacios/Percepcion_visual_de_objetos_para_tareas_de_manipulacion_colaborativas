#!/usr/bin/env python3

from __future__ import print_function
from six.moves import input

import sys
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import trajectory_msgs.msg

from std_msgs.msg import Float32
import franka_gripper.msg
import panda_demo.msg

import tf2_ros
import tf2_geometry_msgs

from math import tau, dist, fabs, cos
import numpy as np

from moveit_commander.conversions import pose_to_list
import actionlib

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


class RobotInterface(object):
    def __init__(self):
        super(RobotInterface, self).__init__()

        # Initialize moveit commander and ros node
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node("auto_picker", anonymous=True)

        # Initialize tf2
        self.tf_buffer = tf2_ros.Buffer(rospy.Duration(100.0))
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)

        # Get move groups
        robot = moveit_commander.RobotCommander()
        scene = moveit_commander.PlanningSceneInterface()

        group_name = "panda_arm"
        move_group = moveit_commander.MoveGroupCommander(group_name)
        hand_group = moveit_commander.MoveGroupCommander("panda_hand")

        # Set move group parameters
        move_group.set_max_velocity_scaling_factor(0.5)
        move_group.set_max_acceleration_scaling_factor(0.5)
        # hand_group.set_goal_position_tolerance(0.08)


        #Setup Actions
        self.homing_client = actionlib.SimpleActionClient('franka_gripper/homing', franka_gripper.msg.HomingAction)
        self.homing_client.wait_for_server()

        self.move_client = actionlib.SimpleActionClient('franka_gripper/move', franka_gripper.msg.MoveAction)
        self.move_client.wait_for_server()

        self.callibration_client = actionlib.SimpleActionClient('gs_action', panda_demo.msg.GsAction)
        self.callibration_client.wait_for_server()


        print("============ Printing robot state")
        print(robot.get_current_state())
        print("")
        
        self.box_name = "box"
        self.robot = robot
        self.scene = scene
        self.move_group = move_group
        self.hand_group = hand_group
        self.pick_pose = None

        # Get the robot into the default state
        self.go_to_default_joint_state()
        print("============ Homing ...")
        self.homing()

        print("============ Subscribing to topic gs_max_distance ...")
        self.max_dist = None
        rospy.Subscriber("gs_max_distance", Float32, self.cb_gs)
        while self.max_dist  == None and not rospy.is_shutdown():
            rospy.sleep(0.1)
        

        print("============ Subscribing to topic /pick_place ...")
        rospy.Subscriber("/pick_pose", geometry_msgs.msg.PoseStamped, self.cb_pick)

    def go_to_default_joint_state(self):
        move_group = self.move_group

        # Default position joint values
        joint_goal = move_group.get_current_joint_values()
        joint_goal[0] = 0
        joint_goal[1] = -tau / 8
        joint_goal[2] = 0
        joint_goal[3] = -tau / 4
        joint_goal[4] = 0
        joint_goal[5] = tau / 6  # 1/6 of a turn
        joint_goal[6] = 0

        move_group.go(joint_goal, wait=True)
        move_group.stop()

        current_joints = move_group.get_current_joint_values()
        return all_close(joint_goal, current_joints, 0.01)

    def add_box(self, box_pose, timeout=4):
        box_name = self.box_name
        scene = self.scene
        # The box's size is not known but it's not a problem
        scene.add_box(box_name, box_pose, size=(0.030, 0.030, 0.030))

    def remove_box(self, timeout=4):
        box_name = self.box_name
        scene = self.scene
        move_group = self.move_group

        move_group.detach_object("panda_link8")
        scene.remove_world_object(box_name)

    def get_current_pose(self):
        return self.move_group.get_current_pose().pose

    # Definition for grasp msg
    def openGripper(self, posture):
        posture.joint_names = ["panda_finger_joint1","panda_finger_joint2"]

        posture.points.append(trajectory_msgs.msg.JointTrajectoryPoint())
        posture.points[0].positions = [0.04,0.04]
        posture.points[0].time_from_start = rospy.Duration.from_sec(0.5)
        return
    
    # Definition for grasp msg
    def closedGripper(self, posture):
        posture.joint_names = ["panda_finger_joint1","panda_finger_joint2"]

        posture.points.append(trajectory_msgs.msg.JointTrajectoryPoint())
        posture.points[0].positions = [0.04,0.04]
        # posture.points[0].effort = [5,5]
        posture.points[0].time_from_start = rospy.Duration.from_sec(0.5)
        return

    # Grasp
    def pick(self,grasp_pose):
        grasp = moveit_msgs.msg.Grasp()

        grasp.grasp_pose.header.frame_id = "panda_link0"
        grasp.grasp_pose.pose = grasp_pose


        grasp.pre_grasp_approach.direction.header.frame_id = "panda_link0"

        grasp.pre_grasp_approach.direction.vector.z = -1.0
        grasp.pre_grasp_approach.min_distance = 0.095
        grasp.pre_grasp_approach.desired_distance = 0.25


        grasp.post_grasp_retreat.direction.header.frame_id = "panda_link0"

        # grasp.post_grasp_retreat.direction.vector.z = 1.0
        # grasp.post_grasp_retreat.min_distance = 0.1
        # grasp.post_grasp_retreat.desired_distance = 0.25

        self.openGripper(grasp.pre_grasp_posture)
        self.closedGripper(grasp.grasp_posture)

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

        self.openGripper(place_location.post_place_posture)

        self.move_group.set_support_surface_name("table")
        self.move_group.place(self.box_name, place_location)

        self.move_group.stop()

        return

    # Franka gripper homing callibrates the fingers
    def homing(self):
        goal = franka_gripper.msg.HomingGoal()
        self.homing_client.send_goal(goal)

        self.homing_client.wait_for_result()

    # Send a goal to the gripper
    def move_gripper(self,pose):
        goal = franka_gripper.msg.MoveGoal()
        goal.width = pose
        goal.speed = 0.1

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
    
    # Check if the gellsight is touched
    def check_touch(self):
        print(self.max_dist)
        return self.max_dist.data >= 5

    # Callback functions
    def cb_pick(self,pose):
        self.pick_pose = pose
    
    def cb_gs(self,dist) :
        self.max_dist = dist
        

def main():
    try:
        print("")
        print("----------------------------------------------------------")
        print("Starting the automatic pick and place")
        print("----------------------------------------------------------")
        print("Press Ctrl-D to exit at any time")
        print("")
        
        interface = RobotInterface()

        print("Waiting for pose msg")
        
        pose = interface.pick_pose
        # Wait until pose msg is received
        while pose == None and not rospy.is_shutdown():
            pose = interface.pick_pose
            rospy.sleep(0.1)

        print("Caught pose msg \n============")

        # Move pose from camera frame to robot frame
        transform = interface.tf_buffer.lookup_transform("panda_link0",
                                       # source frame:
                                       pose.header.frame_id,
                                       # get the tf at the time the pose was valid
                                       pose.header.stamp,
                                       # wait for at most 1 second for transform, otherwise throw
                                       rospy.Duration(1.0))
        
        pose_transformed = tf2_geometry_msgs.do_transform_pose(pose, transform)

        #Add box at object pose
        box_pose = pose_transformed
        box_pose.pose.orientation.x = 0
        box_pose.pose.orientation.y = 0
        box_pose.pose.orientation.z = 0
        box_pose.pose.orientation.w = 1
        interface.add_box(box_pose)

        print("Added box at : ")
        print(box_pose)

        print("Pick position at : ")
        pose_transformed.pose.position.z += 0.13
        pose_transformed.pose.position.y += -0.05
        pose_transformed.pose.position.x += 0.02
        pose_transformed.pose.orientation.x = -0.9342
        pose_transformed.pose.orientation.y = -0.3563
        pose_transformed.pose.orientation.z = -0.0163
        pose_transformed.pose.orientation.w = 0.0083

        print(pose_transformed.pose)
        input(
            "============ Press `Enter` to pick ..."
        )

        # Start calibration action
        interface.callibration_client.send_goal(panda_demo.msg.GsGoal())

        # Get into grasp position
        interface.pick(pose_transformed.pose)

        # Wait for the calibration to be done
        interface.callibration_client.wait_for_result()
        print("Gellsight Mini Callibration Finished")

        # Close the gripper progressively until the gellsight touches
        poses = np.linspace(0.08,0.0,100)
        for pose in poses:
            interface.move_gripper(pose)
            if interface.check_touch():
                print("Toutching ... width =",pose)
                break

        print(interface.hand_group.get_current_joint_values())
        input(
            "============ Press `Enter` to place ..."
        )

        # Place at the given position
        wpose = geometry_msgs.msg.Pose()
        wpose.position.x = 0.4470
        wpose.position.y = 0.0061
        wpose.position.z = pose_transformed.pose.position.z - 0.15
        wpose.orientation.x = 0.0
        wpose.orientation.y = 0.0
        wpose.orientation.z = 0.0
        wpose.orientation.w = 1.0
        interface.place(wpose)

        input(
            "============ Press `Enter` to go to default state ..."
        )

        # set to default state
        interface.remove_box()
        interface.go_to_default_joint_state()
        interface.open_gripper()

        input(
            "============ Press `Enter` to finish ..."
        )
        print("============ Python demo complete!")

    except rospy.ROSInterruptException:
        return
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()