import math
import matplotlib.pyplot as plt

l = 1
size_side = 1
k = (2/3) * (size_side * math.sqrt(3) / 2)

def calculation(centr_x, centr_y, angle_of_rot):
	try:
		def print_line(x1,y1,x2,y2):	
			plt.plot([x1, x2],[y1, y2])
			#print('Длина: ', math.sqrt((x1 - x2)**2 + (y1 - y2)**2))				

		def triangl_evertex(i):
			return centr_x + k * math.cos(math.pi * (0.5 + i * 2 / 3.0) + angle_of_rot), centr_y + k * math.sin(math.pi * (0.5 + i * 2 / 3.0) + angle_of_rot)

		def print_triangle():
			top_x1, top_y1 = triangl_evertex(1)
			top_x2, top_y2 = triangl_evertex(2)	
			top_x3, top_y3 = triangl_evertex(3)		
			print_line(top_x1, top_y1, top_x2, top_y2)
			print_line(top_x3, top_y3, top_x2, top_y2)
			print_line(top_x1, top_y1, top_x3, top_y3)	

		def angles(topx, topy, x, y):
			alpha = math.acos(math.sqrt((x - topx)**2 + (y - topy)**2) / (2 * l))
			betta = math.atan((topy - y) / (topx - x))
			if topx - x < 0:
				betta += math.pi
			return alpha + betta, betta - alpha
		
		def building_kinematic_chain(x, y, num):	
			top_x, top_y = triangl_evertex(num)	
			angle1, angle2 = angles(top_x, top_y, x, y)
	
			print_line(x, y, x + l * math.cos(angle1), y + l * math.sin(angle1))
			print_line(x, y, x + l * math.cos(angle2), y + l * math.sin(angle2))
			plt.plot(x, y, 'go')

			print_line(x + l * math.cos(angle1), y + l * math.sin(angle1), top_x, top_y)
			print_line(x + l * math.cos(angle2), y + l * math.sin(angle2), top_x, top_y)


		building_kinematic_chain(0, 0, 1)
		building_kinematic_chain(3.4, 0.33, 2)
		building_kinematic_chain(2, 3, 3)

		print_triangle()
		
		plt.axis('equal')
		plt.show()

	except ValueError: 
		print("Введены недопустимые координаты")


centr_x = float(input("Введить координату x центра треугольника\nx = "))
centr_y = float(input("Введить координату y центра треугольника\ny = "))
angel_of_rot = float(input("Введить угол поворота\nangle = "))

calculation(centr_x, centr_y, angel_of_rot)
