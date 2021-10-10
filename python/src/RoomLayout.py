import csv
import matplotlib.pyplot as plt
plt.ion()
import matplotlib.patches as patches
import numpy as np
import time

class RoomLayout:
    dimensions = None   # (x, z)
    camera = None       # (x, z) - points upwards
    lights = []         # [[x1, z1, current power (? / 100), goal power (? / 100)], ...]
    people = []         # [(x1, z1), ...]

    MAX_LIGHT_ALPHA = 0.4 * 0.01
    MAX_LIGHT_RAD = 5 * 0.01

    fig, ax = plt.subplots()

    def __init__(self, FileName):
        with open(FileName, 'r') as input:
            reader = csv.reader(input, delimiter=' ')
            
            row1 = next(reader)
            self.dimensions = (float(row1[0]), float(row1[1]))
            row2 = next(reader)
            self.camera = (float(row2[0]), float(row2[1]))
            
            for line in reader:
                self.lights.append([float(line[0]), float(line[1]), 0, 100])
    
    def RefreshPeople(self, locs):
        self.people = []
        for i in range(len(locs)):
            self.people.append((self.camera[0] + locs[i][0],
                                self.camera[1] + locs[i][1]))

    def RefreshRoom(self, PeopleLocs):
        # add points for people
        self.RefreshPeople(PeopleLocs)
        for person in self.people:
            self.ax.plot(person[0], person[1], 'r+')
        
        # TODO: calculate goal powers

        # draw the light circles
        for light in self.lights:
            # adjust light power towards goal
            if light[2] < light[3]:
                light[2] += 10
            elif light[2] > light[3]:
                light[2] -= 10
            
            # draw the light circle
            circle = patches.Circle((light[0], light[1]),
                                        light[2] * RoomLayout.MAX_LIGHT_RAD,
                                        alpha = light[2] * RoomLayout.MAX_LIGHT_ALPHA,
                                        color = 'y')
            self.ax.add_patch(circle)

        plt.xlim([0, self.dimensions[0]])
        plt.ylim([0, self.dimensions[1]])
        plt.gca().set_aspect('equal', adjustable='box')
        self.fig.canvas.draw()
        time.sleep(0.5)
        self.fig.canvas.flush_events()
        plt.cla()
