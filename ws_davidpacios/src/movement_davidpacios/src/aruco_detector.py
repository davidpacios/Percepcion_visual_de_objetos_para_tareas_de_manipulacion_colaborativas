#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from std_msgs.msg import String
import numpy as np
import tf

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
aruco_pose_calibration_pub = rospy.Publisher('/aruco_pose_panda_link0', String, queue_size=10) 

counter = 0
ids_saved = []
aruco_info = ""

# pose_pick = geometry_msgs.msg.Pose()
# pose_pick.position.x = 0.4161880497314183
# pose_pick.position.y = 0.11825780711004699
# pose_pick.position.z = 0.14369141349788575
# pose_pick.orientation.x = -0.9231143539216148
# pose_pick.orientation.y = -0.3840649074696301
# pose_pick.orientation.z = -0.01819345318830564
# pose_pick.orientation.w = 0.00479944739623474

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
                id_aruco = ids[i][0]
                corner = corners[i][0]

                if id_aruco in ids_saved:
                    continue

                # Calcular la posición y la orientación del marcador
                rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corner, 0.1, camera_matrix, dist_coeffs)
                
                # Convertir la orientación de rotación a cuaternión
                rvec_matrix = cv2.Rodrigues(rvec)[0]
                q = tf.transformations.quaternion_from_matrix(rvec_matrix)
                
                if id_aruco == 7: #Aruco Calibration
                    aruco_aux = f"{id_aruco}:{tvec[0][0]:.2f}:{tvec[0][1]:.2f}:{tvec[0][2]:.2f}:{q[0]:.2f}:{q[1]:.2f}:{q[2]:.2f}:{q[3]:.2f};"
                    aruco_pose_pub.publish(aruco_aux)
                    continue

                # Formatear la información del ArUco
                aruco_info += f"{id_aruco}:{tvec[0][0]:.2f}:{tvec[0][1]:.2f}:{tvec[0][2]:.2f}:{q[0]:.2f}:{q[1]:.2f}:{q[2]:.2f}:{q[3]:.2f};"
                ids_saved.append(id_aruco)

            counter+=1;
            if counter == 50:
                print(aruco_info)
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
