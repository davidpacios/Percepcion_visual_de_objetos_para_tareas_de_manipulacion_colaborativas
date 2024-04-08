#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PoseStamped
import tf2_ros

 # Inicializar el objeto TransformListener
tf_buffer = tf2_ros.Buffer()
tf_listener = tf2_ros.TransformListener(tf_buffer)
pub = rospy.Publisher('/aruco_poses_trf', PoseStamped, queue_size=10)

def aruco_callback(msg):
    try:
        aruco_poses = msg.split(';')
        #transformed_poses = ""
        transformed_poses = "100:0.4161880497314183:0.11825780711004699:0.14369141349788575:-0.9231143539216148:-0.3840649074696301:-0.01819345318830564:0.00479944739623474;"

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
            
            # Transformar el PoseStamped al marco de referencia deseado
            trf_pose = tf_buffer.transform(aruco_pose, "/panda_link0", rospy.Time(0))
            
            # Construir el string con la información de la posición transformada
            trf_pose_str = f"{id_aruco}:{trf_pose.pose.position.x}:{trf_pose.pose.position.y}:{trf_pose.pose.position.z}:{trf_pose.pose.orientation.x}:{trf_pose.pose.orientation.y}:{trf_pose.pose.orientation.z}:{trf_pose.pose.orientation.w};"
            
            # Concatenar el string al string global
            transformed_poses += trf_pose_str
        
        # Publicar todas las posiciones transformadas juntas
        pub.publish(transformed_poses)
    
    except Exception as e:
        rospy.logerr("Error al procesar la información de los ArUcos: %s", str(e))


def main():
    rospy.init_node('aruco_transformer')
    
    # Suscribirse al topic que contiene las posiciones de los ArUcos
    rospy.Subscriber('/aruco_poses', PoseStamped, aruco_callback)
    
    rospy.spin()

if __name__ == '__main__':
    main()
