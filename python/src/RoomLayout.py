import csv
import numpy as np
import cv2

class RoomLayout:
    dimensions = None
    camera = None
    lights = []
    humans = []
    graph = None

    def __init__(self, FileName):
        with open(FileName, 'r') as input:
            reader = csv.reader(input, delimiter=' ')
            
            row1 = next(reader)
            self.dimensions = (float(row1[0]), float(row1[1]))
            row2 = next(reader)
            self.camera = (float(row2[0]), float(row2[1]))
            
            for line in reader:
                self.lights.append((float(line[0]), float(line[1])))

        GraphWidth = int(10 * (self.dimensions[0] + 2))
        GraphHeight = int(10 * (self.dimensions[1] + 2))
        
        self.graph = np.zeros((GraphHeight, GraphWidth, 3), np.uint8)
        self.graph.fill(255)

        for i in range(9, GraphWidth - 9):
            self.graph[9][i] = [0, 0, 0]
            self.graph[GraphHeight - 9][i] = [0, 0, 0]

        for i in range(9, GraphHeight - 9):
            self.graph[i][9] = [0, 0, 0]
            self.graph[i][GraphWidth - 9] = [0, 0, 0]


    
    def PlaceHuman(self, locs):
        self.lights = []
        for i in range(len(locs)):
            self.humans.append((self.camera[0] + locs[i][0],
                                self.camera[1] + locs[i][1]))
    
    def DrawRoom(self, LightScalars):

        
        
        # scale the image
        scale_percent = 220 # percent of original size
        width = int(self.graph.shape[1] * scale_percent / 100)
        height = int(self.graph.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(self.graph, dim, interpolation = cv2.INTER_AREA)
        cv2.imshow('room', resized)
        cv2.waitKey(0)