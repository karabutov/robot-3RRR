import matplotlib.pyplot as plt
from matplotlib import mlab
import numpy as np
import matplotlib.patches as ps 
import matplotlib.lines as ls
import matplotlib.path as ph
import matplotlib.patches as pc

def print_line(x1,y1,x2,y2):	
    plt.plot([x1, x2],[y1, y2])

def draw(args):
    areas = np.array(args)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    while areas.size != 0:
        jac.is_jacobian_deg(areas[0])
        #if is_jacobian_deg(areas[0]):
        #    rect = pc.Rectangle((areas[0][0][0], areas[0][1][0]), areas[0][0][1] - areas[0][0][0], areas[0][1][1] - areas[0][1][0], color="red");
        #else:
         #   rect = pc.Rectangle((areas[0][0][0], areas[0][1][0]), areas[0][0][1] - areas[0][0][0], areas[0][1][1] - areas[0][1][0], color="blue");
        rect = pc.Rectangle((areas[0][0][0], areas[0][1][0]), areas[0][0][1] - areas[0][0][0], areas[0][1][1] - areas[0][1][0], color="blue");

        ax.add_patch(rect)
        areas = np.delete(areas, 0, 0)
    plt.axis('equal') 
    plt.show()
