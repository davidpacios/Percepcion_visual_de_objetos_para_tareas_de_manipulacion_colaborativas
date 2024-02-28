import cv2
import numpy as np

def draw_circle(event, x, y, flags, param): # mouse callback
	if event == cv2.EVENT_LBUTTONDBLCLK:
		cv2.circle(img, (x,y), 50, (255, 0, 0), -1)

img = np.zeros((512,512,3), np.uint8) # black 512x512 image
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

while(True):
	cv2.imshow('image',img)
	if cv2.waitKey(1) & 0xFF == 27:
		break

cv2.destroyAllWindows()
