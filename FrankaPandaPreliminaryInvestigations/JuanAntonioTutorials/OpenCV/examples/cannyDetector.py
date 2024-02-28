import cv2
import numpy as np

img= cv2.imread('cam.jpg')
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # Change to gray

def nothing(x):
	pass

cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.namedWindow('blurw',cv2.WINDOW_NORMAL)
cv2.createTrackbar('th1','image',0,255,nothing)
cv2.createTrackbar('th2','image',0,255,nothing)
cv2.createTrackbar('blur','image',1,100,nothing)

while(True):
	th1=cv2.getTrackbarPos('th1','image')
	th2=cv2.getTrackbarPos('th2','image')
	size= cv2.getTrackbarPos('blur','image')
	kernel=np.ones((size,size),np.float32)/(size*size)
	filteredGray= cv2.filter2D(gray,-1,kernel) #Convolution with kernel
	edges=cv2.Canny(filteredGray,th1,th2) # Corners detection with Canny
	cv2.imshow('image',edges)
	cv2.imshow('blurw',filteredGray)
	if cv2.waitKey(1) & 0xFF == 27:
		break
		
cv2.destroyAllWindows()
