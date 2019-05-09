import numpy as np

def search(boxes, x, y):
    print(x, y)
    for i in range(boxes.size):
        print(boxes[i].coordinates[0][0], boxes[i].coordinates[0][1], boxes[i].coordinates[1][0], boxes[i].coordinates[1][1])
        if x > boxes[i].coordinates[0][0] and x < boxes[i].coordinates[0][1] and y > boxes[i].coordinates[1][0] and y < boxes[i].coordinates[1][1]:
            print(i)
            return boxes[i].number

def minimum_value(boxes):
    min = boxes[0].value
    res = 0
    for i in range(boxes.size):
        if boxes[i].value < min:
            min = boxes[i].value
            res = boxes[i].number
    return res

def distance(box1, box2):
    return (box1.centre_x - box2.centre_x)**2 + (box1.centre_y - box2.centre_y)**2

def dijkstra_algorithm(boxes, x, y):
    
    tracks = np.ones((1, boxes.size))
    initial = search(boxes, x, y)
    
    boxes[2].value
    
    boxes_c = np.array(boxes)
    print(boxes_c)
    print(initial)
    boxes_c[initial].value = 0
    for i in range(boxes_c.size):
        tracks[i] = initial
        
    while boxes_c.size != 0:
        
        cur = minimum_value(boxes_c)
        
        for i in range(boxes_c[cur].neighbors.size):
            dist = distance(boxes_c[cur], boxes_c[cur].neighbors[i])
            if boxes_c[cur].value + dist < boxes_c[cur].neighbors[i].value:
                boxes_c[cur].neighbors[i].value = boxes_c[cur].value + dist
                tracks[boxes_c[cur].neighbors[i].number] = boxes_c[cur].number
        
        boxes_c = np.delete(boxes_c, 0, 0)
        
    return tracks
        
def trajectory_search(boxes, x1, y1, x2, y2):
    
    tracks = dijkstra_algorithm(boxes, x1, y1)
    initial = search(boxes, x1, y1)
    final = search(boxes, x2, y2)
    
    trajectory = np.array([boxes[final]])
    cur = final
    
    while cur != initial:
        trajectory = np.append(trajectory, boxes[tracks[cur]], 0)
        cur = tracks[cur]
        
    trajectory = np.append(trajectory, boxes[cur], 0)
    
    return tracks