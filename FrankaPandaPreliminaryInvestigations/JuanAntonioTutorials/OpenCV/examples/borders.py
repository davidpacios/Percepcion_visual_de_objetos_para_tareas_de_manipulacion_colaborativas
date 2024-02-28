import cv2
import numpy as np

# Border operations need to work with
# 64-bit floating numbers for detecting
# positive/negative slopes in gradient
ddepth = cv2.CV_64F

img = cv2.imread('sudoku.jpg')
img = cv2.GaussianBlur(img,(3,3),0)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow('original',gray)

# Laplacian
laplacian = cv2.Laplacian(gray,ddepth)

# Sobel Gradient-X
grad_x = cv2.Sobel(gray,ddepth,1,0,ksize = 3)
# Sobel Gradient-Y
grad_y = cv2.Sobel(gray,ddepth,0,1,ksize = 3)


# Converting back from 64-bit floating-point (CV_64F)
# into original 8-bit unsigned integers (CV_8U)
abs_grad_x = cv2.convertScaleAbs(grad_x)  
abs_grad_y = cv2.convertScaleAbs(grad_y)
abs_laplacian = cv2.convertScaleAbs(laplacian)
cv2.imshow('SobelX',abs_grad_x)
cv2.imshow('SobelY',abs_grad_y)
cv2.imshow('Laplacian',abs_laplacian)

# Combining both gradients into one Sobel image
dst = cv2.addWeighted(abs_grad_x,0.5,abs_grad_y,0.5,0)
cv2.imshow('SobelXY',dst)

cv2.waitKey(0)
cv2.destroyAllWindows()
