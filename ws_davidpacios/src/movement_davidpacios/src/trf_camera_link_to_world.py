#!/usr/bin/env python3
import rospy
import tf2_ros
import geometry_msgs.msg
from std_msgs.msg import String
from tf import transformations
import numpy as np
id_aruco_calibration = 8

def main():
    rospy.init_node('trf_camera_link_to_world') 

    global broadcaster
    broadcaster = tf2_ros.TransformBroadcaster()  

    # Suscribirse al topic que contiene la información de la transformación
    print("============ Subscribing to topic /aruco_pose_frame ...")
    rospy.Subscriber("aruco_pose_frame", String, transform_callback)
    print("============ Using the aruco with id ", id_aruco_calibration ,"to create the frame")
    # Mantener el nodo ROS en ejecución
    rospy.spin()

def transform_callback(msg):
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

    arucos_data = msg.data[:-1]
    aruco_info = arucos_data.split(':')
    id_aruco, x, y, z, x_orientation, y_orientation, z_orientation, w_orientation = map(float, aruco_info)
    t = geometry_msgs.msg.TransformStamped()
    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "camera_link"
    t.child_frame_id = "aruco_frame"

    t.transform.translation.x = x
    t.transform.translation.y = y
    t.transform.translation.z = z
    t.transform.rotation.x = x_orientation
    t.transform.rotation.y = y_orientation
    t.transform.rotation.z = z_orientation
    t.transform.rotation.w = w_orientation

    broadcaster.sendTransform(t)

    # arucos_data = msg.data[:-1]
    # aruco_info = arucos_data.split(':')
    # id_aruco, x, y, z, x_orientation, y_orientation, z_orientation, w_orientation = map(float, aruco_info)

    # # Transformación entre aruco_frame y camera_link
    # transform_matrix_world_marker = transformations.concatenate_matrices(
    #     transformations.translation_matrix((0.08 , -0.06, 0.0)), # medio del aruco
    #     transformations.quaternion_matrix((0, 0, 0, 1))
    # )

    # # Definir las rotaciones deseadas
    # rot_z = transformations.quaternion_about_axis(90 * (np.pi / 180), (0, 0, 1))  # Rotación de 90 grados en el eje Z
    # rot_x = transformations.quaternion_about_axis(-90 * (np.pi / 180), (1, 0, 0))  # Rotación de -90 grados en el eje X

    # # Aplicar la rotación alrededor del eje Z primero
    # rotation_matrix_z = transformations.quaternion_matrix(rot_z)
    # transform_matrix_world_marker = np.dot(transform_matrix_world_marker, rotation_matrix_z)

    # # Aplicar la rotación alrededor del eje X luego
    # rotation_matrix_x = transformations.quaternion_matrix(rot_x)
    # transform_matrix_world_marker = np.dot(transform_matrix_world_marker, rotation_matrix_x)


    # transform_matrix_camera_marker = transformations.concatenate_matrices(
    #     transformations.translation_matrix((x, y, z)),
    #     transformations.quaternion_matrix((x_orientation, y_orientation, z_orientation, w_orientation))
    # )

    # transform_matrix_marker_camera = transformations.inverse_matrix(transform_matrix_camera_marker)

    # transform_matrix_world_camera = np.dot(transform_matrix_world_marker, transform_matrix_marker_camera)

    # transform_matrix_camera_world = transformations.inverse_matrix(transform_matrix_world_camera)
    # translation = transformations.translation_from_matrix(transform_matrix_camera_world)
    # rotation = transformations.quaternion_from_matrix(transform_matrix_camera_world)

    # t = geometry_msgs.msg.TransformStamped()
    # t.header.stamp = rospy.Time.now()
    # t.header.frame_id = "camera_link"
    # t.child_frame_id = "world"

    # # Asignar la traslación y la rotación al mensaje TransformStamped
    # t.transform.translation.x = translation[0]
    # t.transform.translation.y = translation[1]
    # t.transform.translation.z = translation[2]
    # t.transform.rotation.x = rotation[0]
    # t.transform.rotation.y = rotation[1]
    # t.transform.rotation.z = rotation[2]
    # t.transform.rotation.w = rotation[3]

    # broadcaster.sendTransform(t)





    

   

if __name__ == '__main__':
    main()
