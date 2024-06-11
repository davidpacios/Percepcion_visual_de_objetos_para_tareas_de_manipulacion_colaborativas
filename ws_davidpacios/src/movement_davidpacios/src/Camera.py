#!/usr/bin/env python3
import rospy
import tf2_ros
import geometry_msgs.msg
from std_msgs.msg import String, Bool
from tf import transformations
import numpy as np
from collections import Counter

class Camera:
    def __init__(self, id_aruco_calibration):
        self.id_aruco_calibration = id_aruco_calibration
        self.measurements = {
            'x': [],
            'y': [],
            'z': [],
            'x_orientation': [],
            'y_orientation': [],
            'z_orientation': [],
            'w_orientation': []
        }
        self.calibrated = False

        # Initialize ROS node
        rospy.init_node('camera')

        # Create a TransformBroadcaster
        self.broadcaster = tf2_ros.TransformBroadcaster()

        # Create a publisher for the calibration done topic
        self.calibration_pub = rospy.Publisher("calibration_done", Bool, queue_size=10)

        # Subscribe to the aruco pose frame topic
        rospy.Subscriber("aruco_pose_frame", String, self.collect_measurements_callback)

        # Subscribe to the request calibration topic
        rospy.Subscriber("request_calibration", Bool, self.request_calibration_callback)

        print("============ Using the aruco with id ", id_aruco_calibration, " to create the frame")

    def request_calibration_callback(self, msg):
        if msg.data:
            self.calibrated = False
            self.measurements = {
                'x': [],
                'y': [],
                'z': [],
                'x_orientation': [],
                'y_orientation': [],
                'z_orientation': [],
                'w_orientation': []
            }

            #Esperar a que haya 50 measurements
            print("[Astra Camera]      Calibrating...")
            while len(self.measurements['x']) < 50:
                rospy.sleep(0.1)

            self.calculate_calibration()
            # Publicar que la calibración ha sido realizada
            self.calibrated = True
            self.calibration_pub.publish(True)


    def collect_measurements_callback(self, msg):
        if self.calibrated: return

        # Obtener las posiciones y orientaciones de la aruco
        arucos_data = msg.data[:-1]
        aruco_info = arucos_data.split(':')
        id_aruco, x_aux, y_aux, z_aux, x_orientation_aux, y_orientation_aux, z_orientation_aux, w_orientation_aux = map(float, aruco_info)
        self.measurements['x'].append(x_aux)
        self.measurements['y'].append(y_aux)
        self.measurements['z'].append(z_aux)
        self.measurements['x_orientation'].append(x_orientation_aux)
        self.measurements['y_orientation'].append(y_orientation_aux)
        self.measurements['z_orientation'].append(z_orientation_aux)
        self.measurements['w_orientation'].append(w_orientation_aux)

    def calculate_calibration(self):
        x_mode, x_count = Counter(self.measurements['x']).most_common(1)[0]
        y_mode, y_count = Counter(self.measurements['y']).most_common(1)[0]
        z_mode, z_count = Counter(self.measurements['z']).most_common(1)[0]
        x_orientation_mode, x_orientation_count = Counter(self.measurements['x_orientation']).most_common(1)[0]
        y_orientation_mode, y_orientation_count = Counter(self.measurements['y_orientation']).most_common(1)[0]
        z_orientation_mode, z_orientation_count = Counter(self.measurements['z_orientation']).most_common(1)[0]
        w_orientation_mode, w_orientation_count = Counter(self.measurements['w_orientation']).most_common(1)[0]

        # Usar las modas como valores de calibración
        self.x = x_mode
        self.y = y_mode
        self.z = z_mode
        self.x_orientation = x_orientation_mode
        self.y_orientation = y_orientation_mode
        self.z_orientation = z_orientation_mode
        self.w_orientation = w_orientation_mode

        print("[Astra Camera]      Calibrated:")
        print(f"[Astra Camera]          X: {x_mode} (mode: {x_count}), Y: {y_mode} (mode: {y_count}), Z: {z_mode} (mode: {z_count})")
        print(f"[Astra Camera]          Orientation - X: {x_orientation_mode} (mode: {x_orientation_count}), "
        f"Y: {y_orientation_mode} (mode: {y_orientation_count}), "
        f"Z: {z_orientation_mode} (mode: {z_orientation_count}), "
        f"W: {w_orientation_mode} (mode: {w_orientation_count})")


    def publish_loop(self):
        while not rospy.is_shutdown():
            if self.calibrated:
                t_nueva = geometry_msgs.msg.TransformStamped()
                t_nueva.header.stamp = rospy.Time.now()
                t_nueva.header.frame_id = "aruco_frame"
                t_nueva.child_frame_id = "world"
                t_nueva.transform.translation.x = 0.08
                t_nueva.transform.translation.y = -0.06
                t_nueva.transform.translation.z = 0.00
                t_nueva.transform.rotation.x = 0
                t_nueva.transform.rotation.y = 0
                t_nueva.transform.rotation.z = 0
                t_nueva.transform.rotation.w = 1

                # Convertir la rotación inicial a cuaternión
                quat = (
                    t_nueva.transform.rotation.x,
                    t_nueva.transform.rotation.y,
                    t_nueva.transform.rotation.z,
                    t_nueva.transform.rotation.w
                )

                rot_desired = transformations.quaternion_about_axis(90 * (3.14159 / 180), (0, 0, 1))  # Convertir grados a radianes
                quat_rotated = transformations.quaternion_multiply(quat, rot_desired)
                rot_desired = transformations.quaternion_about_axis(-90 * (3.14159 / 180), (1, 0, 0))
                quat_rotated = transformations.quaternion_multiply(quat_rotated, rot_desired)

                t_nueva.transform.rotation.x = quat_rotated[0]
                t_nueva.transform.rotation.y = quat_rotated[1]
                t_nueva.transform.rotation.z = quat_rotated[2]
                t_nueva.transform.rotation.w = quat_rotated[3]

                self.broadcaster.sendTransform(t_nueva)

                t_camera_marker = geometry_msgs.msg.TransformStamped()
                t_camera_marker.header.stamp = rospy.Time.now()
                t_camera_marker.header.frame_id = "camera_link"
                t_camera_marker.child_frame_id = "aruco_frame"
                t_camera_marker.transform.translation.x = self.x
                t_camera_marker.transform.translation.y = self.y
                t_camera_marker.transform.translation.z = self.z
                t_camera_marker.transform.rotation.x = self.x_orientation
                t_camera_marker.transform.rotation.y = self.y_orientation
                t_camera_marker.transform.rotation.z = self.z_orientation
                t_camera_marker.transform.rotation.w = self.w_orientation

                self.broadcaster.sendTransform(t_camera_marker)


if __name__ == '__main__':
    camera = Camera(id_aruco_calibration=8)
    camera.publish_loop()
    rospy.spin()
