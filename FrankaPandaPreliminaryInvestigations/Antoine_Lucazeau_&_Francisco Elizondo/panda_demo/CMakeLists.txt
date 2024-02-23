cmake_minimum_required(VERSION 3.1.3)
project(panda_demo)

find_package(catkin REQUIRED
  COMPONENTS
    interactive_markers
    moveit_core
    moveit_ros_planning
    moveit_ros_planning_interface
    moveit_ros_perception
    rviz_visual_tools
    moveit_visual_tools
    pluginlib
    geometric_shapes
    pcl_ros
    pcl_conversions
    rosbag
    tf2_ros
    tf2_eigen
    tf2_geometry_msgs
    sensor_msgs
    std_msgs
    message_generation
    actionlib
    actionlib_msgs
)


find_package(Eigen3 REQUIRED)
find_package(Boost REQUIRED system filesystem date_time thread)

set(THIS_PACKAGE_INCLUDE_DIRS
  doc/interactivity/include
)

add_action_files(DIRECTORY action FILES Gs.action)

generate_messages(
  DEPENDENCIES
  actionlib_msgs
  std_msgs
)

catkin_package(
  LIBRARIES
  INCLUDE_DIRS
  CATKIN_DEPENDS
    moveit_core
    moveit_visual_tools
    moveit_ros_planning_interface
    interactive_markers
    tf2_geometry_msgs
    actionlib_msgs
    std_msgs
    message_runtime 
  DEPENDS
    EIGEN3
)

###########
## Build ##
###########

include_directories(${THIS_PACKAGE_INCLUDE_DIRS})
include_directories(SYSTEM ${catkin_INCLUDE_DIRS} ${Boost_INCLUDE_DIR} ${EIGEN3_INCLUDE_DIRS})

catkin_install_python(PROGRAMS
  src/pick_and_place_python.py
  src/camera_position_calibrator.py
  src/auto_picker.py
  src/gripper_control.py
  src/gripper_test.py
  src/gs_screenshot.py
  src/gs_action_server.py
  src/callibration_client_test.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

add_executable(pcl_filter src/pcl_filter.cpp)
add_executable(euclidean_cluster src/euclidean_cluster.cpp)

target_link_libraries(pcl_filter ${catkin_LIBRARIES})
target_link_libraries(euclidean_cluster ${catkin_LIBRARIES})
install(DIRECTORY launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})