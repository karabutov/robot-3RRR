import drawing as dr
import box
import dijkstra as di
import datetime
import jacobian as jac
import area
import numpy as np

#a_phi = float(input("Enter angle of rootation\nangel = "))

tstart = datetime.datetime.now()

areas = area.calculating("ip")

delta = datetime.datetime.now() - tstart

print("Area time: " + str(delta.seconds) + "." + str(delta.microseconds))

print("Quantity of boxes = ", areas.shape[0])

boxes = np.empty((areas.shape[0],), dtype=np.object)
i = 0
for i in range(areas.shape[0]):
    boxes[i] = box.Box(areas[i], i)

#for i in range(boxes.size):
#    boxes[i].printbox(EPSILON)

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


tstart = datetime.datetime.now()

for i in range(boxes.size):
    for j in range(boxes.size):
        if j == i:
            continue
        if boxes[i].is_neighbor(boxes[j]):
            boxes[i].add_neighbor(boxes[j])
trajectory = di.trajectory_search(boxes, x1, y1, x2, y2)

delta = datetime.datetime.now() - tstart
print("Trajectory time1: " + str(delta.seconds) + "." + str(delta.microseconds))


tstart = datetime.datetime.now()

#dr.draw(boxes, trajectory, singularity)
dr.draw(boxes, trajectory, np.array([]))
#dr.draw(boxes, np.array([]), singularity)
#dr.draw(boxes, np.array([]), np.array([]))

delta = datetime.datetime.now() - tstart
print("Print time: " + str(delta.seconds) + "." + str(delta.microseconds))


print("That's all!!!")
