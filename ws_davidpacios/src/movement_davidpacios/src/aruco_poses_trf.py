#!/usr/bin/env python3
import rospy
import tf2_ros
from std_msgs.msg import String
import tf2_ros
from tf2_geometry_msgs import PoseStamped
from tf import transformations

pub = rospy.Publisher('/aruco_poses_trf', String, queue_size=10)

def aruco_callback(msg):
    aruco_poses = msg.data.split(';')[:-1]
    transformed_poses = ""
    #transformed_poses = "100:0.4161880497314183:0.11825780711004699:0.14369141349788575:-0.9231143539216148:-0.3840649074696301:-0.01819345318830564:0.00479944739623474;"

    for aruco_pose_str in aruco_poses:
        aruco_info = aruco_pose_str.split(':')
        
        id_aruco, x, y, z, x_orientation, y_orientation, z_orientation, w_orientation = map(float, aruco_info)
        
        aruco_pose = PoseStamped()
        aruco_pose.header.frame_id = "camera_link"  # El marco de referencia del ArUco
        aruco_pose.pose.position.x = x
        aruco_pose.pose.position.y = y
        aruco_pose.pose.position.z = z
        aruco_pose.pose.orientation.x = x_orientation
        aruco_pose.pose.orientation.y = y_orientation
        aruco_pose.pose.orientation.z = z_orientation
        aruco_pose.pose.orientation.w = w_orientation


        tf_buf = tf2_ros.Buffer()
        tf_listener = tf2_ros.TransformListener(tf_buf)
        try:
            # Esperar hasta que se pueda obtener la transformación
            tf_buf.can_transform("camera_link", "world", rospy.Time(), rospy.Duration(1.0))
            # Realizar la transformación de la posición
            target_pt = tf_buf.transform(aruco_pose, "world")
            transformed_poses += f"{id_aruco}:{target_pt.pose.position.x}:{target_pt.pose.position.y}:{target_pt.pose.position.z}:{target_pt.pose.orientation.x}:{target_pt.pose.orientation.y}:{target_pt.pose.orientation.z}:{target_pt.pose.orientation.w};"
            
        except Exception as e:
            # Manejar la excepción si no se puede realizar la transformación
            print(f"No se pudo realizar la transformación para el ArUco ID {id_aruco}: {e}")

    # Publicar todas las posiciones transformadas juntas
    pub.publish(transformed_poses)
   
def main():
    rospy.init_node('aruco_poses_trf')
    
    # Suscribirse al topic que contiene las posiciones de los ArUcos
    rospy.Subscriber('/aruco_poses', String, aruco_callback)
    
    rospy.spin()

if __name__ == '__main__':
    main()
