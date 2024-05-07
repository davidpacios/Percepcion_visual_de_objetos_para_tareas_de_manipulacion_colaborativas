#!/usr/bin/env python3

from __future__ import print_function
import numpy
from six.moves import input
import os
import sys
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import trajectory_msgs.msg
from std_msgs.msg import Float32
import franka_gripper.msg
import actionlib
import panda_demo.msg
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped

initial_position = [0.00045490688645574993, -0.7849138098515794, 8.362466942548564e-05, -2.3567824603199075, -0.00021172463217377824, 1.5710602207713658, 0.7850459519227346]
object_position = [-2.104341227623454, -0.4319778308001077, 2.5377667935354666, -2.5344143068273293, 0.8894710473178161, 2.8222173599137195, -1.1655434282617638]
final_position = [0.31117872249452694, 0.661868957685263, 0.23851138023744548, -1.9054843345423356, -0.29362653295861346, 2.599592895878686, -0.050700302571436415]
pose_place = geometry_msgs.msg.Pose()
pose_place.position.x = 0.46409545551322356
pose_place.position.y = 0.3672940207021908
pose_place.position.z = 0.04
pose_place.orientation.x = 0
pose_place.orientation.y = 0
pose_place.orientation.z = 0
pose_place.orientation.w = 1

gripper_max_opening = 0.04  # adjust as needed

def clear_screen():
    # Verifica si el sistema operativo es Windows o no
    if os.name == 'nt':
        # Si es Windows, usa 'cls' para limpiar la pantalla
        os.system('cls')
    else:
        # Si no es Windows, usa 'clear' para limpiar la pantalla
        os.system('clear')

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

        print("============ Subscribing to topic arucos_poses_trf ...")
        self.arucos = None
        rospy.Subscriber("aruco_poses_trf", String, self.callback_arucos_position)
        while not self.arucos and not rospy.is_shutdown():
            rospy.sleep(0.1)

        print("============ Subscribing to topic gs_max_distance ...")
        self.max_dist = None
        rospy.Subscriber("gs_max_distance", Float32, self.callback_gelsightmini)
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

    
    def move_to_pick(self, grasp_pose):
        grasp = moveit_msgs.msg.Grasp()

        grasp.grasp_pose.header.frame_id = "panda_link0"
        grasp.grasp_pose.pose = grasp_pose

        grasp.pre_grasp_approach.direction.header.frame_id = "panda_link0"
        grasp.pre_grasp_approach.direction.vector.z = -1.0
        grasp.pre_grasp_approach.min_distance = 0.095
        grasp.pre_grasp_approach.desired_distance = 0.2

        grasp.post_grasp_retreat.direction.header.frame_id = "panda_link0"

        self.openGripper(grasp.pre_grasp_posture, gripper_max_opening)
        self.closedGripper(grasp.grasp_posture, gripper_max_opening)

        # Planear la trayectoria sin ejecutarla
        plan = self.move_group.plan()

        if plan:
            print("Plan de ejecución generado con éxito.")
            self.move_group.pick(self.box_name, grasp)
            self.move_group.stop()
        else:
            print("No se pudo generar un plan de ejecución. Verifica los parámetros de entrada.")

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
        
        self.openGripper(place_location.post_place_posture, gripper_max_opening)
        self.move_group.place(self.box_name, place_location)
        self.move_group.stop()

        return
    
    def place_2(self,place_pose):
        self.go_to_joint_state(final_position)
        self.open_gripper()
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

        return 

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
        
    def check_touch(self):
        print("Data:",self.max_dist)
        return self.max_dist.data > 9
    
    def callback_gelsightmini(self,dist) :
        self.max_dist = dist

    def move_gripper(self,pose):
        goal = franka_gripper.msg.MoveGoal()
        goal.width = pose
        goal.speed = 0.3    

        self.move_client.send_goal(goal)
        self.move_client.wait_for_result()
    
    def callback_arucos_position(self, data):
        self.arucos = []
        # Recupera la información de los arucos desde el mensaje de tipo String
        arucos_info = data.data.split(';')
        
        # Parsea la información de cada aruco y crea objetos PoseStamped
        for aruco_info in arucos_info:
            if aruco_info:  # Verifica si la cadena no está vacía
                aruco_data = aruco_info.split(':')
                if len(aruco_data) >= 4:  # Verifica si hay al menos 4 elementos (id, x, y, z)
                    pose_msg = PoseStamped()
                    pose_msg.header.frame_id = f"aruco_{aruco_data[0]}"
                    pose_msg.header.stamp = rospy.Time.now()
                    pose_msg.pose.position.x = float(aruco_data[1])
                    pose_msg.pose.position.y = float(aruco_data[2])
                    pose_msg.pose.position.z = float(aruco_data[3])    
                    pose_msg.pose.orientation.x = float(aruco_data[4])                
                    pose_msg.pose.orientation.y = float(aruco_data[5])                
                    pose_msg.pose.orientation.z = float(aruco_data[6])                
                    pose_msg.pose.orientation.w = float(aruco_data[7]) 

                    # Añade el objeto PoseStamped a la lista de arucos
                    self.arucos.append(pose_msg)

    def select_aruco(self):
        print("Seleccione un marcador ArUco:")
        for i, aruco_data in enumerate(self.arucos):
            print(f"{i+1}. ID del marcador: {aruco_data.header.frame_id.replace('aruco_', '')}")
            print(f"Posición (x, y, z): ({aruco_data.pose.position.x}, {aruco_data.pose.position.y}, {aruco_data.pose.position.z}, {aruco_data.pose.orientation.x}, {aruco_data.pose.orientation.y}, {aruco_data.pose.orientation.z},{aruco_data.pose.orientation.w})")

        while True:
            try:
                selection = int(input("Select an Arucon (Pulse 0 to go back): "))
                if selection == 0: return None
                aruco_position = self.arucos[selection - 1].pose
                aruco_id = aruco_data.header.frame_id.replace('aruco_', '')

                print(f"Ha seleccionado el marcador ArUco con ID {aruco_id}:")
                if selection != 1:
                    aruco_position.position.x = aruco_position.position.x + 0.03
                    aruco_position.position.y = aruco_position.position.y - 0.025
                aruco_position.position.z = 0.14362088204387037
                aruco_position.orientation.x = -0.9231143539216148
                aruco_position.orientation.y = -0.3840649074696301
                aruco_position.orientation.z = -0.01819345318830564
                aruco_position.orientation.w = 0.00479944739623474
                print(aruco_position)
                return aruco_position
            
            except (ValueError, IndexError):
                print("Opción no válida. Por favor, ingrese un número válido.")

def go_initial_position_and_open_gripper(MoveGroup):
    if initial_position is not None:
            MoveGroup.go_to_joint_state(initial_position)
    else:
        print("Initial position not set.")
    MoveGroup.open_gripper()

def go_object_position(MoveGroup):
    if object_position is None:
        print("Object position not set.")
        return
    MoveGroup.go_to_joint_state(object_position)

def go_final_position(MoveGroup):
    if final_position is None:
        print("Object position not set.")
        return
    MoveGroup.go_to_joint_state(final_position)

def pick_and_place(MoveGroup):
    if initial_position is None:
        print("Initial position not set.")
        return

    object_pose = MoveGroup.select_aruco()
    
    if object_pose == None:
        return
      
    a = MoveGroup.add_box()
    print("Object have been added: ", a)

    MoveGroup.open_gripper()
    MoveGroup.go_to_joint_state(initial_position)

    print("Calibrating")
    MoveGroup.callibration_client.send_goal(panda_demo.msg.GsGoal())
    print("Picking")
    MoveGroup.move_to_pick(object_pose)
    MoveGroup.callibration_client.wait_for_result()
    # Close the gripper progressively until the gellsight touches
    poses = numpy.linspace(0.08,0.0,100)
    for pose in poses:
        MoveGroup.move_gripper(pose)
        if MoveGroup.check_touch():
            print("Toutching ... width =",pose)
            break
    print("Picked")

    MoveGroup.go_to_joint_state(initial_position)

    print("Placing")
    MoveGroup.place(pose_place)
    #MoveGroup.place_2(pose_place)
    print("Placed")
    
    MoveGroup.go_to_joint_state(initial_position)
    MoveGroup.open_gripper()

    a = MoveGroup.remove_box()
    print("Object have been removed: ", a)

def main():
    try:
        #clear_screen()
        print("")
        print("----------------------------------------------------------")
        print("Welcome to the Movement-DPV, created by David Pacios Vázquez")
        print("----------------------------------------------------------")
        print("")
        MoveGroup = MoveGroupPythonInterfaceTutorial()
        while True:
            print("0. Initial position")
            print("1. Go to object position")
            print("3. Go to final posicion")
            print("5. Pick and Place with Arucos")
            print("6. Exit")
            
            choice = input("Enter your choice (0-6): ")
            
            if choice == '0':
                go_initial_position_and_open_gripper(MoveGroup)
                
            elif choice == '1':
                go_object_position(MoveGroup)
                
            elif choice == '3':
                go_final_position(MoveGroup)

            elif choice == '5':
                pick_and_place(MoveGroup)

            if choice == '6':
                go_initial_position_and_open_gripper(MoveGroup)
                break
            else:
                print("Invalid choice. Please enter a number between 0 and 5.")
        print("============ Movement-DPV ended!")
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()