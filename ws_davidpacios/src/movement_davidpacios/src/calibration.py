#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from geometry_msgs.msg import PoseStamped
import numpy as np

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
aruco_pose_pub = rospy.Publisher('/aruco_poses', PoseStamped, queue_size=10)

def image_callback(msg):
    try:
        # Convertir el mensaje de imagen de ROS a una imagen OpenCV
        frame = bridge.imgmsg_to_cv2(msg, "bgr8")
    
        # Detectar los marcadores
        corners, ids, rejected = detector.detectMarkers(frame)
        
        # Dibujar los marcadores
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            
            # Calcular la pose de los marcadores usando solvePnP
            for i in range(len(ids)):
                # Obtener los puntos 3D del marcador ArUco (esquina en la parte superior izquierda)
                marker_length = 0.5  # Longitud del lado del marcador ArUco (en metros)
                obj_points = np.array([[0, 0, 0], [marker_length, 0, 0], [marker_length, marker_length, 0], [0, marker_length, 0]], dtype=np.float32)
                
                # Obtener los puntos 2D del marcador ArUco
                image_points = corners[i][0]
                
                # Calcular la pose del marcador usando solvePnP
                success, rvec, tvec = cv2.solvePnP(obj_points, image_points, camera_matrix, dist_coeffs)
                
                # Imprimir la posición del marcador con respecto a la cámara
                if success:
                    print(f"Marcador ID {ids[i]}:")
                    print("Rvec:", rvec.flatten())
                    print("Tvec:", tvec.flatten())
                    print()
                    pose_msg = PoseStamped()
                    pose_msg.header.stamp = rospy.Time.now()
                    pose_msg.header.frame_id = f"aruco_{ids[i]}"  # Usar el ID del marcador como nombre del marco
                    pose_msg.pose.position.x = tvec[0][0]
                    pose_msg.pose.position.y = tvec[1][0]
                    pose_msg.pose.position.z = tvec[2][0]

                    aruco_pose_pub.publish(pose_msg)
                    
                    # # Convertir el vector de rotación (rvec) a una matriz de rotación
                    # rot_matrix = cv2.Rodrigues(rvec)[0]
                    
                    # # Convertir la matriz de rotación a un cuaternión
                    # quaternion = quaternion_from_matrix(rot_matrix)
                    
                    # # Asignar la orientación del cuaternión al mensaje PoseStamped
                    # pose_msg.pose.orientation.x = quaternion[0]
                    # pose_msg.pose.orientation.y = quaternion[1]
                    # pose_msg.pose.orientation.z = quaternion[2]
                    # pose_msg.pose.orientation.w = quaternion[3]
                    
                    
        
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
