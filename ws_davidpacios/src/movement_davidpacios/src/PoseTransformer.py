#!/usr/bin/env python3
import rospy
import tf2_ros
from std_msgs.msg import String
from tf2_geometry_msgs import PoseStamped


class PoseTransformer:
    def __init__(self):
        rospy.init_node('pose_transformer')

        self.tf_buf = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buf)
        self.pub = rospy.Publisher('/aruco_poses_trf', String, queue_size=10)
        
        # Subscribe to the topic containing the ArUco positions
        rospy.Subscriber('/aruco_poses', String, self.aruco_callback)

    def aruco_callback(self, msg):
        aruco_poses = msg.data.split(';')[:-1]
        transformed_poses = ""

        for aruco_pose_str in aruco_poses:
            aruco_info = aruco_pose_str.split(':')
            
            id_aruco, x, y, z, x_orientation, y_orientation, z_orientation, w_orientation = map(float, aruco_info)
            
            aruco_pose = PoseStamped()
            aruco_pose.header.frame_id = "camera_link"  # The reference frame of the ArUco
            aruco_pose.pose.position.x = x
            aruco_pose.pose.position.y = y
            aruco_pose.pose.position.z = z
            aruco_pose.pose.orientation.x = x_orientation
            aruco_pose.pose.orientation.y = y_orientation
            aruco_pose.pose.orientation.z = z_orientation
            aruco_pose.pose.orientation.w = w_orientation

            try:
                # Wait until the transformation is available
                self.tf_buf.can_transform("camera_link", "world", rospy.Time(), rospy.Duration(1.0))
                # Perform the transformation of the position
                target_pt = self.tf_buf.transform(aruco_pose, "world")
                transformed_poses += f"{id_aruco}:{target_pt.pose.position.x}:{target_pt.pose.position.y}:{target_pt.pose.position.z}:{target_pt.pose.orientation.x}:{target_pt.pose.orientation.y}:{target_pt.pose.orientation.z}:{target_pt.pose.orientation.w};"
                
            except Exception as e:
                # Handle the exception if the transformation cannot be performed
                rospy.logwarn(f"Could not perform transformation for ArUco ID {id_aruco}: {e}")

        # Publish all transformed positions together
        self.pub.publish(transformed_poses)

    

if __name__ == '__main__':
    pose_transformer = PoseTransformer()
    rospy.spin()
