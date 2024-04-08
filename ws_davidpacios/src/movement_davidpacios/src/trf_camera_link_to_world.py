#!/usr/bin/env python3
import rospy
import tf2_ros
import geometry_msgs.msg
from std_msgs.msg import String

broadcaster = tf2_ros.TransformBroadcaster()

def main():
    rospy.init_node('trf_camera_link_to_world')   

    # Suscribirse al topic que contiene la información de la transformación
    print("============ Subscribing to topic /aruco_pose_panda_link0 ...")
    rospy.Subscriber("aruco_pose_panda_link0", String, transform_callback)


def transform_callback(msg):
    # Crear un objeto TransformStamped con la información recibida
    t = geometry_msgs.msg.TransformStamped()
    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "world"
    t.child_frame_id = "camera_link"

    aruco_info = msg.split(':')
    id_aruco, x, y, z, x_orientation, y_orientation, z_orientation, w_orientation = map(float, aruco_info)

    #Transformar con respecto a world: 
    #(0.86,0,0.03) panda_link0 == (447,380,0) camera_link
    #(x,y,z) panda_link0 == (210, 441,0) camera_link

    t.transform.translation.x = x
    t.transform.translation.y = y
    t.transform.translation.z = z
    t.transform.rotation.x = x_orientation
    t.transform.rotation.y = y_orientation
    t.transform.rotation.z = z_orientation
    t.transform.rotation.w = w_orientation
    
    # Publicar la transformación
    broadcaster.sendTransform(t)

if __name__ == '__main__':
    main()
