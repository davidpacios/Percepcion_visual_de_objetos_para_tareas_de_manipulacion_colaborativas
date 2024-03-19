#! /usr/bin/env python3
import sys, time

# numpy and scipy
import numpy as np

# OpenCV
import cv2

# Ros libraries
import rospy

# Ros Messages
from sensor_msgs.msg import CompressedImage
# We do not use cv_bridge it does not support CompressedImage in python
# from cv_bridge import CvBridge, CvBridgeError

VERBOSE=True
SHOW=True

class image_feature:

    def __init__(self):
        self.image_pub = rospy.Publisher("/output/image_raw/compressed",CompressedImage, queue_size=10)
        self.subscriber = rospy.Subscriber("/camera/image/compressed",
            CompressedImage, self.callback,  queue_size = 1)
        
        if VERBOSE :
            print ("subscribed to /camera/image/compressed")


    def callback(self, ros_data):
        '''Callback function of subscribed topic. 
        Here images get converted and features detected'''
        if VERBOSE :
            print ('received image of type: "%s"' % ros_data.format)

        #direct conversion to CV2
        np_arr = np.fromstring(ros_data.data, np.uint8)

        #image_np = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)
        image_np = cv2.imdecode(np_arr, cv2.COLOR_BGR2GRAY)
        #image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR) # OpenCV >= 3.0:

        if SHOW:
            cv2.imshow('cv_img', image_np)
            cv2.waitKey(2)

        #Create CompressedImage
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpg"
        msg.data = np.array(cv2.imencode('.jpg', image_np)[1]).tostring()
        self.image_pub.publish(msg)
        
        #self.subscriber.unregister()

def main(args):
    '''Initializes and cleanup ros node'''
    ic = image_feature()
    rospy.init_node('image_feature', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print ("Shutting down ROS Image view module")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
