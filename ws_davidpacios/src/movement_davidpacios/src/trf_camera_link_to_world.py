#!/usr/bin/env python3
import rospy
import tf2_ros
import geometry_msgs.msg
from std_msgs.msg import String

aux = False
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
    global aux
    if not aux: aux = True

    arucos_data = msg.data[:-1]
    aruco_info = arucos_data.split(':')
    id_aruco, x, y, z, x_orientation, y_orientation, z_orientation, w_orientation = map(float, aruco_info)


    # Crear un objeto TransformStamped con la información recibida
    t = geometry_msgs.msg.TransformStamped()
    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "aruco_frame"
    t.child_frame_id = "camera_link"

    # Transformación entre aruco_frame y camera_link
    t.transform.translation.x = x
    t.transform.translation.y = y
    t.transform.translation.z = z
    t.transform.rotation.x = x_orientation
    t.transform.rotation.y = y_orientation
    t.transform.rotation.z = z_orientation
    t.transform.rotation.w = w_orientation
    
    # Publicar la transformación entre aruco_frame y camera_link
    broadcaster.sendTransform(t)

    # Añadir transformación entre panda_link0 y aruco_frame
    t_nueva = geometry_msgs.msg.TransformStamped()
    t_nueva.header.stamp = rospy.Time.now()
    t_nueva.header.frame_id = "panda_link0"
    t_nueva.child_frame_id = "aruco_frame"
    t_nueva.transform.translation.x = 0.80  
    t_nueva.transform.translation.y = 0.06
    t_nueva.transform.translation.z = 0.00  
    t_nueva.transform.rotation.x = 0
    t_nueva.transform.rotation.y = 0
    t_nueva.transform.rotation.z = 0
    t_nueva.transform.rotation.w = 1
    
    # Publicar la nueva transformación entre panda_link0 y aruco_frame
    broadcaster.sendTransform(t_nueva)

if __name__ == '__main__':
    main()
