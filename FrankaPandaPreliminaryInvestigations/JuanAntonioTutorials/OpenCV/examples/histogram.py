import cv2
import numpy as np
from matplotlib import pyplot as plt
img = cv2.imread('dark.png')
color = ('b','g','r')

for i,col in enumerate(color):
  histr = cv2.calcHist([img],[i],None,[256],[0,256])
  plt.plot(histr,color = col)
  plt.xlim([0,256])

gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
histr_gray= cv2.calcHist([gray],[0], None,[256],[0,256])
plt.plot(histr_gray,color='k') # Black plot

# histogram equalization
equ = cv2.equalizeHist(gray)
histr_equ= cv2.calcHist([equ],[0], None,[256],[0,256])
plt.plot(histr_equ,color='m') # Magenta plot 

cv2.imshow('src',gray)
cv2.imshow('equ',equ)
plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()
