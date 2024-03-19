#! /usr/bin/env python3

from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2
import rospy

from sensor_msgs.msg import CompressedImage

SHOW=False

def cam_node():
    image_pub = rospy.Publisher("/camera/image/compressed", CompressedImage, queue_size=1)

    rospy.init_node('cam_node', anonymous=True)
    
    camera=PiCamera()
    camera.resolution=(640,480)
    camera.framerate = 32
    camera.rotation=0
    rawCapture=PiRGBArray(camera,size=(640, 480))
    
    time.sleep(0.1)

    rate = rospy.Rate(30) # 10hz

    
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
	    # and occupied/unoccupied text
        
        image = frame.array

	    # show the frame
        if SHOW:
            cv2.imshow("Frame", image)
            cv2.waitKey(1)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpg"
        msg.data = np.array(cv2.imencode('.jpg', gray)[1]).tostring()

        image_pub.publish(msg)

	    # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

    camera.close()

if __name__ == '__main__':
    try:
        cam_node()
    except rospy.ROSInterruptException:
        pass
