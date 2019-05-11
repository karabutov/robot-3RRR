import drawing as dr
import box
import dijkstra as di
import datetime
import jacobian as jac
import areaotim
import numpy as np
#import drawing3d as d3

#a_phi = float(input("Enter angle of rootation\nangel = "))

# When calculate without singularity Max Size of MIN_SIZE[0], MIN_SIZE[1] = 0.5
# When calculate with singularity Max Size of MIN_SIZE[0], MIN_SIZE[1] = 0.1
box.MAX_SIZE = [0.1, 0.1, 100]

initial_box = areaotim.initial_limits()
initial_box.print_box_only("Initial box")

tstart = datetime.datetime.now()

boxes = areaotim.start_divide(np.empty((0,), dtype=np.object), initial_box)

delta = datetime.datetime.now() - tstart

print("Area. Boxes.size: " + str(boxes.size) + "; Time: " + str(delta.seconds) + "." + str(delta.microseconds))

#x1 = float(input("x1 = "))
#y1 = float(input("y1 = "))
#x2 = float(input("x2 = "))
#y2 = float(input("y2 = "))

tstart = datetime.datetime.now()

#singularity, boxes = jac.singularity_points(boxes)
singularity = np.array([])

delta = datetime.datetime.now() - tstart

print("Area with singularity. Boxes.size: " + str(boxes.size) + "; Singularity. Size " + str(singularity.size) + "; Time: " + str(delta.seconds) + "." + str(delta.microseconds))

for i in range(boxes.size):
    boxes[i].number = i

tstart = datetime.datetime.now()

ncycle = 0
TPROF4 = datetime.datetime.now()
TPROF5 = datetime.datetime.now()
for i in range(boxes.size):
    if (boxes[i].neighbors.size < 8):
        for j in range(i + 1, boxes.size):
            if (boxes[i].is_neighbor(boxes[j])):
                boxes[i].add_neighbor(boxes[j])
                boxes[j].add_neighbor(boxes[i])
            ncycle += 1
            if (ncycle%1000000 == 0):
                tps2 = datetime.datetime.now()
                delta_all = tps2 - TPROF4
                delta1000 = tps2 - TPROF5
                #print("C: " + str(ncycle) + "; " + str(i) + ":" + str(j) + "; d1000: " + str(delta1000.seconds) + "; all: " + str(delta_all.seconds))
                TPROF5 = tps2
            if (boxes[i].neighbors.size == 8):
                break

delta = datetime.datetime.now() - tstart
print("Neighbors. Time "  + str(delta.seconds) + "." + str(delta.microseconds))

#for i in range(boxes.size):
#    boxes[i].printbox()

x1 = 2.2
y1 = 0.5
x2 = 1.2
y2 = 0.9

trajectory = di.trajectory_search(boxes, x1, y1, x2, y2)
#trajectory = np.array([])

#dr.draw(boxes, trajectory, singularity)
dr.draw(boxes, trajectory, singularity)
#dr.draw(boxes, np.array([]), singularity)
#dr.draw(boxes, np.array([]), np.array([]))

'''
print("Left -> Right")
x1 = 1.1
y1 = 0.8
x2 = 2.0
y2 = 0.8
trajectory = di.trajectory_search(boxes, x1, y1, x2, y2)
dr.draw(boxes, trajectory, singularity)

print("Right -> Left")
x1 = 2.0
y1 = 0.8
x2 = 1.1
y2 = 0.8
trajectory = di.trajectory_search(boxes, x1, y1, x2, y2)
dr.draw(boxes, trajectory, singularity)

print("Down -> Top")
x1 = 1.7
y1 = 0.6
x2 = 1.7
y2 = 1.7
trajectory = di.trajectory_search(boxes, x1, y1, x2, y2)
dr.draw(boxes, trajectory, singularity)

print("Top -> Down")
x1 = 1.7
y1 = 1.7
x2 = 1.7
y2 = 0.6
trajectory = di.trajectory_search(boxes, x1, y1, x2, y2)
dr.draw(boxes, trajectory, singularity)

print("Right Down -> Left Top")
x1 = 2.3
y1 = 0.6
x2 = 1.4
y2 = 1.2
trajectory = di.trajectory_search(boxes, x1, y1, x2, y2)
dr.draw(boxes, trajectory, singularity)

print("Left Top -> Right Down")
x1 = 1.4
y1 = 1.2
x2 = 2.3
y2 = 0.6
trajectory = di.trajectory_search(boxes, x1, y1, x2, y2)
dr.draw(boxes, trajectory, singularity)

print("Right Top -> Left Down")
x1 = 2.0
y1 = 1.3
x2 = 1.1
y2 = 0.5
trajectory = di.trajectory_search(boxes, x1, y1, x2, y2)
dr.draw(boxes, trajectory, singularity)

print("Left Down -> Right Top")
x1 = 1.1
y1 = 0.5
x2 = 2.0
y2 = 1.3
trajectory = di.trajectory_search(boxes, x1, y1, x2, y2)
dr.draw(boxes, trajectory, singularity)
'''
print("That's all!!!")
