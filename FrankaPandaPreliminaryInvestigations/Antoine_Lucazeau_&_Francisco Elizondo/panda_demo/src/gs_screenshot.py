from __future__ import print_function
from six.moves import input

import cv2
import rospy
import numpy as np
from std_msgs.msg import Float32

class PressureEstimator:

    def __init__(self):

        self.cap = cv2.VideoCapture(-1,cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        width = 3280
        height = 2464
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.threshold = 1.2
        self.n_calibrating = 10

        #Initialize parameters
        self.dist_calibration = [0]*self.n_calibrating
        self.avg_dist = 0
        #Calibrate
        self.calibrate()

    def __del__(self):
        print("-----Releasing camera")
        self.cap.release()

    def filter_image(self,img):
        border = 200
        cropped_image = img[border:2464-border, border:3280-border]
        return cv2.medianBlur(cropped_image,3)

    def compute_max_distance(self,img1, img2):
        h, w = img1.shape[0:2]
        diff = cv2.subtract(img1, img2)
        diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        dist = np.max(diff)
        self.diff = diff
        return dist

    def calibrate(self):
        print("-----Calibrating...")
        print("Don't touch the gelsight")

        first_ret = False
        t0 = rospy.get_time()
        throw_away = 10

        while not(first_ret and throw_away <= 0):
            first_ret, self.first_frame = self.cap.read()
            throw_away -= 1
            if (rospy.get_time() - t0) > 3 :
                print("Error Could not capture image")
                break
        
        self.first_frame = self.filter_image(self.first_frame)

        for i in range(self.n_calibrating):
            ret, self.frame = self.cap.read()
            self.frame = self.filter_image(self.frame)
            self.dist_calibration[i] = self.compute_max_distance(self.first_frame,self.frame)

        self.avg_dist = sum(self.dist_calibration)/self.n_calibrating

        print("-----Calibration Complete")
        print("Default max distance =",self.avg_dist/255*100)
    
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

    def handle_gs_max(self,_):
        max_dist = self.get_max_distance()
        print("Maximum distance = ",max_dist)
        return max_dist



def main():

    rospy.init_node("gs_screenshot", anonymous=True)
    pressure_estimator = PressureEstimator()
    print("-----Ready to use the gellsight. Press q to exit")
    
    # s = rospy.Service('gs_max_distance', GsMax, pressure_estimator.handle_gs_max)
    # rospy.spin()
    pub = rospy.Publisher('gs_max_distance', Float32, queue_size=0)

    while True:

        max_dist = pressure_estimator.get_max_distance()
        cv2.imshow('Pic',cv2.resize(pressure_estimator.frame,(960,540)))
        pub.publish(Float32(max_dist))

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass