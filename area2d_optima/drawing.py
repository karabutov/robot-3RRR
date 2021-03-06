import matplotlib.pyplot as plt
from matplotlib import mlab
import matplotlib.patches as ps 
import matplotlib.lines as ls
import matplotlib.path as ph
import matplotlib.patches as pc
import numpy as np

def print_line(x1,y1,x2,y2):	
    plt.plot([x1, x2],[y1, y2], color = "red")

def paint(areas, color, ax):
    for i in range(areas.size):
        paint_element(areas[i].coordinates, color, ax)

def paint_element(coord, color, ax):
    rect = pc.Rectangle((coord[0][0], coord[1][0]), coord[0][1] - coord[0][0], coord[1][1] - coord[1][0], color=color);
    ax.add_patch(rect)


def draw(areas, trajectory, singularity):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    for i in range(areas.size):
        if areas[i].neighbors.size < 8:
            paint_element(areas[i].coordinates, "blue", ax)

    paint(singularity, "red", ax)
    paint(trajectory, "green", ax)        

    #for i in range(area.size):
    #    for j in range(area[i].neighbors.size):
    #        print_line(area[i].centre_x, area[i].centre_y, area[i].neighbors[j].centre_x, area[i].neighbors[j].centre_y)   
       
    plt.axis('equal') 
    plt.show()
