import numpy as np
import math

def search(boxes, x, y):
    for i in range(boxes.size):
        if (boxes[i].is_internal_dot(x, y)):
            return int(boxes[i].number)

def minimum_value(boxes):
    minimum = boxes[0].value
    res = 0
#    print("   m b ", boxes.size, minimum)
    for i in range(boxes.size):
#        outp = "        step " + str(i) + ":" + str(boxes[i].number) + ": " + str(boxes[i].value)
        if boxes[i].value < minimum:
            minimum = boxes[i].value
            res = i
#            outp = "   Min. " + outp
#        print(outp)
    return res

def distance(box1, box2):
    return math.sqrt((box1.centre_x - box2.centre_x)**2 + (box1.centre_y - box2.centre_y)**2)

def dijkstra_algorithm(boxes, initial):
    
    boxes_c = np.array(boxes)
    boxes_c[initial].value = 0
    
    while boxes_c.size != 0:
        cur = minimum_value(boxes_c)
#        print("Min", boxes_c[cur].number)
#        print(boxes_c[cur].neighbors.size)
        for i in range(boxes_c[cur].neighbors.size):
#            print(boxes_c[cur].neighbors[i].coordinates)
            nb = boxes_c[cur].neighbors[i]
            if nb.is_processed == True:
                continue
            dist = distance(boxes_c[cur], nb)
            if boxes_c[cur].value + dist < nb.value:
                nb.value = boxes_c[cur].value + dist
                nb.track = int(boxes_c[cur].number)
#        boxes_c[cur].printvalues()
        boxes_c[cur].is_processed = True
        boxes_c = np.delete(boxes_c, cur, 0)   
    return
        
def trajectory_search(boxes, x1, y1, x2, y2):
    
    initial = search(boxes, x1, y1)
    if (initial < 0):
        print("ERROR: Initial point out of valid area")
        return np.array([])
    
    for i in range(boxes.size):
        boxes[i].initialize(initial)
    
    dijkstra_algorithm(boxes, initial)
    final = search(boxes, x2, y2)
    
    trajectory = np.array([boxes[final]])
    cur = final

    while cur != initial:
        trajectory = np.append(trajectory, [boxes[cur]], 0)
        cur = boxes[cur].track
        
    trajectory = np.append(trajectory, [boxes[cur]], 0)
    
    return trajectory