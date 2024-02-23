# Install script for directory: /home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
        file(MAKE_DIRECTORY "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
      endif()
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin")
        file(WRITE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin" "")
      endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/install/_setup_util.py")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/install" TYPE PROGRAM FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/build/astra_camera/catkin_generated/installspace/_setup_util.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/install/env.sh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/install" TYPE PROGRAM FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/build/astra_camera/catkin_generated/installspace/env.sh")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/install/setup.bash;/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/install/local_setup.bash")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/install" TYPE FILE FILES
    "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/build/astra_camera/catkin_generated/installspace/setup.bash"
    "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/build/astra_camera/catkin_generated/installspace/local_setup.bash"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/install/setup.sh;/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/install/local_setup.sh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/install" TYPE FILE FILES
    "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/build/astra_camera/catkin_generated/installspace/setup.sh"
    "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/build/astra_camera/catkin_generated/installspace/local_setup.sh"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/install/setup.zsh;/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/install/local_setup.zsh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/install" TYPE FILE FILES
    "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/build/astra_camera/catkin_generated/installspace/setup.zsh"
    "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/build/astra_camera/catkin_generated/installspace/local_setup.zsh"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/install/.rosinstall")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/install" TYPE FILE FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/build/astra_camera/catkin_generated/installspace/.rosinstall")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/astra_camera" TYPE FILE FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/devel/.private/astra_camera/include/astra_camera/AstraConfig.h")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages/astra_camera" TYPE FILE FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/devel/.private/astra_camera/lib/python3/dist-packages/astra_camera/__init__.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/devel/.private/astra_camera/lib/python3/dist-packages/astra_camera/cfg")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages/astra_camera" TYPE DIRECTORY FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/devel/.private/astra_camera/lib/python3/dist-packages/astra_camera/cfg")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/astra_camera/msg" TYPE FILE FILES
    "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/msg/DeviceInfo.msg"
    "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/msg/Extrinsics.msg"
    "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/msg/Metadata.msg"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/astra_camera/srv" TYPE FILE FILES
    "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/srv/GetBool.srv"
    "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/srv/GetCameraInfo.srv"
    "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/srv/GetCameraParams.srv"
    "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/srv/GetDeviceInfo.srv"
    "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/srv/GetDouble.srv"
    "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/srv/GetInt32.srv"
    "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/srv/GetString.srv"
    "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/srv/SetInt32.srv"
    "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/srv/SetString.srv"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/astra_camera/cmake" TYPE FILE FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/build/astra_camera/catkin_generated/installspace/astra_camera-msg-paths.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/devel/.private/astra_camera/include/astra_camera")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/devel/.private/astra_camera/share/roseus/ros/astra_camera")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/devel/.private/astra_camera/share/common-lisp/ros/astra_camera")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/devel/.private/astra_camera/share/gennodejs/ros/astra_camera")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/devel/.private/astra_camera/lib/python3/dist-packages/astra_camera")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/devel/.private/astra_camera/lib/python3/dist-packages/astra_camera")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/build/astra_camera/catkin_generated/installspace/astra_camera.pc")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/astra_camera/cmake" TYPE FILE FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/build/astra_camera/catkin_generated/installspace/astra_camera-msg-extras.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/astra_camera/cmake" TYPE FILE FILES
    "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/build/astra_camera/catkin_generated/installspace/astra_cameraConfig.cmake"
    "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/build/astra_camera/catkin_generated/installspace/astra_cameraConfig-version.cmake"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/astra_camera" TYPE FILE FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/package.xml")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libastra_camera.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libastra_camera.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libastra_camera.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/devel/.private/astra_camera/lib/libastra_camera.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libastra_camera.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libastra_camera.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libastra_camera.so"
         OLD_RPATH "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/include/openni2_redist/x64:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_calib3d:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_core:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_dnn:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_features2d:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_flann:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_highgui:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_imgcodecs:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_imgproc:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_ml:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_objdetect:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_photo:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_stitching:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_video:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_videoio:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_aruco:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_bgsegm:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_bioinspired:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_ccalib:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_datasets:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_dnn_objdetect:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_dnn_superres:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_dpm:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_face:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_freetype:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_fuzzy:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_hdf:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_hfs:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_img_hash:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_line_descriptor:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_optflow:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_phase_unwrapping:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_plot:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_quality:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_reg:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_rgbd:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_saliency:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_shape:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_stereo:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_structured_light:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_superres:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_surface_matching:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_text:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_tracking:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_videostab:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_viz:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_ximgproc:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_xobjdetect:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_xphoto:/opt/ros/noetic/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libastra_camera.so")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/astra_camera/astra_camera_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/astra_camera/astra_camera_node")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/astra_camera/astra_camera_node"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/astra_camera" TYPE EXECUTABLE FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/devel/.private/astra_camera/lib/astra_camera/astra_camera_node")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/astra_camera/astra_camera_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/astra_camera/astra_camera_node")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/astra_camera/astra_camera_node"
         OLD_RPATH "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/include/openni2_redist/x64:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_calib3d:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_core:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_dnn:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_features2d:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_flann:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_highgui:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_imgcodecs:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_imgproc:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_ml:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_objdetect:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_photo:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_stitching:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_video:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_videoio:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_aruco:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_bgsegm:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_bioinspired:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_ccalib:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_datasets:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_dnn_objdetect:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_dnn_superres:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_dpm:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_face:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_freetype:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_fuzzy:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_hdf:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_hfs:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_img_hash:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_line_descriptor:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_optflow:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_phase_unwrapping:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_plot:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_quality:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_reg:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_rgbd:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_saliency:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_shape:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_stereo:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_structured_light:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_superres:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_surface_matching:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_text:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_tracking:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_videostab:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_viz:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_ximgproc:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_xobjdetect:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_xphoto:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/devel/.private/astra_camera/lib:/opt/ros/noetic/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/astra_camera/astra_camera_node")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/astra_camera/list_devices_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/astra_camera/list_devices_node")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/astra_camera/list_devices_node"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/astra_camera" TYPE EXECUTABLE FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/devel/.private/astra_camera/lib/astra_camera/list_devices_node")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/astra_camera/list_devices_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/astra_camera/list_devices_node")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/astra_camera/list_devices_node"
         OLD_RPATH "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/include/openni2_redist/x64:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_calib3d:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_core:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_dnn:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_features2d:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_flann:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_highgui:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_imgcodecs:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_imgproc:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_ml:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_objdetect:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_photo:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_stitching:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_video:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_videoio:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_aruco:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_bgsegm:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_bioinspired:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_ccalib:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_datasets:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_dnn_objdetect:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_dnn_superres:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_dpm:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_face:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_freetype:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_fuzzy:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_hdf:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_hfs:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_img_hash:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_line_descriptor:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_optflow:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_phase_unwrapping:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_plot:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_quality:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_reg:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_rgbd:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_saliency:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_shape:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_stereo:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_structured_light:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_superres:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_surface_matching:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_text:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_tracking:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_videostab:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_viz:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_ximgproc:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_xobjdetect:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/opencv_xphoto:/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/devel/.private/astra_camera/lib:/opt/ros/noetic/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/astra_camera/list_devices_node")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE FILE FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/include/openni2_redist/x64/libOpenNI2.so")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/" TYPE DIRECTORY FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/include/openni2_redist/x64/OpenNI2")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/astra_camera/" TYPE DIRECTORY FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/include")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/astra_camera" TYPE FILE FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/56-orbbec-usb.rules")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/astra_camera" TYPE DIRECTORY FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/scripts")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/astra_camera" TYPE FILE FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/56-orbbec-usb.rules")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/astra_camera" TYPE DIRECTORY FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/scripts")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/astra_camera" TYPE DIRECTORY FILES "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/ros_astra_camera/launch")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/build/astra_camera/gtest/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/build/astra_camera/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
