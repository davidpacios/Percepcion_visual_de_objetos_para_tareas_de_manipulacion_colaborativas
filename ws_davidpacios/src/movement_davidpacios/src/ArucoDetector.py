#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from std_msgs.msg import String, Bool
import numpy as np
import tf
import tf.transformations as tr
import yaml

class ArucoDetector:
    def __init__(self):
        rospy.init_node('aruco_detector', anonymous=True)

        self.bridge = CvBridge()
        
        # Initialize the ArUco detector and camera parameters
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.parameters = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.parameters)
        
        # Calibration parameters yaml file
        self.camera_calibration_parameters_filename = "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/movement_davidpacios/camera/rgb_camera.yaml"
        
        # Publishers for ArUco positions and orientations
        self.aruco_pose_pub = rospy.Publisher('/aruco_poses', String, queue_size=10)
        self.aruco_pose_pub_frame = rospy.Publisher('/aruco_pose_frame', String, queue_size=10)
        
        self.id_aruco_to_frame = 8
        self.marker_length_to_frame = 0.095  # Marker side length (in meters)
        self.marker_length_to_pick_and_place = 0.030
        
        self.aruco_info = ""
        self.rate = rospy.Rate(10)  # 10 Hz

        # Initialize camera parameters
        self.camera_matrix = None
        self.dist_coeffs = None
        self.load_camera_parameters()
        
        # Subscribe to the camera image topic
        rospy.Subscriber("/camera/color/image_raw", Image, self.image_callback)

        self.camera_calibration = False
        rospy.Subscriber("calibration_done", Bool, self.callback_camera_calibration_done)
        
        
    def load_camera_parameters(self):
        try:
            with open(self.camera_calibration_parameters_filename, 'r') as f:
                yaml_content = yaml.safe_load(f)
                
                camera_matrix_str = yaml_content['camera_matrix']['data']
                dist_coeffs_str = yaml_content['distortion_coefficients']['data']
                
                self.dist_coeffs = np.array([float(coeff) for coeff in dist_coeffs_str[0].split()]).reshape(-1, 1)
                self.camera_matrix = np.array(camera_matrix_str).reshape(3, 3)

                print("Camera matrix:")
                print(self.camera_matrix)
                print("\nDistortion coefficients:")
                print(self.dist_coeffs)
                
        except FileNotFoundError:
            print(f"Error: The file '{self.camera_calibration_parameters_filename}' was not found.")
        except IOError:
            print(f"Error: The file '{self.camera_calibration_parameters_filename}' cannot be opened.")

    def image_callback(self, msg):
        # Convert the ROS image message to an OpenCV image
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
    
        corners, ids, rejected = self.detector.detectMarkers(frame)
        if ids is None: return
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        
        for i in range(len(ids)):
            id_aruco = ids[i][0]
            corner = corners[i][0]

            if id_aruco == self.id_aruco_to_frame: marker_length = self.marker_length_to_frame
            else: marker_length = self.marker_length_to_pick_and_place
            
            obj_points = np.array([[0, 0, 0], [marker_length, 0, 0], [marker_length, marker_length, 0], [0, marker_length, 0]], dtype=np.float32)
            image_points = corner.reshape(-1, 1, 2)
            success, rvec, tvec = cv2.solvePnP(obj_points, image_points, self.camera_matrix, self.dist_coeffs)
            cv2.drawFrameAxes(frame, self.camera_matrix, self.dist_coeffs, rvec, tvec, marker_length)

            rvec_matrix = cv2.Rodrigues(rvec)[0]
            rvec_matrix_4x4 = np.eye(4)
            rvec_matrix_4x4[:3, :3] = rvec_matrix
            rvec_matrix_4x4[:3, 3] = tvec.flatten()
            q = tr.quaternion_from_matrix(rvec_matrix_4x4)

            if id_aruco == self.id_aruco_to_frame:
                aruco_info_frame = f"{id_aruco}:{tvec[0][0]}:{tvec[1][0]}:{tvec[2][0]}:{q[0]}:{q[1]}:{q[2]}:{q[3]};"
                self.aruco_pose_pub_frame.publish(aruco_info_frame)
            else:
                self.aruco_info += f"{id_aruco}:{tvec[0][0]}:{tvec[1][0]}:{tvec[2][0]}:{q[0]}:{q[1]}:{q[2]}:{q[3]};"

        if self.camera_calibration:
            self.aruco_pose_pub.publish(self.aruco_info)
            self.aruco_info = ""
            
        cv2.imshow("Image", frame)
        cv2.waitKey(1)
        self.rate.sleep()

    def callback_camera_calibration_done(self,data):
        self.camera_calibration = data

if __name__ == '__main__':
    aruco_detector = ArucoDetector()
    rospy.spin()



# rotation_matrix = np.eye(4)
# rotation_matrix[0:3, 0:3] = cv2.Rodrigues(np.array(rvec))[0]
# r = R.from_matrix(rotation_matrix[0:3, 0:3])
# quat = r.as_quat()

# print(f"Marker2 ID {ids[i]}:")
# print("Tvec:", tvec)
# print("Rvec:", rvec)
# print("Matrix:", rotation_matrix)
# print("Q:", quat)
# print("--------------------------")
