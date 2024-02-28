from picamera.array import PiRGBArray
from picamera import PiCamera
import time, cv2

camera= PiCamera()
camera.resolution= (320,240)
rawCapture = PiRGBArray(camera, size=(320,240))
time.sleep(2) # Allow the camera to warmup

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
	image= frame.array # Get raw NumPy array of the frame
	cv2.imshow('Frame',image) # Show frame
	rawCapture.truncate(0) # Clear stream for next frame
	if cv2.waitKey(1) & 0xFF == 27: # ESC key
		break
cv2.destroyAllWindows()
