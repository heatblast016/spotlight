#Imports
from RoomLayout import RoomLayout
from Perception import Perception
from LightMonitor import LightMonitor
import pyrealsense2 as rs
import sys
import matplotlib.pyplot as plt
import numpy as np
import cv2
import math

#TODO think of funny variable names
perception = Perception()
#lm = LightMonitor()
room = RoomLayout(sys.argv[1])

def convertCoords(triple):
    if(triple):
        return (triple[0], triple[2])
    return []

while True:
    perception.update()    
    hoomans = perception.getHumans()
    if(hoomans):
        for hooman in hoomans:
            humanArray.append(convertCoords(hooman))
    else:
        humanArray = hoomans
    brightnessFactor = 1.0 #-((lm.getBrightness())/2.55)
    room.RefreshRoom(humanArray, brightnessFactor)
