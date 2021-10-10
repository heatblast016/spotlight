import cv2
import numpy as np

image = np.zeros((100, 200, 3), np.uint8)
cv2.imshow('image window', image)
print(image)
cv2.waitKey(0)

for i in range(200):
    image[20][i][0] = 255
    image[20][i][1] = 255
    image[20][i][2] = 255
    
cv2.imshow('image window', image)
cv2.waitKey(0)