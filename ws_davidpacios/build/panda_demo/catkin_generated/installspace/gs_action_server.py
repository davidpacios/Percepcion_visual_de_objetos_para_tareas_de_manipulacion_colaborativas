#!/usr/bin/env python3
from __future__ import print_function
from six.moves import input

import cv2
import numpy as np
import rospy

from std_msgs.msg import Float32
import actionlib
from panda_demo.msg import GsAction, GsResult, GsFeedback

class GellsightAction(object):
    def __init__(self, action_server_name):
        # Start Action server
        self.action_server = actionlib.SimpleActionServer(action_server_name, GsAction, auto_start=False)
        # Set the callback to be executed when a goal is received
        self.action_server.register_goal_callback(self.goal_callback)
        # Set the callback that should be executed when a preempt request is received
        self.action_server.register_preempt_callback(self.preempt_callback)
        # Start the server
        self.action_server.start()

        # Start camera
        self.cap = cv2.VideoCapture(-1,cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        width = 3280
        height = 2464
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # Filter parameters
        self.threshold = 1.2
        self.n_calibrating = 10

        # Initialize parameters
        self.freeze = False
        self.dist_calibration = [0]*self.n_calibrating
        self.avg_dist = 0
        # Calibrate
        self.calibrate()

        # Start filming
        self.loop()
    
    def __del__(self):
        print("-----Releasing camera")
        self.cap.release()
        cv2.destroyAllWindows()

    # Filter to be applied to each frames
    def filter_image(self,img):
        border = 200
        cropped_image = img[border:2464-border, border:3280-border]
        return cv2.medianBlur(cropped_image,3)

    # Compute distance between two frames
    def compute_max_distance(self,img1, img2):
        h, w = img1.shape[0:2]
        diff = cv2.subtract(img1, img2)
        diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        dist = np.max(diff)
        self.diff = diff
        return dist

    # Calibrate the Camera
    def calibrate(self):
        print("-----Calibrating...")
        print("Don't touch the gelsight")

        first_ret = False
        t0 = rospy.get_time()
        throw_away = 10
        # Wait for the first frames to be captured and toss away the first frames
        while not(first_ret and throw_away <= 0):
            first_ret, self.first_frame = self.cap.read()
            if first_ret: throw_away -= 1
            if (rospy.get_time() - t0) > 3 :
                print("Error Could not capture image")
                break
        
        self.first_frame = self.filter_image(self.first_frame)

        # Compute the average distance between two frames while the Gs is not touched
        for i in range(self.n_calibrating):
            ret, self.frame = self.cap.read()
            self.frame = self.filter_image(self.frame)
            self.dist_calibration[i] = self.compute_max_distance(self.first_frame,self.frame)

        self.avg_dist = sum(self.dist_calibration)/self.n_calibrating

        print("-----Calibration Complete")
        print("Default max distance =",self.avg_dist/255*100)

    # Search for the pixel with the most distance
    def get_max_distance(self):
        if (self.cap.isOpened()):
            ret, self.frame = self.cap.read()
            self.frame = self.filter_image(self.frame)
            dist = self.compute_max_distance(self.first_frame,self.frame)

            distance_percent = max(0,dist - self.avg_dist*self.threshold)/255*100

            return distance_percent
        else :
            print("Error Capture is closed")
            return
        
    def loop(self):

        pub = rospy.Publisher('gs_max_distance', Float32, queue_size=0)

        while True:

            if not self.freeze:
                max_dist = self.get_max_distance()
                pub.publish(Float32(max_dist))
                cv2.imshow('Pic',cv2.resize(self.frame,(960,540)))

                if cv2.waitKey(1) == ord('q') or rospy.is_shutdown():
                    break

    # Callback
    def goal_callback(self):
        
        # start with the new goal
        self.action_server.accept_new_goal()

        #calibrate
        self.freeze = True
        self.calibrate()

        # feedback
        action_feedback = GsFeedback()
        action_feedback.calibrated = True
        # Publish the feedback
        self.action_server.publish_feedback(action_feedback)

        # Return the response of the action
        self.action_result = GsResult()
        self.action_result.distance = self.avg_dist
        self.action_server.set_succeeded(self.action_result)

        # Unfreeze the camera
        self.freeze = False
        

    def preempt_callback(self):
        """
            Callback executed when a preempt request has been received.
        """
        # You can add some code here if you need to perform some specific operations when a preemption request is sent
        self.action_server.set_preempted()

if __name__ == '__main__':
    rospy.init_node('gs_action_server')
    server = GellsightAction('gs_action')
    rospy.spin()