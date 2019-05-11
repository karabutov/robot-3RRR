import numpy as np
import datetime

def search(boxes, x, y, p):
    for i in range(boxes.size):
        if (boxes[i].is_internal_dot(x, y, p)):
            return int(boxes[i].number)
    return -1

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
    return res, 

def dijkstra_algorithm(initialbox):

    initialbox.value = 0
    work_boxes = np.empty((0,), dtype=np.object)
    work_boxes = np.append(work_boxes, [initialbox], 0)
#    cycle = 0
    while work_boxes.size != 0:
        cur = minimum_value(work_boxes)
        cur_box = work_boxes[cur]
        work_boxes = np.delete(work_boxes, cur, 0)
#        print("Min V", cur_box.number, "Size", work_boxes.size)
        for i in range(cur_box.neighbors.size):
#            print(cur_box.neighbors[i].coordinates)
            nb = cur_box.neighbors[i]
            if nb.is_processed:
                continue
            if not nb.is_added:
                work_boxes = np.append(work_boxes, [nb], 0)
                nb.is_added = True
#                nb.printvalues()
            dist = cur_box.distance(nb)
            if cur_box.value + dist < nb.value:
                nb.value = cur_box.value + dist
                nb.track = int(cur_box.number)
#        cur_box.printvalues()
        cur_box.is_processed = True
#        cycle += 1
#        if cycle > 20:
#            break
    return
        
def trajectory_search(boxes, x1, y1, p1, x2, y2, p2):
    tstart = datetime.datetime.now()
    
    initial = search(boxes, x1, y1, p1)
    if (initial < 0):
        print("ERROR: Initial point out of valid area")
        return np.array([])
    
    final = search(boxes, x2, y2, p2)
    if (final < 0):
        print("ERROR: Final point out of valid area")
        return np.array([])

    for i in range(boxes.size):
        boxes[i].initialize(initial)
    
    print("Initial: " + str(initial) + "; Final: " + str(final))
    dijkstra_algorithm(boxes[initial])
#    print("boxes filled with trajectory")
    
    trajectory = np.array([])
    cur = final

    while cur != initial:
        trajectory = np.append(trajectory, [boxes[cur]], 0)
        cur = boxes[cur].track

    trajectory = np.append(trajectory, [boxes[cur]], 0)

    delta = datetime.datetime.now() - tstart
    print("Trajectory. Size " + str(trajectory.size) + ". Time "  + str(delta.seconds) + "." + str(delta.microseconds))
    
    return trajectory