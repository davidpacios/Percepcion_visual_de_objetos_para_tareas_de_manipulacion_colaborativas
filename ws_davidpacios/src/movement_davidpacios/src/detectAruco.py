#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

bridge = CvBridge()

# Inicializar el detector de ArUco y los parámetros de la cámara
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

def image_callback(msg):
    try:
        # Convertir el mensaje de imagen de ROS a una imagen OpenCV
        frame = bridge.imgmsg_to_cv2(msg, "bgr8")
        # Capturar una imagen
    
        # Detectar los marcadores
        corners, ids, rejected = detector.detectMarkers(frame)
        
        # Dibujar los marcadores
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    
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

