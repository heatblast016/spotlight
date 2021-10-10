# https://stackoverflow.com/questions/10958835/matplotlib-color-gradient-in-patches
# https://stackoverflow.com/questions/11874767/how-do-i-plot-in-real-time-in-a-while-loop-using-matplotlib

import matplotlib.pyplot as plt
import numpy as np
import time

def gauplot(centers, radiuses, xr=None, yr=None):
    nx, ny = 1000.,1000.
    xgrid, ygrid = np.mgrid[xr[0]:xr[1]:(xr[1]-xr[0])/nx,yr[0]:yr[1]:(yr[1]-yr[0])/ny]
    im = xgrid*0 + np.nan
    xs = np.array([np.nan])
    ys = np.array([np.nan])
    fis = np.concatenate((np.linspace(-np.pi,np.pi,100), [np.nan]) )
    cmap = plt.cm.gray
    cmap = plt.cm.get_cmap("gray").copy()
    cmap.set_bad('white')
    thresh = 3
    for curcen,currad in zip(centers,radiuses):
        curim=(((xgrid-curcen[0])**2+(ygrid-curcen[1])**2)**.5)/currad*thresh
        im[curim<thresh]=np.exp(-.5*curim**2)[curim<thresh]
        xs = np.append(xs, curcen[0] + currad * np.cos(fis))
        ys = np.append(ys, curcen[1] + currad * np.sin(fis))
    plt.imshow(im.T, cmap=cmap, extent=xr+yr, origin="lower")
    # plt.plot(xs, ys, 'r-')
    plt.show()


gauplot([(0,0), (2,3), (5,1), (6,7), (6.1, 6.1)], [.3, .4, .5, 1, .4], [-1,10], [-1,10])
gauplot([(6.1, 6.1)], [.4], [-1,10], [-1,10])

"""
import cv2
import numpy as np

class DrawRoom:
    def __init__(self, room, imshow):

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
"""