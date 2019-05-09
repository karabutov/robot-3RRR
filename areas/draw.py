import matplotlib.pyplot as plt
from matplotlib import mlab
import numpy as np
import matplotlib.patches as ps 
import matplotlib.lines as ls
import matplotlib.path as ph
import matplotlib.patches as pc
import jacobian as jac

def print_line(x1,y1,x2,y2):	
    plt.plot([x1, x2],[y1, y2], color = "red")

def draw(args, trajectory):
    areas = np.array(args)
    tr = np.array(trajectory)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    while areas.size != 0:
        coord = areas[0].coordinates
        #if jac.is_jacobian_deg(coord):
        #    rect = pc.Rectangle((coord[0][0], coord[1][0]), coord[0][1] - coord[0][0], coord[1][1] - coord[1][0], color="red");
        #else:
        #    rect = pc.Rectangle((coord[0][0], coord[1][0]), coord[0][1] - coord[0][0], coord[1][1] - coord[1][0], color="blue");

        rect = pc.Rectangle((coord[0][0], coord[1][0]), coord[0][1] - coord[0][0], coord[1][1] - coord[1][0], color="blue");
        
        ax.add_patch(rect)
        areas = np.delete(areas, 0, 0)

    for i in range(args.size):
       for j in range(args[i].neighbors.size):
            print_line(args[i].centre_x, args[i].centre_y, args[i].neighbors[j].centre_x, args[i].neighbors[j].centre_y)   
    
    while tr.size != 0:
        coord = tr[0].coordinates
        rect = pc.Rectangle((coord[0][0], coord[1][0]), coord[0][1] - coord[0][0], coord[1][1] - coord[1][0], color="red");
        ax.add_patch(rect)
        tr = np.delete(tr, 0, 0)        
    
    plt.axis('equal') 
    plt.show()
