#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from std_msgs.msg import String
import numpy as np
import tf
import tf.transformations as tr
import math
import os
import yaml
from scipy.spatial.transform import Rotation as R

bridge = CvBridge()

# Inicializar el detector de ArUco y los parámetros de la cámara
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

# Calibration parameters yaml file
camera_calibration_parameters_filename = "/home/frankaros/TFG_Percepcion_visual_de_objetos_y_humanos_para_tareas_de_manipulacion_colaborativas/ws_davidpacios/src/movement_davidpacios/camera/rgb_camera.yaml"
# Parámetros íntrinsecos de la cámara Astra Orbbec


# Publicador para las posiciones y orientaciones de los arucos
aruco_pose_pub = rospy.Publisher('/aruco_poses', String, queue_size=10)
aruco_pose_pub_frame = rospy.Publisher('/aruco_pose_frame', String, queue_size=10) 

id_aruco_to_frame = 8
marker_length_to_frame = 0.095 #metros
marker_length_to_pick_and_place = 0.030 #metros

counter = 0
ids_saved = []
aruco_info = ""

def image_callback(msg):
    global ids_saved
    global counter
    global aruco_info
    try:
        # Convertir el mensaje de imagen de ROS a una imagen OpenCV
        frame = bridge.imgmsg_to_cv2(msg, "bgr8")
    
        corners, ids, rejected = detector.detectMarkers(frame)
        if ids is None: return
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        
        for i in range(len(ids)):
            id_aruco = ids[i][0]
            corner = corners[i][0]

            if id_aruco == id_aruco_to_frame: marker_length = marker_length_to_frame
            else: marker_length = marker_length_to_pick_and_place
            obj_points = np.array([[0, 0, 0], [marker_length, 0, 0], [marker_length, marker_length, 0], [0, marker_length, 0]], dtype=np.float32)
            image_points = corner.reshape(-1, 1, 2)
            success, rvec, tvec = cv2.solvePnP(obj_points, image_points, camera_matrix, dist_coeffs)
            cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec, tvec, marker_length)

            rvec_matrix = cv2.Rodrigues(rvec)[0]
            rvec_matrix_4x4 = np.eye(4)
            rvec_matrix_4x4[:3, :3] = rvec_matrix
            rvec_matrix_4x4[:3, 3] = tvec.flatten()
            q = tr.quaternion_from_matrix(rvec_matrix_4x4)

            if id_aruco == id_aruco_to_frame:
                aruco_info_frame = f"{id_aruco}:{tvec[0][0]}:{tvec[1][0]}:{tvec[2][0]}:{q[0]}:{q[1]}:{q[2]}:{q[3]};"
                aruco_pose_pub_frame.publish(aruco_info_frame)
            elif id_aruco not in ids_saved:
                aruco_info += f"{id_aruco}:{tvec[0][0]}:{tvec[1][0]}:{tvec[2][0]}:{q[0]}:{q[1]}:{q[2]}:{q[3]};"
                ids_saved.append(id_aruco)

        counter+=1;
        if counter == 50:
            aruco_pose_pub.publish(aruco_info)
            counter = 0
            aruco_info = ""
            ids_saved = []
            
        cv2.imshow("Image", frame)
        cv2.waitKey(1)
        
    except Exception as e:
        print(e)

def main():
    rospy.init_node('aruco_detector', anonymous=True)
    global camera_matrix
    global  dist_coeffs
    try:
        # Abrir el archivo YAML
        with open(camera_calibration_parameters_filename, 'r') as f:
            contenido_yaml = yaml.safe_load(f)
            
            # Extraer la matriz de la cámara y los coeficientes de distorsión
            camera_matrix_str = contenido_yaml['camera_matrix']['data']
            dist_coeffs_str = contenido_yaml['distortion_coefficients']['data']
            
            # Convertir los coeficientes de distorsión de string a una lista de floats
            dist_coeffs = np.array([float(coeff) for coeff in dist_coeffs_str[0].split()]).reshape(-1, 1)
            # Convertir la matriz de la cámara de string a un array numpy
            camera_matrix = np.array(camera_matrix_str).reshape(3, 3)

            print("Matriz de la cámara:")
            print(camera_matrix)
            print("\nCoeficientes de distorsión:")
            print(dist_coeffs)
            
    except FileNotFoundError:
        print(f"Error: El archivo '{camera_calibration_parameters_filename}' no se encuentra.")
        return
    except IOError:
        print(f"Error: No se puede abrir el archivo '{camera_calibration_parameters_filename}'.")
        return
    rospy.Subscriber("/camera/color/image_raw", Image, image_callback)
    rospy.spin()

if __name__ == '__main__':
    main()
                 
# print(f"Marcador ID {ids[i]}:")
# print("Tvec:", tvec)
# print("Rvec:", rvec)
# print("Matrix:", rvec_matrix)
# print("Matrix_4x4:", rvec_matrix_4x4)
# print("Q:", q)
# print()

# rotation_matrix = np.eye(4)
# rotation_matrix[0:3, 0:3] = cv2.Rodrigues(np.array(rvec))[0]
# r = R.from_matrix(rotation_matrix[0:3, 0:3])
# quat = r.as_quat()

# print(f"Marcador2 ID {ids[i]}:")
# print("Tvec:", tvec)
# print("Rvec:", rvec)
# print("Matrix:", rotation_matrix)
# print("Q:", quat)
# print("--------------------------")