import time
import cv2
import numpy as np

# Initialize the camera and grab a reference to the raw camera capture
cap = cv2.VideoCapture(0)

# Allow the camera to warmup
time.sleep(0.1)

# Define the windows where color sliders and images will be shown
def nothing(x):
	pass
cv2.namedWindow("w_threshold")
cv2.namedWindow("w_frame")

# Trackbars for min and max thresholds for HSV components
cv2.createTrackbar("Hmin", "w_threshold",0,179,nothing)
cv2.createTrackbar("Hmax", "w_threshold",0,179,nothing)
cv2.createTrackbar("Smin", "w_threshold",0,255,nothing)
cv2.createTrackbar("Smax", "w_threshold",255,255,nothing)
cv2.createTrackbar("Vmin", "w_threshold",0,255,nothing)
cv2.createTrackbar("Vmax", "w_threshold",255,255,nothing)

drawing = False
ix,iy = -1, -1
# Callback for showing Hue value where double click on the image
def draw_hue(event,x,y,flags,param):
	global ix,iy,drawing
	if event == cv2.EVENT_LBUTTONDBLCLK:
		ix,iy = x,y
		drawing = True

cv2.setMouseCallback("w_frame",draw_hue)

while(True):
	# grab the raw NumPy array representing the image
	ret, image = cap.read()	
	
	# Blur the source image to reduce color noise
	blur = cv2.blur(image,(3,3))
	
	# Convert the image to HSV (Hue, Saturation, Value) model
	hsv= cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
	
	global ix,iy,drawing
	if drawing == True:
		p = hsv[ix,iy]
		print "HSV-Pixel(",ix,",",iy,")=(",p[0],",",p[1],",",p[2],")"
		drawing = False
	
	# Get HSV thresholds from trackbars
	hmin = cv2.getTrackbarPos("Hmin","w_threshold")
	hmax = cv2.getTrackbarPos("Hmax","w_threshold")
	smin = cv2.getTrackbarPos("Smin","w_threshold")
	smax = cv2.getTrackbarPos("Smax","w_threshold")
	vmin = cv2.getTrackbarPos("Vmin","w_threshold")
	vmax = cv2.getTrackbarPos("Vmax","w_threshold")
	
	# Establish the lower and upper thresholds for binarization of image
	lower = np.array((hmin,smin,vmin))
	upper = np.array((hmax,smax,vmax))
	
	# Binarization of HSV image with previous thresholds
	mask = cv2.inRange(hsv,lower,upper)

	# Combination of binary image and original one
	maskColor= cv2.bitwise_and(image,image,mask=mask)

	# Find contours in the threshold images
	_,contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	
	# Find contour with maximum area and store it as best_cnt
	max_area = 0
	best_cnt = None
	for cnt in contours:
		area = cv2.contourArea(cnt)
		if area > max_area:
			max_area = area
			best_cnt = cnt
	if best_cnt is not None:
		# Calculate moments of the biggest contour
		M = cv2.moments(best_cnt)
		# Verify that the area is big enough to consider it as an object
		if M["m00"] > 1000: 
			# Centroid
			cx, cy = int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"])
			cv2.circle(image,(cx,cy),10,(0,0,255),-1)
			rect = cv2.minAreaRect(best_cnt)
			#box = cv2.cv.BoxPoints(rect)
			#box = cv2.BoxPoints(rect)
			#box = np.int0(box)
			#cv2.drawContours(image,[box],0,(0,0,255),2)
	# Show result of binarization
	cv2.imshow("w_threshold",maskColor)
	cv2.imshow("w_frame",image)
	
	key = cv2.waitKey(1) & 0xFF
	#if the "q" key is pressed, finish loop
	if key == ord("q"):
		break
		
cv2.destroyAllWindows()
	
