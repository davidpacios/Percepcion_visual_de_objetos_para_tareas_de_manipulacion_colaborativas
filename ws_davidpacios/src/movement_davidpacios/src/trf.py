#!/usr/bin/env python3

import rospy
import tf
from geometry_msgs.msg import PointStamped

if __name__ == "__main__":
    rospy.init_node("transform_aruco_position")

    listener = tf.TransformListener()

    # Supongamos que tienes la posición del ArUco en el marco de referencia /camera_link
    aruco_position_camera = PointStamped()
    aruco_position_camera.header.frame_id = "camera_link"
    aruco_position_camera.point.x = 416.0
    aruco_position_camera.point.y = 417.0
    aruco_position_camera.point.z = 0.0

    # Espera para asegurarse de que se haya publicado la transformación
    rospy.sleep(1.0)

    # Transforma la posición del ArUco de /camera_link a panda_link8
    try:
        aruco_position_panda = listener.transformPoint("panda_link0", aruco_position_camera)
        rospy.loginfo(f"Posición del ArUco en panda_link0: {aruco_position_panda}")
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        rospy.logwarn("No se pudo realizar la transformación.")

    rospy.spin()
