#! /usr/bin/env python3
import panda_demo.msg
import curses
from Robot import Robot
import rospy

class Menu(object):
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)  # Hide the cursor
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.current_row = 0
        self.main_menu_options = ["Start", "Options", "Exit"]
        self.options_menu_options = ["Reset to Initial Position", "Calibrate Camera", "Manage Poses to Place", "Back to Main Menu"]
        self.robot = Robot(self)

    def print_menu(self, menu, title):
        """Print the menu options and title on the screen, handling multiple lines in the title."""
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        # Split the title into multiple lines
        title_lines = title.split('\n')
        
        # Calculate the starting y position for the title to be centered vertically
        title_start_y = 1
        
        # Print the title, handling multiple lines
        for i, title_line in enumerate(title_lines):
            title_x = width // 2 - len(title_line) // 2
            if 0 <= title_start_y + i < height and 0 <= title_x < width:
                self.stdscr.addstr(title_start_y + i, title_x, title_line, curses.A_BOLD)

        # Print the menu options
        for idx, row in enumerate(menu):
            x = width // 2 - len(row) // 2
            y = height // 2 - len(menu) // 2 + idx
            if 0 <= y < height and 0 <= x < width:
                if idx == self.current_row:
                    self.stdscr.attron(curses.color_pair(1))
                    self.stdscr.addstr(y, x, row)
                    self.stdscr.attroff(curses.color_pair(1))
                else:
                    self.stdscr.addstr(y, x, row)

        self.stdscr.refresh()

    def navigate_menu(self, menu, title):
        """Navigate the menu using arrow keys and Enter."""
        self.current_row = 0
        while True:
            if curses.is_term_resized(*self.stdscr.getmaxyx()):
                self.stdscr.clear()
                curses.resize_term(*self.stdscr.getmaxyx())
            self.print_menu(menu, title)
            key = self.stdscr.getch()

            if key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif key == curses.KEY_DOWN and self.current_row < len(menu) - 1:
                self.current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return self.current_row

    def print_centered_message(self, message):
        """Print a message in the center of the screen, handling multiple lines."""
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        
        lines = message.split('\n')
        for i, line in enumerate(lines):
            x = width // 2 - len(line) // 2
            y = height // 2 - len(lines) // 2 + i
            if 0 <= y < height and 0 <= x < width:
                self.stdscr.addstr(y, x, line)
        
        self.stdscr.refresh()

    def write_centered_message(self, prompt):
        """Display a prompt centered and allow user input."""
        height, width = self.stdscr.getmaxyx()
        
        # Clear screen and print prompt centered
        self.stdscr.clear()
        lines = prompt.split('\n')
        for i, line in enumerate(lines):
            x = width // 2 - len(line) // 2
            y = height // 2 - len(lines) // 2 + i
            if 0 <= y < height and 0 <= x < width:
                self.stdscr.addstr(y, x, line)
        
        # Enable echo and get user input
        curses.echo()
        input_y = height // 2 + len(lines) // 2 + 1
        input_x = width // 2
        if 0 <= input_y < height and 0 <= input_x < width:
            self.stdscr.move(input_y, input_x)
            self.stdscr.refresh()
            user_input = self.stdscr.getstr(input_y, input_x).decode('utf-8')
        else:
            user_input = ''
        curses.noecho()
        
        return user_input
    
    def string_info_pose(self,pose_name, object):
        """Return a formatted string with the information of the object."""
        position = object.position
        orientation = object.orientation
        return (
            f"Object ID: {pose_name}\n"
            f"Position: x={position.x:.3f}, y={position.y:.3f}, z={position.z:.3f}\n"
            f"Orientation: x={orientation.x:.3f}, y={orientation.y:.3f}, z={orientation.z:.3f}, w={orientation.w:.3f}"
        )

    def main_menu(self):
        """Display the main menu and handle user input."""
        while True:
            choice = self.navigate_menu(self.main_menu_options, "Pick and Place DPV")

            if choice == 0:  # Start
                self.execute_pick_and_place()
            elif choice == 1:  # Options
                self.options_menu()
            elif choice == 2:  # Exit
                break
    
    def select_place_pose(self):
        """Display the select place pose menu and handle user input."""
        place_poses = self.robot.get_place_poses()
        self.select_place_pose_menu_options = [f"Pose with name-{name}" for name in place_poses.keys()] + ["Back to Object Menu"]
        choice = self.navigate_menu(self.select_place_pose_menu_options, "Select A Place Pose")

        if choice == len(self.select_place_pose_menu_options) - 1:  # Back to Object Menu
            return None

        pose_name = list(place_poses.keys())[choice]

        self.print_centered_message(f"Selected Place Pose: {pose_name}")

        return place_poses.get(pose_name)

    def select_objects_menu(self):
        """Display the select objects menu and handle user input."""
        while True:
            objects = self.robot.get_objects()
            self.select_objects_menu_options = [f"Object with Aruco ID-{i}" for i in objects.keys()] + ["Back to Main Menu"]
            choice = self.navigate_menu(self.select_objects_menu_options, "Select An Object")

            if choice == len(self.select_objects_menu_options) - 1:  # Back to Main Menu
                return None

            object_id = list(objects.keys())[choice]

            self.print_centered_message(f"Selected {object_id}")

            selected_object = objects.get(object_id)
            
            place_pose = self.select_place_pose()
            if place_pose is not None:
                return selected_object, place_pose

            self.print_centered_message("Returning to object selection menu.")

    def execute_pick_and_place(self):
        """Main function to execute the pick and place operation."""
        while True:
            result = self.select_objects_menu()
            if result is None:
                return

            selected_object, place_pose = result

            a = self.robot.add_box(selected_object)
            self.print_centered_message(f"Object has been added: {a}")

            self.robot.go_to_inital_position()
            self.robot.open_gripper()

            # self.robot.prepare_gelsight_mini()            

            self.print_centered_message("Picking")

            self.robot.pick(selected_object.pose)

            self.robot.go_to_inital_position()

            self.print_centered_message("Placing")
            self.robot.place(place_pose)

            self.robot.go_to_inital_position()
            self.robot.open_gripper()

            a = self.robot.remove_box()
            self.print_centered_message(f"Object has been removed: {a}")
            rospy.sleep(2)
            break


    def menu_place_poses(self):
            """Allow the user to select an existing place pose or navigate to add a new one."""
            while True:
                # List existing poses
                self.select_pose_menu_options = list(self.robot.get_place_poses().keys()) + ["Add New Pose to Place", "Back to Options Menu"]
                choice = self.navigate_menu(self.select_pose_menu_options, "Manage Place Poses")

                if choice == len(self.select_pose_menu_options) - 1:  # Back to Options Menu
                    return
                elif choice == len(self.select_pose_menu_options) - 2:  # Add New Pose to Place
                    self.add_new_place_pose()
                else:
                    pose_name = self.select_pose_menu_options[choice]
                    self.selected_place_pose(pose_name)

    def add_new_place_pose(self):
        """Allow the user to add a new place pose."""
        while True:
            objects = self.robot.get_objects()
            self.select_objects_menu_options = [f"Object with Aruco ID-{i}" for i in objects.keys()] + ["Back to New Pose Menu"]
            obj_choice = self.navigate_menu(self.select_objects_menu_options, "Select An Object to Set New Place Pose")

            if obj_choice == len(self.select_objects_menu_options) - 1:  # Back to New Pose Menu
                return

            object_id = list(objects.keys())[obj_choice]
            pose_name = self.write_centered_message(f"Selected Object with Aruco ID-{object_id}\nEnter name for the new place pose:")

            self.robot.add_place_pose(pose_name, object_id)
            self.selected_place_pose(pose_name)  # Show the selected pose and options

    def selected_place_pose(self, pose_name):
        """Display the selected pose information and provide options to go back or delete the pose."""
        pose = self.robot.get_place_poses().get(pose_name)
        message = self.string_info_pose(pose_name, pose)
        options = ["Back", "Delete"]
        
        # Print pose information and options
        while True:
            choice = self.navigate_menu(options, message + "\n\nOptions:")
            
            if choice == 0:  # Back
                return
            elif choice == 1:  # Delete
                del self.robot.place_poses[pose_name]
                self.print_centered_message(f"Pose '{pose_name}' has been deleted.")
                self.stdscr.getch()
                return

    def options_menu(self):
        """Display the options menu and handle user input."""
        while True:
            choice = self.navigate_menu(self.options_menu_options, "Options")

            if choice == 0:  # Reset to Initial Position
                self.print_centered_message("Resetting to initial position...")
                self.robot.go_to_inital_position()
                self.robot.open_gripper()
            elif choice == 1:  # Calibrate Camera
                self.print_centered_message("Calibrating camera...")
                self.robot.request_calibration()
            elif choice == 2:  # New Pose to Place
                self.menu_place_poses()

            elif choice == 3:  # Back to Main Menu
                break

def main(stdscr):
    menu = Menu(stdscr)
    menu.main_menu()

if __name__ == "__main__":
    curses.wrapper(main)
