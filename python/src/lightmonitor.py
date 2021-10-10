import numpy as np
import math
import cv2
from random import randrange
class LightMonitor():
    def __init__(self):
        self.cam = cv2.VideoCapture(1)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        self.cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        self.cam.set(cv2.CAP_PROP_EXPOSURE, 0.01)
        self.cam.set(cv2.CAP_PROP_BRIGHTNESS, 50)
        self.cam.set(cv2.CAP_PROP_SATURATION, 50)
    def getBrightness(self):
        average = 0 
        ret, frame = self.cam.read()
        bwframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurframe = cv2.blur(bwframe, (200,200))
        cv2.imshow('Brightness sensor', blurframe)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          return 0
        for i in range(100):
            x, y = randrange(639), randrange(479)
            average += bwframe[y,x]
            average = average/100             
        return average

#Testing Code
#lm = lightmonitor()
#while True:
#    print(lm.getBrightness()) 
     
    