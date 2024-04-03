#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from std_msgs.msg import String
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
aruco_pose_pub = rospy.Publisher('/aruco_poses', String, queue_size=10)  # Cambiado el tipo de mensaje a una lista de PoseStamped

counter = 0
ids_saved = []
#aruco_info = ""

# pose_pick = geometry_msgs.msg.Pose()
# pose_pick.position.x = 0.4161880497314183
# pose_pick.position.y = 0.11825780711004699
# pose_pick.position.z = 0.14369141349788575
# pose_pick.orientation.x = -0.9231143539216148
# pose_pick.orientation.y = -0.3840649074696301
# pose_pick.orientation.z = -0.01819345318830564
# pose_pick.orientation.w = 0.00479944739623474
aruco_info = "100:0.4161880497314183:0.11825780711004699:0.14369141349788575:-0.9231143539216148:-0.3840649074696301:-0.01819345318830564:0.00479944739623474;"

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
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            
            # Construir el mensaje de tipo String con la información de los arucos
            for i in range(len(ids)):
                if ids[i][0] in ids_saved:
                    continue

                marker_id = ids[i][0]
                marker_x = corners[i][0][0][0] / 100
                marker_y = corners[i][0][0][1] / 100
                marker_z = 0 / 100
                orientation_x = 0
                orientation_y = 0
                orientation_z = 0
                orientation_w = 0

                aruco_info += f"{marker_id}:{marker_x}:{marker_y}:{marker_z}:{orientation_x}:{orientation_y}:{orientation_z}:{orientation_w};"

                ids_saved.append(marker_id)

            counter+=1;
            
            if counter == 50:
                aruco_pose_pub.publish(aruco_info)
                counter = 0
                #aruco_info = ""
                aruco_info = "100:0.4161880497314183:0.11825780711004699:0.14369141349788575:-0.9231143539216148:-0.3840649074696301:-0.01819345318830564:0.00479944739623474;"

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
