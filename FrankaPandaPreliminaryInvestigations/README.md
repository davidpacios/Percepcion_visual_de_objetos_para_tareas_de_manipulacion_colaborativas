# Important description of the contents in this computer
This includes the works of Antoine Lucazeau (lucazeau@sigma-clermont.fr) from Mar-Sep 2023 and Francisco Elizondo (pacoelizondo@live.com.mx) from Sep-Dec 2023.

## ws_moveit
By Antoine  
Ros workspace to control the franka panda robot with automatic path generation using the astra camera. It includes demos that can be used during presentations, like the automatic pick and place auto_picker that identifies an object in space with the camera, generates a path for the arm and then it grasps the object, considering a succesful grasp when the gelsight detects a noticeable change in the image.

More information about the workspace on Franka_guide.txt file on desktop. More information about demos on Demo.txt file on desktop.

## ros_own_gripper
By Francisco  
Ros workspace to control a custom gripper with the dynamixel servo-motor and read traction (force/area) measurements using the gelsight tactile sensor for contact surface area and papillarray sensor for forces. Readme file inside the package. Research paper explaining surface area calculation and other details to be added. If you ever get here and the paper is not in the folder please contact me via email so I can send it to you.

## own_gripper_cpp
By Francisco  
C++ multi-thread program to control a custom gripper with the dynamixel sevo-motor via PID with current as control input and the papillarray sensor for force measurement as control output and feedback. Readme file
inside the folder.

## contactilesoftware
By contactile  
Papillarray C++ and ROS demos. It also includes the manuals that explain the hub communication protocol and memory adresses to access data.  
IMPORTANT NOTE: The sen0 port on the hub must always be connected to the same sensor, as it has a special firmware to self-calibrate that was recently flashed because of a bug that didn't let it start. The sensor is labeled as sen0 as well.


## gsrobotics
By gelsight  
Gelsight SDK that include python and ros examples for image and 3D reconstruction. More info at: https://github.com/gelsightinc/gsrobotics

## DynamixelSDK
Source code to install the servomotor's SDK, examples included.
More info at: https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/overview/
IMPORTANT NOTE: The motor's controller has to be connected directly to the PC and not an USB hub, otherwise it wont work.

## catkin_ws
By Francisco  
Test ros workspace to control the franka gripper (not the custom one) via PID force control using the papillarray for force measurement. Doesn't work because the franka gripper methods are unreliable and present several bugs. Not usable, not readable, didn't delete just in case.














