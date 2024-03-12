#! /usr/bin/env python3
import cv2
import numpy as np

for i in range(10):  # Probamos con los primeros 10 índices
        cap = cv2.VideoCapture(i,cv2.CAP_V4L2)
        if cap.isOpened():
            print(f"Opción {i}: Abierto")
            cap.release()
        else:
            print(f"Opción {i}: No abierto")


cap = cv2.VideoCapture(1, cv2.CAP_V4L2)


aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

while True:
    # Capturar una imagen
    ret, frame = cap.read()

    # Detectar los marcadores
    corners, ids, rejected = detector.detectMarkers(frame)


    # Dibujar los marcadores
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    # Mostrar la imagen
    cv2.imshow("Image", frame)

    # Esperar a que el usuario pulse una tecla
    key = cv2.waitKey(1)
    if key == 27:
        break

# Cerrar la cámara
cap.release()

# Obtener la posición de los marcadores
marker_corners = corners[0]
marker_id = ids[0][0]

# Obtener las dimensiones del cubo
cube_width = 0.5
cube_height = 0.5
cube_depth = 0.5

# Dibujar el cubo
cv2.drawCube(frame, marker_corners, marker_id, cube_width, cube_height, cube_depth)

cv2.imshow("Image", frame)