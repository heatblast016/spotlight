import csv
import matplotlib.pyplot as plt
import numpy as np

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
    
    def PlaceHuman(self, locs):
        self.lights = []
        for i in range(len(locs)):
            self.humans.append((self.camera[0] + locs[i][0],
                                self.camera[1] + locs[i][1]))
    
    def DrawRoom(self):
        fig, ax = plt.subplots()  # Create a figure containing a single axes.
      
        plt.xlim([0, self.dimensions[0]])
        plt.ylim([0, self.dimensions[1]])
        plt.gca().set_aspect('equal', adjustable='box')
        
        
        for person in self.humans:
            ax.plot(person[0], person[1], 'r+')
        

        plt.draw()
        plt.pause(3)
        plt.clf()
