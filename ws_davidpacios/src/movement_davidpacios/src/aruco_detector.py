#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from std_msgs.msg import String
import numpy as np
import tf
import tf.transformations as tr

bridge = CvBridge()

# Inicializar el detector de ArUco y los parámetros de la cámara
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

# Parámetros íntrinsecos de la cámara Astra Orbbec
camera_matrix = np.array([[554.26, 0, 320], 
                          [0, 460.89, 240], 
                          [0, 0, 1]]) #Matriz de la cámara

dist_coeffs = np.zeros((4, 1)) #Coeficientes de distorsión

# Publicador para las posiciones y orientaciones de los arucos
aruco_pose_pub = rospy.Publisher('/aruco_poses', String, queue_size=10)
aruco_pose_pub_frame = rospy.Publisher('/aruco_pose_frame', String, queue_size=10) 

id_aruco_to_frame = 8
marker_length_to_frame = 0.06  # Longitud del lado del marcador ArUco (en metros)
marker_length_to_pick_and_place = 0.024

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
    
        # Detectar los marcadores
        corners, ids, rejected = detector.detectMarkers(frame)
        
        # Dibujar los marcadores
        if ids is None:
            return
        
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        
        for i in range(len(ids)):
            id_aruco = ids[i][0]
            corner = corners[i][0]

            if id_aruco in ids_saved:
                continue

            # Obtener los puntos 3D del marcador ArUco (esquina en la parte superior izquierda)
            if id_aruco == id_aruco_to_frame:
                marker_length = marker_length_to_frame
            else:
                marker_length = marker_length_to_pick_and_place


            obj_points = np.array([[0, 0, 0], [marker_length, 0, 0], [marker_length, marker_length, 0], [0, marker_length, 0]], dtype=np.float32)
            # Obtener los puntos 2D del marcador ArUco
            image_points = corner.reshape(-1, 1, 2)
            # Calcular la pose del marcador usando solvePnP
            success, rvec, tvec = cv2.solvePnP(obj_points, image_points, camera_matrix, dist_coeffs)
            # Convertir la orientación de rotación a cuaternión
            rvec_matrix = cv2.Rodrigues(rvec)[0]
            # Añadir una fila de ceros con un 1 en la última posición
            rvec_matrix_4x4 = np.vstack([rvec_matrix, [0, 0, 0]])
            # Añadir una columna de ceros con un 1 en la última posición
            rvec_matrix_4x4 = np.hstack([rvec_matrix_4x4, np.array([[0], [0], [0], [1]])])
            q = tr.quaternion_from_matrix(rvec_matrix_4x4)
        
            # print(f"Marcador ID {ids[i]}:")
            # print("Tvec:", tvec)
            # print("Rvec:", rvec)
            # print("Matrix:", rvec_matrix)
            # print("Q:", q)
            # print()

            if id_aruco == id_aruco_to_frame:
                aruco_info_frame = f"{id_aruco}:{tvec[0][0]}:{tvec[1][0]}:{tvec[2][0]}:{q[0]}:{q[1]}:{q[2]}:{q[3]};"
                aruco_pose_pub_frame.publish(aruco_info_frame)
                continue

            #Formatear la información del ArUco
            aruco_info += f"{id_aruco}:{tvec[0][0]}:{tvec[1][0]}:{tvec[2][0]}:{q[0]}:{q[1]}:{q[2]}:{q[3]};"
            ids_saved.append(id_aruco)


        counter+=1;
        if counter == 50:
            #print(aruco_info)
            aruco_pose_pub.publish(aruco_info)
            counter = 0
            aruco_info = ""
            #aruco_info = "100:0.4161880497314183:0.11825780711004699:0.14369141349788575:-0.9231143539216148:-0.3840649074696301:-0.01819345318830564:0.00479944739623474;"
            ids_saved = []
            
        # Mostrar la imagen
        cv2.imshow("Image", frame)
        cv2.waitKey(1)
        
    except Exception as e:
        print(e)

def main():
    rospy.init_node('aruco_detector', anonymous=True)

    rospy.Subscriber("/camera/color/image_raw", Image, image_callback)
    rospy.spin()

if __name__ == '__main__':
    main()
