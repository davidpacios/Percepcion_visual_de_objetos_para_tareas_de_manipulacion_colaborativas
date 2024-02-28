import cv2
import numpy as np

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.namedWindow('roi', cv2.WINDOW_AUTOSIZE)
img= cv2.imread('cam.jpg')
cv2.imshow('image',img)
drag=False
point1=None
point2=None
selection=False

def choose_roi(event, x, y, flags, param): # mouse callback
	global drag, point1, point2, selection
	img2= img.copy()
	if event==cv2.EVENT_LBUTTONDOWN:
		point1=(x,y)
		drag=True
		print point1
	if event == cv2.EVENT_MOUSEMOVE and drag:
		point2=(x,y)
		cv2.rectangle(img2, point1, point2, (0,0,255),4)
		print point2
	if event == cv2.EVENT_LBUTTONUP and drag:
		point2=(x,y)
		cv2.rectangle(img2, point1, point2, (0,0,255),4)
		selection=True
		drag=False
		print point2
	cv2.imshow('image',img2)

cv2.setMouseCallback('image', choose_roi)
		
while(True):
	if selection:
		cv2.imshow('roi',img[min(point1[1],point2[1]):max(point1[1],point2[1]),min(point1[0],point2[0]):max(point1[0],point2[0])])
		selection= False
	if cv2.waitKey(1) & 0xFF == 27: # ESC key
		break
		
cv2.destroyAllWindows()
