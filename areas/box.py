import numpy as np

class Box:
    
    def __init__(self, area, number):
        self.x0 = area[0][0]
        self.x1 = area[0][1]
        self.y0 = area[1][0]
        self.y1 = area[1][1]
        self.coordinates = np.array([[self.x0, self.x1], [self.y0, self.y1]])
        self.neighbors = np.array([])
        self.number = number
        self.centre_x = self.x0 + (self.x1 - self.x0)/2
        self.centre_y = self.y0 + (self.y1 - self.y0)/2
        self.initialize(0)
    
    def initialize(self, initial):
        self.is_processed = False
        self.value = 0xFFFFFF
        self.track = int(initial);

    def is_neighbor(self, box):
        
        xd = ((self.x1 - self.x0) / 2 + (box.x1 - box.x0) / 2) * 1.01
        yd = ((self.y1 - self.y0) / 2 + (box.y1 - box.y0) / 2) * 1.01
        
        if (abs(self.centre_x - box.centre_x) < xd and abs(self.centre_y - box.centre_y) < yd):
            return True
        
        return False

    def add_neighbor(self, box):
        self.neighbors = np.append(self.neighbors, [box], 0)

    def is_internal_dot(self, x, y):
        if (self.x0 <= x and self.x1 >= x and self.y0 <= y and self.y1 >= y):
            return True
        return False

    def is_left_box(self, box):
        if (self.centre_x > box.centre_x):
            if (self.y0 <= box.y0 and self.y1 >= box.y0):
                return True
            if (self.y1 >= box.y1 and self.y0 <= box.y1):
                return True
        return False

    def is_right_box(self, box):
        if (self.centre_x < box.centre_x):
            if (self.y0 <= box.y0 and self.y1 >= box.y0):
                return True
            if (self.y1 >= box.y1 and self.y0 <= box.y1):
                return True
        return False

    def is_top_box(self, box):
        if (self.centre_y > box.centre_y):
            if (self.x0 <= box.x0 and self.x1 >= box.x0):
                return True
            if (self.x1 >= box.x1 and self.x0 <= box.x1):
                return True
        return False

    def is_down_box(self, box):
        if (self.centre_y < box.centre_y):
            if (self.x0 <= box.x0 and self.x1 >= box.x0):
                return True
            if (self.x1 >= box.x1 and self.x0 <= box.x1):
                return True
        return False

    def position_box(self, box):
        pos = ""
        if (self.is_left_box(box)):
            pos = pos + "l"
        if (self.is_right_box(box)):
            pos = pos + "r"
        if (self.is_top_box(box)):
            pos = pos + "t"
        if (self.is_down_box(box)):
            pos = pos + "d"
        return pos

    def printbox(self, epsi):
        print("N: ", self.number, "x:y", self.centre_x, self.centre_y, "Neighbors: ", self.neighbors.size)
        if (self.x0 >= self.x1):
            print("ERROR Left Right Xs: ", self.x0, self.x1)
        if (self.y0 >= self.y1):
            print("ERROR Top Down Ys: ", self.y0, self.y1)
        if (self.x1 - self.x0 > epsi):
            print("ERROR Width: ", self.x1 - self.x0, "Xs", self.x0, self.x1)
        if (self.y1 - self.y0 > epsi):
            print("ERROR Height: ", self.y1 - self.y0, "Ys", self.y0, self.y1)
        ln = 0;
        rn = 0;
        tn = 0;
        dn = 0;
        er = 0
        for i in range(self.neighbors.size):
            nb = self.neighbors[i]
            if (self.is_top_box(nb)):
                tn+=1
            elif (self.is_down_box(nb)):
                dn+=1
            elif (self.is_left_box(nb)):
                ln+=1
            elif (self.is_right_box(nb)):
                rn+=1
            else:
                er+=1
        if (er > 0):
            print("ERROR Neighbors: ", er)
        print("Neighbors: ", tn, rn, dn, ln)


    def printvalues(self):
        print("N: ", self.number, "Value", self.value, "x:y", self.centre_x, self.centre_y, "Neighbors: ", self.neighbors.size)
        outp = ""
        minpos = ""
        minvalue = 999999
        for i in range(self.neighbors.size):
            nb = self.neighbors[i]
            if (nb.is_processed):
                continue
            pos = self.position_box(nb)
            outp = outp + pos + " " + str(nb.number) + "=" + str(nb.value) + "; "
            if (minvalue > nb.value):
                minpos = pos
                minvalue = nb.value
        print("Min: " + minpos + "=" + str(minvalue), outp)