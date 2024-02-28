import numpy as np
import cv2

img= cv2.imread('cam.jpg', cv2.IMREAD_GRAYSCALE)
print img.shape # Size of image (rows, columns, channels if color image)
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.imshow('Image', img)
k=cv2.waitKey(0) & 0xFF
if k == ord('s'): # 's' key
	cv2.imwrite('camGray.png', img)
cv2.destroyAllWindows()
