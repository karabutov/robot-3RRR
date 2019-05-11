import pylab
from mpl_toolkits.mplot3d import Axes3D
import numpy
import matplotlib.pyplot as plt

def paint_box(area, ax, color, alpha):
    for i in range(12):
            ax.plot([area.lines[i][0][0] ,area.lines[i][0][1]],[area.lines[i][1][0] ,area.lines[i][1][1]],[area.lines[i][2][0] ,area.lines[i][2][1]],"--",alpha = alpha, color=color)

def paint_hole_box(area, ax, color, alpha):
    ax.bar3d(area[0][0], area[1][0], area[2][0], area[0][0] - area[0][1], area[1][0] - area[1][1], area[2][0] - area[2][1], color = color, alpha = alpha)
    
def paint_tr_si(area, ax, color, alpha):
    for j in range(area.size):
        #paint_box(area[j], ax, color, alpha)
        paint_hole_box(area[j].coordinates, ax, color, alpha)

def paint_area(area, ax, color, alpha):
    i = 0
    for j in range(area.size):
        if area[j].neighbors.size <= 25:
            i = i+1
            #paint_box(area[j], ax, color, alpha)
            paint_hole_box(area[j].coordinates, ax, color, alpha)
    print(i)

def draw(area, trajectory, singularity):

    fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    ax = fig.gca(projection='3d')

    paint_tr_si(trajectory, ax, "g", 0.8)
    
    paint_tr_si(singularity, ax, "r", 1)
    
    paint_area(area, ax, "b", 0.4)

    plt.axis('equal') 
    plt.show()
