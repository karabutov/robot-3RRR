import pylab
from mpl_toolkits.mplot3d import Axes3D
import numpy
import matplotlib.pyplot as plt



def makeData1 ():
    x = numpy.arange (0, 4, 0.1)
    y = numpy.arange (0, 4, 0.1)
    xgrid, ygrid = numpy.meshgrid(x, y)

    zgrid = numpy.sin (xgrid) * numpy.sin (ygrid) / (xgrid * ygrid)
    return xgrid, ygrid, zgrid

def paint_box(area, ax, color, alpha):
    for i in range(12):
            ax.plot([area.lines[i][0][0] ,area.lines[i][0][1]],[area.lines[i][1][0] ,area.lines[i][1][1]],[area.lines[i][2][0] ,area.lines[i][2][1]],"--",alpha = alpha, color=color)
    
def paint_tr_si(area, ax, color, alpha):
    for j in range(area.size):
        paint_box(area[j], ax, color, alpha)

def paint_area(area, ax, color, alpha):
    for j in range(area.size):
        if area[j].neighbors.size <= 25:
            paint_box(area[j], ax, color, alpha)    

def draw(area, trajectory, singularity):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    paint_tr_si(trajectory, ax, "g", 0.8)
    
    paint_tr_si(singularity, ax, "r", 0.3)
    
    paint_area(area, ax, "b", 0.3)

    plt.axis('equal') 
    plt.show()
    #Axes3D.plot()
