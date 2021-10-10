import csv

import matplotlib.pyplot as plt
plt.ion()
import matplotlib.patches as patches

import math
import numpy as np

import time

class RoomLayout:
    MAX_LIGHT_ALPHA = 0.4
    MAX_LIGHT_RAD = 5
    POLLING_RATE = 0.05
    MAX_HUMAN_RAD = 5
    
    dimensions = None   # (x, z)
    camera = None       # (x, z) - points upwards
    lights = []         # [[x1, z1, current power (? / 100), goal power (? / 100)], ...]
    people = []         # [(x1, z1), ...]

    UsedEnergy = 0
    RegEnergy = 0

    fig, ax = plt.subplots()

    def dist(self, point1, point2):
        return ((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)**0.5

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

    def ClosestLightDist(self, PersonLoc):
        ClosestLight = -1
        for light in self.lights:
            loc = (light[0], light[1])
            if (ClosestLight == -1 or self.dist(loc, PersonLoc) < self.dist(ClosestLight, PersonLoc)):
                ClosestLight = loc
        return self.dist(ClosestLight, PersonLoc)


    def RefreshLights(self, ExternalLightFctr):
        for light in self.lights:
            light[3] = 0
        for person in self.people:
            MinDist = self.ClosestLightDist(person)
            if (MinDist < RoomLayout.MAX_HUMAN_RAD):
                for i in range(len(self.lights)):
                    CurDist = self.dist((self.lights[i][0], self.lights[i][1]), person)
                    if CurDist <= RoomLayout.MAX_HUMAN_RAD:
                        ScaledVal = int((RoomLayout.MAX_HUMAN_RAD - CurDist) /
                                                (RoomLayout.MAX_HUMAN_RAD - MinDist) * 100)
                        if ScaledVal > self.lights[i][3]:
                            self.lights[i][3] = ScaledVal
            else:
                for i in range(len(self.lights)):
                    CurDist = self.dist((self.lights[i][0], self.lights[i][1]), person)
                    if CurDist == MinDist:
                        self.lights[i][3] = 100
        for light in self.lights:
            light[3] *= ExternalLightFctr

    def RefreshRoom(self, PeopleLocs, ExternalLightFctr):
        # add points for people
        self.RefreshPeople(PeopleLocs)
        for person in self.people:
            self.ax.plot(person[0], person[1], 'r+')
        
        self.ax.plot(self.camera[0], self.camera[1], 'g^')
        
        self.RefreshLights(ExternalLightFctr)
        for light in self.lights:
            # adjust light power towards goal
            if light[3] - light[2] > 1:
                light[2] += 2
            elif light[2] - light[3] > 1:
                light[2] -= 2
            
            self.ax.plot(light[0], light[1], 'bo')
            # draw the light circle
            circle = patches.Circle((light[0], light[1]),
                                        light[2] * 0.01 * RoomLayout.MAX_LIGHT_RAD,
                                        alpha = light[2] * 0.01 * RoomLayout.MAX_LIGHT_ALPHA,
                                        color = 'y')
            self.ax.add_patch(circle)

        # calcualte energy saving
        for light in self.lights:
            self.UsedEnergy += (light[2] / 100)
        self.RegEnergy += len(self.lights)
        text = 'Energy Saving: ' + ''.join(r'$%2.2f$' % ((self.RegEnergy - self.UsedEnergy) / self.RegEnergy * 100)) + '%'

        plt.annotate(text, xy=(1, 1), xytext=(-5, -5), fontsize=8,
                     xycoords='axes fraction', textcoords='offset points',
                     horizontalalignment='right', verticalalignment='top')

        plt.xlim([0, self.dimensions[0]])
        plt.ylim([0, self.dimensions[1]])
        plt.gca().set_aspect('equal', adjustable='box')
        self.fig.canvas.draw()
        time.sleep(RoomLayout.POLLING_RATE)
        self.fig.canvas.flush_events()
        plt.cla()
