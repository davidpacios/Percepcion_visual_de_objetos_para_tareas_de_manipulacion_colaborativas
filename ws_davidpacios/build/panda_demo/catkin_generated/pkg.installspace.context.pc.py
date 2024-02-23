# generated from catkin/cmake/template/pkg.context.pc.in
CATKIN_PACKAGE_PREFIX = ""
PROJECT_PKG_CONFIG_INCLUDE_DIRS = "${prefix}/include;/usr/include/eigen3".split(';') if "${prefix}/include;/usr/include/eigen3" != "" else []
PROJECT_CATKIN_DEPENDS = "moveit_core;moveit_visual_tools;moveit_ros_planning_interface;interactive_markers;tf2_geometry_msgs;actionlib_msgs;std_msgs;message_runtime".replace(';', ' ')
PKG_CONFIG_LIBRARIES_WITH_PREFIX = "-lfranka_example_controllers".split(';') if "-lfranka_example_controllers" != "" else []
PROJECT_NAME = "panda_demo"
PROJECT_SPACE_DIR = "/home/frankaros/ws_davidpacios/install"
PROJECT_VERSION = "0.1.0"
