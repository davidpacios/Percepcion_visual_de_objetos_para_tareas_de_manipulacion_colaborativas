import numpy as np
import cv2

cap = cv2.VideoCapture(0)

width= cap.get(cv2.CAP_PROP_FRAME_WIDTH) # Older: cv2.cv.CV_CAP_PROP_FRAME_WIDTH
height= cap.get(cv2.CAP_PROP_FRAME_HEIGHT)# Older: cv2.cv.CV_CAP_PROP_FRAME_HEIGHT
print("size= %d x %d;" % (width, height))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width/2)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height/2)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
