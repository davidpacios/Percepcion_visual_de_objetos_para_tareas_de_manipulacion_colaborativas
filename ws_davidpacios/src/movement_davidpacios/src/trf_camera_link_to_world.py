#!/usr/bin/env python3
import rospy
import tf2_ros
import geometry_msgs.msg
from std_msgs.msg import String
from tf import transformations
import numpy as np
from collections import Counter

id_aruco_calibration = 8

def main():
    global broadcaster

    rospy.init_node('trf_camera_link_to_world') 
    broadcaster = tf2_ros.TransformBroadcaster()  

    # Suscribirse al topic que contiene la información de la transformación
    print("============ Subscribing to topic /aruco_pose_frame ...")
    rospy.Subscriber("aruco_pose_frame", String, transform_callback)
    print("============ Using the aruco with id ", id_aruco_calibration ,"to create the frame")
    # Mantener el nodo ROS en ejecución
    rospy.spin()

def transform_callback(msg):
    print(msg)
    # Obtener las posiciones y orientaciones de la aruco
    arucos_data = msg.data[:-1]
    aruco_info = arucos_data.split(':')
    id_aruco, x, y, z, x_orientation, y_orientation, z_orientation, w_orientation = map(float, aruco_info)

    t_nueva = geometry_msgs.msg.TransformStamped()
    t_nueva.header.stamp = rospy.Time.now()
    t_nueva.header.frame_id = "aruco_frame"
    t_nueva.child_frame_id = "world"
    t_nueva.transform.translation.x = 0.08
    t_nueva.transform.translation.y = -0.06
    t_nueva.transform.translation.z = 0.00
    t_nueva.transform.rotation.x = 0
    t_nueva.transform.rotation.y = 0
    t_nueva.transform.rotation.z = 0
    t_nueva.transform.rotation.w = 1

    # Convertir la rotación inicial a cuaternión
    quat = (
        t_nueva.transform.rotation.x,
        t_nueva.transform.rotation.y,
        t_nueva.transform.rotation.z,
        t_nueva.transform.rotation.w
    )

    rot_desired = transformations.quaternion_about_axis(90 * (3.14159 / 180), (0, 0, 1))  # Convertir grados a radianes
    quat_rotated = transformations.quaternion_multiply(quat, rot_desired)
    rot_desired = transformations.quaternion_about_axis(-90 * (3.14159 / 180), (1, 0, 0))
    quat_rotated = transformations.quaternion_multiply(quat_rotated, rot_desired)

    t_nueva.transform.rotation.x = quat_rotated[0]
    t_nueva.transform.rotation.y = quat_rotated[1]
    t_nueva.transform.rotation.z = quat_rotated[2]
    t_nueva.transform.rotation.w = quat_rotated[3]

    broadcaster.sendTransform(t_nueva)

    # Crear la transformación con la posición y orientación más repetidas
    t_camera_marker = geometry_msgs.msg.TransformStamped()
    t_camera_marker.header.stamp = rospy.Time.now()
    t_camera_marker.header.frame_id = "camera_link"
    t_camera_marker.child_frame_id = "aruco_frame"
    t_camera_marker.transform.translation.x = x
    t_camera_marker.transform.translation.y = y
    t_camera_marker.transform.translation.z = z
    t_camera_marker.transform.rotation.x = x_orientation
    t_camera_marker.transform.rotation.y = y_orientation
    t_camera_marker.transform.rotation.z = z_orientation
    t_camera_marker.transform.rotation.w = w_orientation

    broadcaster.sendTransform(t_camera_marker)

if __name__ == '__main__':
    main()
