# https://stackoverflow.com/questions/10958835/matplotlib-color-gradient-in-patches
# https://stackoverflow.com/questions/11874767/how-do-i-plot-in-real-time-in-a-while-loop-using-matplotlib

import matplotlib.pyplot as plt
import numpy as np
import cv2

class DrawRoom:
    def __init__(self, room, imshow):
        graph = [10 * ][][3]
        graph.fill(255)

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