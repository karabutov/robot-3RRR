import numpy as np

class Box:
    
    
    
    def __init__(self, area, number):
        self.coordinates = np.array([[area[0][0], area[0][1]], [area[1][0], area[1][1]]])
        self.neighbors = np.array([])
        self.number = number
        self.centre_x = area[0][0] + (area[0][1] - area[0][0])/2
        self.centre_y = area[1][0] + (area[1][1] - area[1][0])/2
        self.is_processed = False
        self.EPSILON = 0.01
        self.value = 0xFFFFFF
    
    def is_neighbor(self, box):
    
        if ((box.coordinates[0][0] - self.coordinates[0][1] <= self.EPSILON) and (self.coordinates[0][0] - box.coordinates[0][1] <= self.EPSILON)) and ((abs(box.coordinates[1][1] - self.coordinates[1][0]) <= self.EPSILON) or (abs(self.coordinates[1][1] - box.coordinates[1][0]) <= self.EPSILON)):
            return True
        
        if ((box.coordinates[1][0] - self.coordinates[1][1] <= self.EPSILON) and (self.coordinates[1][0] - box.coordinates[1][1] <= self.EPSILON)) and ((abs(box.coordinates[0][1] - self.coordinates[0][0]) <= self.EPSILON) or (abs(self.coordinates[0][1] - box.coordinates[0][0]) <= self.EPSILON)):
            return True        
        
        return False
        
    def add_neighbor(self, box):
        self.neighbors = np.append(self.neighbors, [box], 0)