#!/usr/bin/env python3

import curses
from Robot import Robot
import panda_demo.msg

class Menu:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)  # Hide the cursor
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.current_row = 0
        self.main_menu_options = ["Start", "Options", "Exit"]
        self.options_menu_options = ["Reset to Initial Position", "Calibrate Camera", "Back to Main Menu"]
        self.robot = Robot(self)

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

    def print_centered_message(self, message):
        """Print a message in the center of the screen, handling multiple lines."""
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        
        lines = message.split('\n')
        for i, line in enumerate(lines):
            x = width // 2 - len(line) // 2
            y = height // 2 - len(lines) // 2 + i
            self.stdscr.addstr(y, x, line)
        
        self.stdscr.refresh()


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
        objects = self.robot.get_objects()
        self.select_objects_menu_options = [f"Object with Aruco ID-{i}" for i in objects.keys()] + ["Back to Main Menu"]
        choice = self.navigate_menu(self.select_objects_menu_options, "Select An Object")

        if choice == len(self.select_objects_menu_options) - 1:  # Back to Main Menu
            return    
        
        object_id = list(objects.keys())[choice]
        
        self.print_centered_message(f"Selected {object_id}")

        a = self.robot.add_box()
        self.print_centered_message(f"Object has been added: {a}")

        self.robot.go_to_joint_state(self.initial_position)
        self.robot.open_gripper()

        self.print_centered_message("Calibrating GelSightMini")

        self.robot.gelsight_mini_api.send_goal(panda_demo.msg.GsGoal())
        self.robot.gelsight_mini_api.wait_for_result()

        self.print_centered_message("Picking")

        self.robot.pick(self.robot.get_objects()[object_id].pose)

        self.robot.go_to_joint_state(self.initial_position)
        
        self.print_centered_message("Placing")

        self.robot.place(self.pose_place)

        self.robot.go_to_joint_state(self.initial_position)
        self.robot.open_gripper()

        a = self.robot.remove_box()
        self.print_centered_message(f"Object has been removed: {a}")

    def options_menu(self):
        """Display the options menu and handle user input."""
        while True:
            choice = self.navigate_menu(self.options_menu_options, "Options")

            if choice == 0:  # Reset to Initial Position
                self.print_centered_message("Resetting to initial position...")
                self.robot.go_to_joint_state(self.initial_position)
                self.robot.open_gripper()
            elif choice == 1:  # Calibrate Camera
                self.print_centered_message("Calibrating camera...")
                self.robot.request_calibration()
            elif choice == 2:  # Back to Main Menu
                break

def main(stdscr):
    menu = Menu(stdscr)
    menu.main_menu()

if __name__ == "__main__":
    curses.wrapper(main)
