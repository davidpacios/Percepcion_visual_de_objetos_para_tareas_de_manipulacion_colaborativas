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
from std_msgs.msg import String, Bool
from geometry_msgs.msg import PoseStamped
import curses

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
a = False

gripper_max_opening = 0.04  # adjust as needed

class Robot(object):
    def __init__(self):
        super(Robot, self).__init__()

        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node("robot")

        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()
        self.move_group = moveit_commander.MoveGroupCommander("panda_arm")
        self.hand_group = moveit_commander.MoveGroupCommander("panda_hand")
        self.planning_frame = self.move_group.get_planning_frame()
        self.eef_link = self.move_group.get_end_effector_link()
        self.group_names = self.robot.get_group_names()

        # Misc variables
        self.box_name = "box"
        self.objects = None
        self.pixel_intensity_difference = None
        self.camera_calibration = False

        self.franka_gripper_api = actionlib.SimpleActionClient('franka_gripper/move', franka_gripper.msg.MoveAction)
        self.franka_gripper_api.wait_for_server()

        self.gelsight_mini_api = actionlib.SimpleActionClient('gelsight_mini_action', panda_demo.msg.GsAction)
        self.gelsight_mini_api.wait_for_server()

        # Create a publisher for request calibration
        self.camera_calibration_pub = rospy.Publisher("request_calibration", Bool, queue_size=10)


        rospy.Subscriber("gelsight_pixel_intensity_difference", Float32, self.callback_gelsightmini)
        while self.pixel_intensity_difference == None and not rospy.is_shutdown():
            rospy.sleep(0.1)

        rospy.Subscriber("calibration_done", Bool, self.callback_camera_calibration_done)
        while not self.camera_calibration and not rospy.is_shutdown():
            self.camera_calibration_pub.publish(True)
            rospy.sleep(6)

        
        rospy.Subscriber("aruco_poses_trf", String, self.callback_arucos_position)
        while not self.objects and not rospy.is_shutdown():
            rospy.sleep(0.1)

    def get_current_pose(self):
        return self.move_group.get_current_pose().pose
    
    def go_to_joint_state(self, j):
        joint_goal = self.move_group.get_current_joint_values()
        joint_goal[0] = j[0]
        joint_goal[1] = j[1]
        joint_goal[2] = j[2]
        joint_goal[3] = j[3]
        joint_goal[4] = j[4]
        joint_goal[5] = j[5]
        joint_goal[6] = j[6]

        self.move_group.go(joint_goal, wait=True)
        self.move_group.stop()
        return 

    def openGripper(self, posture, opening):
        posture.joint_names = ["panda_finger_joint1","panda_finger_joint2"]

        posture.points.append(trajectory_msgs.msg.JointTrajectoryPoint())
        posture.points[0].positions = [opening,opening]
        return

    def closeGripper(self, posture, closing):
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
    
    def pick(self,grasp_pose):
        self.move_to_pick(grasp_pose)
        poses = numpy.linspace(0.08, 0.0, 100)
        for pose in poses:
            self.move_gripper(pose)
            #print("Data:",self.pixel_intensity_difference)
            if self.pixel_intensity_difference.data > 11:#diferencia máxima de intensidad de píxeles que se podría esperar en la imagen
                #print("Touching... width =", pose)
                break
        return
    
    def move_gripper(self,pose):
        goal = franka_gripper.msg.MoveGoal()
        goal.width = pose
        goal.speed = 0.3    

        self.franka_gripper_api.send_goal(goal)
        self.franka_gripper_api.wait_for_result()

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
        self.closeGripper(grasp.grasp_posture, gripper_max_opening)

        self.move_group.pick(self.box_name, grasp)
        self.move_group.stop()

        return

    def place(self, place_pose):
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
    
    def callback_camera_calibration_done(self,data):
        self.camera_calibration = data

    def callback_gelsightmini(self,dist) :
        self.pixel_intensity_difference = dist

    def callback_arucos_position(self, data):
        self.objects = {}
        # Recupera la información de los objects desde el mensaje de tipo String
        arucos_info = data.data.split(';')
        
        # Parsea la información de cada aruco y crea objetos PoseStamped
        for aruco_info in arucos_info:
            if aruco_info:  # Verifica si la cadena no está vacía
                aruco_data = aruco_info.split(':')
                if len(aruco_data) >= 4:  # Verifica si hay al menos 4 elementos (id, x, y, z)
                    # Convertir el ID del Aruco a un número decimal
                    aruco_id_decimal = float(aruco_data[0])
                    # Convertir el número decimal a un número entero
                    aruco_id_entero = int(aruco_id_decimal)

                    pose_msg = PoseStamped()
                    pose_msg.header.frame_id = f"aruco_{aruco_id_entero}"
                    pose_msg.header.stamp = rospy.Time.now()
                    pose_msg.pose.position.x = float(aruco_data[1]) + 0.03
                    pose_msg.pose.position.y = float(aruco_data[2])
                    pose_msg.pose.position.z = 0.14 #float(aruco_data[3])    
                    pose_msg.pose.orientation.x = -0.9231143539216148 #float(aruco_data[4])                
                    pose_msg.pose.orientation.y = -0.3840649074696301 #float(aruco_data[5])                
                    pose_msg.pose.orientation.z = -0.01819345318830564 #float(aruco_data[6])                
                    pose_msg.pose.orientation.w = 0.00479944739623474 #float(aruco_data[7]) 

                    # Almacena el objeto PoseStamped en el diccionario usando el ID del Aruco como clave
                    self.objects[aruco_id_entero] = pose_msg

    def select_aruco(self):
        print("Seleccione un marcador ArUco:")
        for aruco_id, aruco_data in self.objects.items():
            print(f"ID del marcador: {aruco_id}")
            print(f"Posición (x, y, z): ({aruco_data.pose.position.x}, {aruco_data.pose.position.y}, {aruco_data.pose.position.z}, {aruco_data.pose.orientation.x}, {aruco_data.pose.orientation.y}, {aruco_data.pose.orientation.z},{aruco_data.pose.orientation.w})")

        while True:
            try:
                selection = int(input("Introduce el ID del ArUco que quieres coger (Pulsa 0 para volver): "))
                if selection == 0:
                    return None
                aruco_data = self.objects.get(selection)
                if aruco_data is None:
                    print("ID de ArUco no válido. Por favor, introduce un ID válido.")
                else:
                    aruco_position = aruco_data.pose
                    print(f"Has seleccionado el marcador ArUco con ID {selection}:")
                    print(aruco_position)
                    return aruco_position
                
            except ValueError:
                print("Entrada no válida. Por favor, introduce un número entero.")


    def get_objects(self):
        return self.objects
    
    def request_calibration(self):
        self.camera_calibration = False
        rospy.Subscriber("calibration_done", Bool, self.callback_camera_calibration_done)
        while not self.camera_calibration and not rospy.is_shutdown():
            self.camera_calibration_pub.publish(True)
            rospy.sleep(6)

# def go_initial_position_and_open_gripper(MoveGroup):
#     if initial_position is not None:
#             MoveGroup.go_to_joint_state(initial_position)
#     else:
#         print("Initial position not set.")
#     MoveGroup.open_gripper()

# def go_object_position(MoveGroup):
#     if object_position is None:
#         print("Object position not set.")
#         return
#     MoveGroup.go_to_joint_state(object_position)

# def go_final_position(MoveGroup):
#     if final_position is None:
#         print("Object position not set.")
#         return
#     MoveGroup.go_to_joint_state(final_position)

# def pick_and_place(MoveGroup):
#     if initial_position is None:
#         print("Initial position not set.")
#         return

#     object_pose = MoveGroup.select_aruco()
    
#     if object_pose == None:
#         return

#     a = MoveGroup.add_box()
#     print("Object has been added: ", a)

#     MoveGroup.open_gripper()
#     MoveGroup.go_to_joint_state(initial_position)

#     print("Calibrating")
#     MoveGroup.gelsight_mini_api.send_goal(panda_demo.msg.GsGoal())
#     MoveGroup.gelsight_mini_api.wait_for_result()

#     print("Picking")
#     MoveGroup.pick(object_pose)
#     print("Picked")

#     MoveGroup.go_to_joint_state(initial_position)

#     print("Placing")
#     # Use the fixed place_pose
#     MoveGroup.place(pose_place)
#     print("Placed")

#     MoveGroup.go_to_joint_state(initial_position)
#     MoveGroup.open_gripper()

#     a = MoveGroup.remove_box()
#     print("Object has been removed: ", a)

# def main():
#     global a
#     try:
#         MoveGroup = Robot()
#         while True:
#             print("")
#             print("----------------------------------------------------------")
#             print("Welcome to the Pick and Place: DPV")
#             print("----------------------------------------------------------")
#             print("")
#             print("1. Start")
#             print("2. Options")
#             print("3. Exit")
            
#             choice = input("Enter your choice (1-3): ")
            
#             if choice == '1':
#                 pick_and_place(MoveGroup)
#             elif choice == '2':
#                 MoveGroup.request_calibration()
#                 print("Options")
                
#             elif choice == '3':
#                 go_initial_position_and_open_gripper(MoveGroup)
#                 break
#             else:
#                 print("Invalid choice. Please enter a number between 0 and 5.")
#     except KeyboardInterrupt:
#         return

# if __name__ == "__main__":
#     main()

    

class Menu:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)  # Hide the cursor
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.current_row = 0
        self.main_menu_options = ["Start", "Options", "Exit"]
        self.options_menu_options = ["Reset to Initial Position", "Calibrate Camera", "Back to Main Menu"]
        self.robot = Robot()

    def print_menu(self, menu, title):
        """Print the menu options and title on the screen."""
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        # Print the title
        title_x = width // 2 - len(title) // 2
        self.stdscr.addstr(1, title_x, title, curses.A_BOLD)

        # Print the menu options
        for idx, row in enumerate(menu):
            x = width // 2 - len(row) // 2
            y = height // 2 - len(menu) // 2 + idx
            if idx == self.current_row:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, row)

        self.stdscr.refresh()

    def navigate_menu(self, menu, title):
        """Navigate the menu using arrow keys and Enter."""
        while True:
            self.print_menu(menu, title)
            key = self.stdscr.getch()

            if key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif key == curses.KEY_DOWN and self.current_row < len(menu) - 1:
                self.current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return self.current_row

    def main_menu(self):
        """Display the main menu and handle user input."""
        while True:
            choice = self.navigate_menu(self.main_menu_options, "Pick and Place DPV")

            if choice == 0:  # Start
                self.select_objects_menu()
            elif choice == 1:  # Options
                self.options_menu()
            elif choice == 2:  # Exit
                break

    def select_objects_menu(self):
        """Display the select objects menu and handle user input."""
        self.select_objects_menu_options = [f"Object with Aruco ID-{i}" for i in self.robot.get_objects().keys()] + ["Back to Main Menu"]
        while True:
            choice = self.navigate_menu(self.select_objects_menu_options, "Select An Object")

            if choice == len(self.select_objects_menu_options) - 1:  # Back to Main Menu
                break
            else:
                object_id = list(self.robot.get_objects().keys())[choice]
                
                self.stdscr.clear()
                self.stdscr.addstr(0, 0, f"Selected {object_id}")
                self.stdscr.refresh()

                a = self.robot.add_box()
                self.stdscr.clear()
                self.stdscr.addstr(0, 0, f"Object has been added: {a}")
                self.stdscr.refresh()

                self.robot.go_to_joint_state(initial_position)
                self.robot.open_gripper()

                self.stdscr.clear()
                self.stdscr.addstr(0, 0, f"Calibrating GelSightMini")
                self.stdscr.refresh()

                self.robot.gelsight_mini_api.send_goal(panda_demo.msg.GsGoal())
                self.robot.gelsight_mini_api.wait_for_result()

                self.stdscr.clear()
                self.stdscr.addstr(0, 0, f"Picking")
                self.stdscr.refresh()

                self.robot.pick(self.robot.get_objects()[object_id].pose)

                self.stdscr.clear()
                self.robot.go_to_joint_state(initial_position)
                
                self.stdscr.addstr(0, 0, f"Placing")
                self.stdscr.refresh()

                self.robot.place(pose_place)

                self.stdscr.clear()
                self.robot.go_to_joint_state(initial_position)
                self.robot.open_gripper()

                a = self.robot.remove_box()
                self.stdscr.clear()
                self.stdscr.addstr(0, 0, f"Object has been removed: {a}")
                self.stdscr.refresh()
                self.stdscr.getch()



    def options_menu(self):
        """Display the options menu and handle user input."""
        while True:
            choice = self.navigate_menu(self.options_menu_options, "Options")

            if choice == 0:  # Reset to Initial Position
                self.stdscr.addstr(0, 0, "Resetting to initial position...")
                self.stdscr.refresh()
                self.robot.go_to_joint_state(initial_position)
                self.robot.open_gripper()
                self.stdscr.getch()
            elif choice == 1:  # Calibrate Camera
                self.stdscr.addstr(0, 0, "Calibrating camera...")
                self.stdscr.refresh()
                self.robot.request_calibration()
                self.stdscr.getch()
            elif choice == 2:  # Back to Main Menu
                break

def main(stdscr):
    menu = Menu(stdscr)
    menu.main_menu()

if __name__ == "__main__":
    curses.wrapper(main)
