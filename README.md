# Percepción visual de objetos para tareas de manipulación colaborativas (en desarrollo)

## Trabajo de fin de grado para el Grado de Ingeniería Informática en la Universidad de Santiago de Compostela.

Se trabajará con el brazo robótico colaborativo Franka Panda para llevar a cabo tareas de manipulación en colaboración con un operador humano. Se utilizará la interfaz de programación del brazo basada en ROS (Robot Operating System) con la ayuda del paquete MoveIt para generar y ejecutar una trayectoria que coloque la pinza del brazo en una posición adecuada para agarrar un objeto ubicado en una mesa. Para calcular la posición de los diferentes objetos se utilizará una cámara Astra y las librerías Aruco y PCL con la finalidad calibrar la cámara y de calcular las posiciones de los objetos tomando como sistema de referencia el Robot Franka. Este objeto puede tener un tamaño variable que será percibido a través de los sensores táctiles GelSight Mini, que escanean imágenes 2D y 3D de diversas superficies de materiales. El tamaño del objeto estará limitado por la capacidad máxima de la pinza del robot. Una vez que el robot haya agarrado el objeto, deberá depositarlo en una posición final. Posteriormente, el robot podrá volver a su posición inicial y repetir esta tarea tantas veces como sea necesario. Durante la ejecución, se deberán tener en cuenta los límites articulares y de la pinza del robot Panda. Toda esta tarea estará automatizada con el uso de lanzadores propios de ROS que iniciarán nodos de los diferentes paquetes.

# Commands
## Pick and place node
roslaunch movement_davidpacios sensor_franka.launch
roslaunch movement_davidpacios pick_and_place.launch

## Camara Astra RGBD
https://www.yahboom.net/public/upload/upload-html/1637059883/Astra%20camera%20calibration.html
roslaunch astra_camera astra.launch
rosrun camera_calibration cameracalibrator.py image:=/camera/color/image_raw camera:=/camera/camera --size 8x6 --square 0.0245


