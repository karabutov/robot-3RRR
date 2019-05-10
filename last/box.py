import numpy as np
import math
import area

class Box:

    def __init__(self, area):
        self.x0 = area[0][0]
        self.x1 = area[0][1]
        self.y0 = area[1][0]
        self.y1 = area[1][1]
        self.phi0 = area[2][0]
        self.phi1 = area[2][1]        
        self.w2 = ((self.x1 - self.x0) / 2) * 1.1
        self.h2 = ((self.y1 - self.y0) / 2) * 1.1
        self.ph2 = ((self.phi1 - self.phi0) / 2) * 1.1
        self.coordinates = np.array([[self.x0, self.x1], [self.y0, self.y1], [self.phi0, self.phi1]])
        self.lines = np.array([[[self.x0, self.x0],[self.y0, self.y0], [self.phi0, self.phi1]],\
                               [[self.x0, self.x1],[self.y0, self.y0], [self.phi0, self.phi0]],\
                         [[self.x0, self.x0],[self.y0, self.y1], [self.phi0, self.phi0]],\
                         [[self.x0, self.x1],[self.y1, self.y1], [self.phi0, self.phi0]],\
                         [[self.x1, self.x1],[self.y0, self.y1], [self.phi0, self.phi0]],\
                         [[self.x1, self.x1],[self.y0, self.y0], [self.phi0, self.phi1]],\
                         [[self.x1, self.x1],[self.y1, self.y1], [self.phi0, self.phi1]],\
                         [[self.x1, self.x1],[self.y0, self.y1], [self.phi1, self.phi1]],\
                         [[self.x0, self.x1],[self.y0, self.y0], [self.phi1, self.phi1]],\
                         [[self.x0, self.x0],[self.y0, self.y1], [self.phi1, self.phi1]],\
                         [[self.x0, self.x1],[self.y1, self.y1], [self.phi1, self.phi1]],\
                         [[self.x0, self.x0],[self.y1, self.y1], [self.phi0, self.phi1]]])
        self.neighbors = np.array([])
        self.centre_x = self.x0 + (self.x1 - self.x0)/2
        self.centre_y = self.y0 + (self.y1 - self.y0)/2
        self.centre_p = self.phi0 + (self.phi1 - self.phi0)/2
        self.number = -1
        self.initialize(0)

    def initialize(self, initial):
        self.is_processed = False
        self.value = 0xFFFFFF
        self.track = int(initial);

    def is_neighbor(self, box):
        if (abs(self.centre_x - box.centre_x) < (self.w2 + box.w2) and abs(self.centre_y - box.centre_y) < (self.h2 + box.h2) and abs(self.centre_p - box.centre_p) < (self.ph2 + box.ph2)):
            return True
        return False
    
    def distance(self, box):
        return math.sqrt((self.centre_x - box.centre_x)**2 + (self.centre_y - box.centre_y)**2 + (self.centre_p - box.centre_p)**2)

    def add_neighbor(self, box):
        self.neighbors = np.append(self.neighbors, [box], 0)

    def is_internal_dot(self, x, y, p):
        if (self.x0 <= x and self.x1 >= x and self.y0 <= y and self.y1 >= y and self.phi0 <= p and self.phi1 >= p):
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

    def angle_nposition(self, box):
        dif = self.centre_p - box.centre_p
        if (abs(dif) < area.ANGLE/2):
            return 1
        if (dif < 0):
            return 2
        return 0

    def angle_sposition(self, box):
        dif = self.centre_p - box.centre_p
        if (abs(dif) < math.pi/8):
            return "="
        if (dif < 0):
            return "^"
        return "v"

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
        return pos + self.angle_sposition(box)

    def printbox(self, epsi, ang):
        print("N: ", self.number, "x:y:p", self.centre_x, self.centre_y, self.centre_p, "Neighbors: ", self.neighbors.size)
        if (self.x0 >= self.x1):
            print("ERROR Left Right Xs: ", self.x0, self.x1)
        if (self.y0 >= self.y1):
            print("ERROR Top Down Ys: ", self.y0, self.y1)
        if (self.phi0 >= self.phi1):
            print("ERROR High Low Ps: ", self.phi0, self.phi1)
        if (self.x1 - self.x0 > epsi):
            print("ERROR Width: ", self.x1 - self.x0, "Xs", self.x0, self.x1)
        if (self.y1 - self.y0 > epsi):
            print("ERROR Height: ", self.y1 - self.y0, "Ys", self.y0, self.y1)
        if (self.phi1 - self.phi0 > ang):
            print("ERROR Angle: ", self.phi1 - self.phi0, "Ps", self.phi0, self.phi1)
        ln = [0,0,0]
        rn = [0,0,0]
        tn = [0,0,0]
        dn = [0,0,0]
        for i in range(self.neighbors.size):
            nb = self.neighbors[i]
            updn = self.angle_nposition(nb)
            if (self.is_top_box(nb)):
                tn[updn] += 1
            elif (self.is_down_box(nb)):
                dn[updn] += 1
            elif (self.is_left_box(nb)):
                ln[updn] += 1
            elif (self.is_right_box(nb)):
                rn[updn] += 1
        print("Neighbors: ", tn, rn, dn, ln)

    def printvalues(self):
        print("N: ", self.number, "Value", self.value, "x:y:p", self.centre_x, self.centre_y, self.centre_p, "Neighbors: ", self.neighbors.size)
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