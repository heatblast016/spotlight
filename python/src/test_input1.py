from RoomLayout import RoomLayout
import sys
import matplotlib.pyplot as plt
import numpy as np

room = RoomLayout(sys.argv[1])
print('dimensions: ', room.dimensions)
print('camera:     ', room.camera)
print('lights:     ', room.lights)

humans = [(3, 4), (-2, 8)]  # my fake GetHumanLocs()
print('humans:     ', room.people)

# set up the graph    
"""
fig, ax = plt.subplots()

plt.ion()
for i in range(50):
    room.RefreshRoom(ax, humans)
    plt.xlim([0, room.dimensions[0]])
    plt.ylim([0, room.dimensions[1]])
    plt.gca().set_aspect('equal', adjustable='box')
    fig.canvas.draw()
    time.sleep(0.5)
    fig.canvas.flush_events()
    plt.cla()
"""

human1 = [(-5, 0)]
for i in range(1000):
    room.RefreshRoom(human1, 1)
    