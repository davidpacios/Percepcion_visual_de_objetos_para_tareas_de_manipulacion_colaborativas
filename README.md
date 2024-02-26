# Percepción visual de objetos y humanos para tareas de manipulación colaborativas (en desarrollo)

## Trabajo de fin de grado para el Grado de Ingeniería Informática en la Universidad de Santiago de Compostela.

Se empleará el brazo robótico colaborativo Franka Panda junto con ROS y MoveIt! para desarrollar tareas de manipulación en cooperación con un operador humano. Además, se utilizará una cámara RGBD y la librería PCL para detectar la posición del objeto y ajustar automáticamente la trayectoria del robot.

# Pick and place node
roslaunch panda_moveit_config franka_control.launch robot_ip:=172.16.0.2 
rosrun davidpacios_movement movement.py

# Camara Astra RGBD
https://www.yahboom.net/public/upload/upload-html/1637059883/Astra%20camera%20calibration.html
roslaunch astra_camera astra.launch
rosrun camera_calibration cameracalibrator.py image:=/camera/color/image_raw camera:=/camera/camera --size 8x6 --square 0.0245


