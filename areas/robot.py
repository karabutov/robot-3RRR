import drawing as dr
import box
import dijkstra as di
import datetime
import jacobian as jac
import area
import numpy as np
import drawing3d as d3

#a_phi = float(input("Enter angle of rootation\nangel = "))

tstart = datetime.datetime.now()

areas = area.calculating("ip")

delta = datetime.datetime.now() - tstart

print("Area time: " + str(delta.seconds) + "." + str(delta.microseconds))

print("Quantity of boxes = ", areas.shape[0])

boxes = np.empty((areas.shape[0],), dtype=np.object)
i = 0
for i in range(areas.shape[0]):
    boxes[i] = box.Box(areas[i])

#x1 = float(input("x1 = "))
#y1 = float(input("y1 = "))
#x2 = float(input("x2 = "))
#y2 = float(input("y2 = "))

x1 = 1.7
y1 = 0.5
x2 = 1.1
y2 = 0.9

tstart = datetime.datetime.now()

singularity, boxes = jac.singularity_points(boxes)

delta = datetime.datetime.now() - tstart
print("Singularity time: " + str(delta.seconds) + "." + str(delta.microseconds))

for i in range(boxes.size):
    boxes[i].number = i

d3.draw(boxes)

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

#for i in range(boxes.size):
#    boxes[i].printbox(EPSILON)

tstart = datetime.datetime.now()
#trajectory = di.trajectory_search(boxes, x1, y1, x2, y2)

delta = datetime.datetime.now() - tstart
print("Trajectory time1: " + str(delta.seconds) + "." + str(delta.microseconds))


tstart = datetime.datetime.now()

#dr.draw(boxes, trajectory, singularity)
#dr.draw(boxes, trajectory, np.array([]))
#dr.draw(boxes, np.array([]), singularity)
#dr.draw(boxes, np.array([]), np.array([]))

delta = datetime.datetime.now() - tstart
print("Print time: " + str(delta.seconds) + "." + str(delta.microseconds))


'''
print("Left -> Right")
x1 = 1.0
y1 = 0.8
x2 = 2.0
y2 = 0.8
trajectory = di.trajectory_search(boxes, x1, y1, x2, y2)
dr.draw(boxes, trajectory)

print("Right -> Left")
x1 = 2.0
y1 = 0.8
x2 = 1.0
y2 = 0.8
trajectory = di.trajectory_search(boxes, x1, y1, x2, y2)
dr.draw(boxes, trajectory)

print("Down -> Top")
x1 = 1.5
y1 = 0.6
x2 = 1.5
y2 = 1.7
trajectory = di.trajectory_search(boxes, x1, y1, x2, y2)
dr.draw(boxes, trajectory)

print("Top -> Down")
x1 = 1.5
y1 = 1.7
x2 = 1.5
y2 = 0.6
trajectory = di.trajectory_search(boxes, x1, y1, x2, y2)
dr.draw(boxes, trajectory)

print("Right Down -> Left Top")
x1 = 2.3
y1 = 0.6
x2 = 1.4
y2 = 1.7
trajectory = di.trajectory_search(boxes, x1, y1, x2, y2)
dr.draw(boxes, trajectory)

print("Left Top -> Right Down")
x1 = 1.4
y1 = 1.7
x2 = 2.3
y2 = 0.6
trajectory = di.trajectory_search(boxes, x1, y1, x2, y2)
dr.draw(boxes, trajectory)

print("Right Top -> Left Down")
x1 = 2.0
y1 = 1.4
x2 = 1.0
y2 = 0.7
trajectory = di.trajectory_search(boxes, x1, y1, x2, y2)
dr.draw(boxes, trajectory)

print("Left Down -> Right Top")
x1 = 1.0
y1 = 0.7
x2 = 2.0
y2 = 1.4
trajectory = di.trajectory_search(boxes, x1, y1, x2, y2)
dr.draw(boxes, trajectory)

'''


print("That's all!!!")
