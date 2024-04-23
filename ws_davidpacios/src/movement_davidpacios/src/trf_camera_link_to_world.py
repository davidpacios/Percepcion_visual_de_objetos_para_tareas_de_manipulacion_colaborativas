#!/usr/bin/env python3
import rospy
import tf2_ros
import geometry_msgs.msg
from std_msgs.msg import String
from tf import transformations
import numpy as np
from collections import Counter


id_aruco_calibration = 8
callback_counter = -1
orientations_array = []
positions_array = []

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
    global callback_counter
    global positions_array
    global orientations_array

    # Incrementar el contador de llamadas de callback
    callback_counter += 1

    # Obtener las posiciones y orientaciones de la aruco
    arucos_data = msg.data[:-1]
    aruco_info = arucos_data.split(':')
    id_aruco, x, y, z, x_orientation, y_orientation, z_orientation, w_orientation = map(float, aruco_info)

    # Redondear las posiciones y orientaciones a dos decimales
    x = round(x, 2)
    y = round(y, 2)
    z = round(z, 2)
    x_orientation = round(x_orientation, 2)
    y_orientation = round(y_orientation, 2)
    z_orientation = round(z_orientation, 2)
    w_orientation = round(w_orientation, 2)

    # Almacenar las posiciones y orientaciones en los arrays
    positions_array.append((x, y, z))
    orientations_array.append((x_orientation, y_orientation, z_orientation, w_orientation))


    if callback_counter == 10 or callback_counter == 0:

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


        # Calcular las posiciones más comunes
        most_common_positions = Counter(positions_array).most_common()

        # Ordenar las posiciones por frecuencia y mantener el orden original en caso de empate
        most_common_positions.sort(key=lambda x: (-x[1], positions_array.index(x[0])))

        # Obtener la posición más repetida (o la primera en caso de empate)
        most_common_position = most_common_positions[0][0]

        # Calcular las orientaciones más comunes
        most_common_orientations = Counter(orientations_array).most_common()

        # Ordenar las orientaciones por frecuencia y mantener el orden original en caso de empate
        most_common_orientations.sort(key=lambda x: (-x[1], orientations_array.index(x[0])))

        # Obtener la orientación más repetida (o la primera en caso de empate)
        most_common_orientation = most_common_orientations[0][0]

        # Crear la transformación con la posición y orientación más repetidas
        t_nueva = geometry_msgs.msg.TransformStamped()
        t_nueva.header.stamp = rospy.Time.now()
        t_nueva.header.frame_id = "camera_link"
        t_nueva.child_frame_id = "aruco_frame"
        t_nueva.transform.translation.x = most_common_position[0]
        t_nueva.transform.translation.y = most_common_position[1]
        t_nueva.transform.translation.z = most_common_position[2]
        t_nueva.transform.rotation.x = most_common_orientation[0]
        t_nueva.transform.rotation.y = most_common_orientation[1]
        t_nueva.transform.rotation.z = most_common_orientation[2]
        t_nueva.transform.rotation.w = most_common_orientation[3]

        broadcaster.sendTransform(t_nueva)


        # Limpiar el array de posiciones y orientaciones para la siguiente ronda
        positions_array = []
        orientations_array = []

        # Resetear el contador
        callback_counter = 0

if __name__ == '__main__':
    main()
