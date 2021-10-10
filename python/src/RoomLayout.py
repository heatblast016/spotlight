import csv
import matplotlib.pyplot as plt
import numpy as np

class RoomLayout:
    dimensions = None   # (x, z)
    camera = None       # (x, z) - points upwards
    lights = []         # [(x1, z1, current power, goal power), ...]
    people = []         # [(x1, z1), ...]

    def __init__(self, FileName):
        with open(FileName, 'r') as input:
            reader = csv.reader(input, delimiter=' ')
            
            row1 = next(reader)
            self.dimensions = (float(row1[0]), float(row1[1]))
            row2 = next(reader)
            self.camera = (float(row2[0]), float(row2[1]))
            
            for line in reader:
                self.lights.append((float(line[0]), float(line[1]), 0, 0))
    
    def RefreshPeople(self, locs):
        self.people = []
        for i in range(len(locs)):
            self.people.append((self.camera[0] + locs[i][0],
                                self.camera[1] + locs[i][1]))

    def DrawRoom(self):
        # set up the graph      
        fig, ax = plt.subplots()
        plt.xlim([0, self.dimensions[0]])
        plt.ylim([0, self.dimensions[1]])
        plt.gca().set_aspect('equal', adjustable='box')
        
        # add points for people
        for person in self.people:
            ax.plot(person[0], person[1], 'r+')
        
        # 

        plt.draw()
        # move these to main:
            # plt.pause(3)
            # plt.clf()
