import cv2
import numpy as np

img = cv2.imread('bike.jpg')
cv2.imshow('original',img)

# 2D convolution with 5x5 mean kernel
kernel = np.ones((5,5),np.float32)/25
filtered2D = cv2.filter2D(img,-1,kernel)
cv2.imshow('5x5 convolution',filtered2D)

# Blur with 5x5 kernel (equal to 2D convolution)
blur = cv2.blur(img,(5,5))
cv2.imshow('5x5 blur',blur)

# Gaussian blur
GaussianBlur = cv2.GaussianBlur(img,(5,5),0)
cv2.imshow('5x5 Gaussian blur', GaussianBlur)

# Median blur
median = cv2.medianBlur(img,5)
cv2.imshow('5x5 median', median)

cv2.waitKey(0)
cv2.destroyAllWindows()
