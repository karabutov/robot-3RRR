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

def paint(area, ax, color):
    for i in range(12):
            ax.plot([area.lines[i][0][0] ,area.lines[i][0][1]],[area.lines[i][1][0] ,area.lines[i][1][1]],[area.lines[i][2][0] ,area.lines[i][2][1]],"--",alpha=0.3, color=color)
    

def draw(area, trajectory):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for j in range(area.size):
        paint(area[j], ax, "b")
    for j in range(trajectory.size):
        paint(trajectory[j], ax, "r")
    plt.axis('equal') 
    plt.show()
    #Axes3D.plot()
