# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.27

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /home/frankaros/.local/lib/python3.8/site-packages/cmake/data/bin/cmake

# The command to remove a file.
RM = /home/frankaros/.local/lib/python3.8/site-packages/cmake/data/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/frankaros/ws_davidpacios/src/geometric_shapes

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/frankaros/ws_davidpacios/build/geometric_shapes

# Include any dependencies generated for this target.
include test/CMakeFiles/test_bounding_box.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include test/CMakeFiles/test_bounding_box.dir/compiler_depend.make

# Include the progress variables for this target.
include test/CMakeFiles/test_bounding_box.dir/progress.make

# Include the compile flags for this target's objects.
include test/CMakeFiles/test_bounding_box.dir/flags.make

test/CMakeFiles/test_bounding_box.dir/test_bounding_box.cpp.o: test/CMakeFiles/test_bounding_box.dir/flags.make
test/CMakeFiles/test_bounding_box.dir/test_bounding_box.cpp.o: /home/frankaros/ws_davidpacios/src/geometric_shapes/test/test_bounding_box.cpp
test/CMakeFiles/test_bounding_box.dir/test_bounding_box.cpp.o: test/CMakeFiles/test_bounding_box.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/frankaros/ws_davidpacios/build/geometric_shapes/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object test/CMakeFiles/test_bounding_box.dir/test_bounding_box.cpp.o"
	cd /home/frankaros/ws_davidpacios/build/geometric_shapes/test && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT test/CMakeFiles/test_bounding_box.dir/test_bounding_box.cpp.o -MF CMakeFiles/test_bounding_box.dir/test_bounding_box.cpp.o.d -o CMakeFiles/test_bounding_box.dir/test_bounding_box.cpp.o -c /home/frankaros/ws_davidpacios/src/geometric_shapes/test/test_bounding_box.cpp

test/CMakeFiles/test_bounding_box.dir/test_bounding_box.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/test_bounding_box.dir/test_bounding_box.cpp.i"
	cd /home/frankaros/ws_davidpacios/build/geometric_shapes/test && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/frankaros/ws_davidpacios/src/geometric_shapes/test/test_bounding_box.cpp > CMakeFiles/test_bounding_box.dir/test_bounding_box.cpp.i

test/CMakeFiles/test_bounding_box.dir/test_bounding_box.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/test_bounding_box.dir/test_bounding_box.cpp.s"
	cd /home/frankaros/ws_davidpacios/build/geometric_shapes/test && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/frankaros/ws_davidpacios/src/geometric_shapes/test/test_bounding_box.cpp -o CMakeFiles/test_bounding_box.dir/test_bounding_box.cpp.s

# Object files for target test_bounding_box
test_bounding_box_OBJECTS = \
"CMakeFiles/test_bounding_box.dir/test_bounding_box.cpp.o"

# External object files for target test_bounding_box
test_bounding_box_EXTERNAL_OBJECTS =

/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: test/CMakeFiles/test_bounding_box.dir/test_bounding_box.cpp.o
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: test/CMakeFiles/test_bounding_box.dir/build.make
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: gtest/lib/libgtest.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/libgeometric_shapes.so.0.7.5
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /opt/ros/noetic/lib/librandom_numbers.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /opt/ros/noetic/lib/libresource_retriever.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /opt/ros/noetic/lib/libroscpp_serialization.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /opt/ros/noetic/lib/librostime.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /usr/lib/x86_64-linux-gnu/libboost_date_time.so.1.71.0
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /opt/ros/noetic/lib/libcpp_common.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /usr/lib/x86_64-linux-gnu/libboost_system.so.1.71.0
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /usr/lib/x86_64-linux-gnu/libboost_thread.so.1.71.0
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /usr/lib/x86_64-linux-gnu/libconsole_bridge.so.0.4
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /usr/lib/x86_64-linux-gnu/libboost_system.so.1.71.0
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.71.0
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /opt/ros/noetic/lib/x86_64-linux-gnu/libfcl.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /usr/lib/x86_64-linux-gnu/libccd.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /usr/lib/x86_64-linux-gnu/libm.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /opt/ros/noetic/lib/liboctomap.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /opt/ros/noetic/lib/liboctomath.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /usr/lib/x86_64-linux-gnu/libassimp.so.5
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /usr/lib/x86_64-linux-gnu/libqhull_r.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /opt/ros/noetic/lib/librandom_numbers.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /opt/ros/noetic/lib/libresource_retriever.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /opt/ros/noetic/lib/libroscpp_serialization.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /opt/ros/noetic/lib/librostime.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /usr/lib/x86_64-linux-gnu/libboost_date_time.so.1.71.0
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /opt/ros/noetic/lib/libcpp_common.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /usr/lib/x86_64-linux-gnu/libboost_system.so.1.71.0
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /usr/lib/x86_64-linux-gnu/libboost_thread.so.1.71.0
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /usr/lib/x86_64-linux-gnu/libconsole_bridge.so.0.4
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /opt/ros/noetic/lib/x86_64-linux-gnu/libfcl.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /usr/lib/x86_64-linux-gnu/libccd.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /usr/lib/x86_64-linux-gnu/libm.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /opt/ros/noetic/lib/liboctomap.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /opt/ros/noetic/lib/liboctomath.so
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: /usr/lib/x86_64-linux-gnu/libconsole_bridge.so.0.4
/home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box: test/CMakeFiles/test_bounding_box.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/home/frankaros/ws_davidpacios/build/geometric_shapes/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable /home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box"
	cd /home/frankaros/ws_davidpacios/build/geometric_shapes/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/test_bounding_box.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
test/CMakeFiles/test_bounding_box.dir/build: /home/frankaros/ws_davidpacios/devel/.private/geometric_shapes/lib/geometric_shapes/test_bounding_box
.PHONY : test/CMakeFiles/test_bounding_box.dir/build

test/CMakeFiles/test_bounding_box.dir/clean:
	cd /home/frankaros/ws_davidpacios/build/geometric_shapes/test && $(CMAKE_COMMAND) -P CMakeFiles/test_bounding_box.dir/cmake_clean.cmake
.PHONY : test/CMakeFiles/test_bounding_box.dir/clean

test/CMakeFiles/test_bounding_box.dir/depend:
	cd /home/frankaros/ws_davidpacios/build/geometric_shapes && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/frankaros/ws_davidpacios/src/geometric_shapes /home/frankaros/ws_davidpacios/src/geometric_shapes/test /home/frankaros/ws_davidpacios/build/geometric_shapes /home/frankaros/ws_davidpacios/build/geometric_shapes/test /home/frankaros/ws_davidpacios/build/geometric_shapes/test/CMakeFiles/test_bounding_box.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : test/CMakeFiles/test_bounding_box.dir/depend
