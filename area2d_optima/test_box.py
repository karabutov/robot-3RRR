import numpy as np
import box
import areaotim

main_box = box.Box([[0., 100.], [0., 200.], [0., 100.]])

main_box.print_box_only("Main box")

box1, box2 = main_box.split()

box1.print_box_only("box 1")
box2.print_box_only("box 2")

for i in range(4):
    ba = box1.get_angle_box(i)
    ba.print_box_only("Angle " + str(i))

box.MAX_SIZE = [10, 10, 1000]
boxes = np.empty((0,), dtype=np.object)
boxes = areaotim.devide_until_valid_size(np.empty((0,), dtype=np.object), box1)
print("Valid Size", boxes.size)
for i in range(boxes.size):
    boxes[i].number = i
#    boxes[i].printbox()
