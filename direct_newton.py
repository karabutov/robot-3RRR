import math
import scipy.optimize
import matplotlib.pyplot as plt
from matplotlib import mlab
import numpy as np
import matplotlib.patches as ps 
import matplotlib.lines as ls
import matplotlib.path as ph

size_side = 1
k = (2/3) * (size_side * math.sqrt(3) / 2)
l = 1

gamma1 = math.pi * (0.5 + 1 * 2/3) 
gamma2 = math.pi * (0.5 + 2 * 2/3) 
gamma3 = math.pi * (0.5 + 3 * 2/3)

x1 = 0.0
y1 = 0.0
x2 = 3.4
y2 = 0.33
x3 = 2.0
y3 = 3.0

theta1 = -0.43188480761509385
theta2 = 2.085718657450161
theta3 = 3.614649307124737

def print_line(x1,y1,x2,y2):	
	plt.plot([x1, x2],[y1, y2])
	#print('Длина: ', math.sqrt((x1 - x2)**2 + (y1 - y2)**2))				

def draw(centr_x, centr_y, phi):
	ax = plt.subplot()
	def triangl_evertex(i):
		return centr_x + k * math.cos(math.pi * (0.5 + i * 2 / 3.0) + phi), centr_y + k * math.sin(math.pi * (0.5 + i * 2 / 3.0) + phi)

	def print_triangle():
		top_x1, top_y1 = triangl_evertex(1)
		top_x2, top_y2 = triangl_evertex(2)	
		top_x3, top_y3 = triangl_evertex(3)		
		print_line(top_x1, top_y1, top_x2, top_y2)
		print_line(top_x3, top_y3, top_x2, top_y2)
		print_line(top_x1, top_y1, top_x3, top_y3)
	
	def draw_kinematic_chains(x, y, theta, i):
		top_x, top_y = triangl_evertex(i)
		print_line(x, y, x + l * math.cos(theta), y + l * math.sin(theta))
		#circle1 = plt.Circle((x + l * math.cos(theta), y + l * math.sin(theta)), radius=l, fill=False)
		#ax.add_artist(circle1)
		print_line(x + l * math.cos(theta), y + l * math.sin(theta), top_x, top_y)
		plt.plot(x, y, 'go')
		
	
	plt.plot(centr_x, centr_y, 'go')
	print_triangle()		
	draw_kinematic_chains(x1, y1, theta1, 1)
	draw_kinematic_chains(x2, y2, theta2, 2)
	draw_kinematic_chains(x3, y3, theta3, 3)
	
	plt.axis('equal')
	plt.show()

def print_solution(results, method):
	print(method)
	for i in range(len(results)):
		print(i+1, " solution: ", "x = ", results[i][0], "y = ", results[i][1], "phi = ", results[i][2])

def func_old(t):
	x = t[0]
	y = t[1]
	phi = t[2]
	return[(x + k * math.cos(gamma1 + phi) - xB1)**2 + (y + k * math.sin(gamma1 + phi) - yB1)**2 - l**2,
	       (x + k * math.cos(gamma2 + phi) - xB2)**2 + (y + k * math.sin(gamma2 + phi) - yB2)**2 - l**2,
	       (x + k * math.cos(gamma3 + phi) - xB3)**2 + (y + k * math.sin(gamma3 + phi) - yB3)**2 - l**2]

def normalize(phi):
	if (abs(phi) < 0.0001) or (abs(phi - 2*math.pi) < 0.01):
		phi = 0.0
		return phi
	inc = -2*math.pi
	if phi < 0:
		inc *= -1

	while not(0 <= phi <= 2 * math.pi):
		phi += inc
	if (abs(phi) < 0.0001) or (abs(phi - 2*math.pi) < 0.01):
		phi = 0.0
	return phi

def new_solution(results, res, ind):
	if ind == 1:
		if len(results) == 0:
			x, y = solution_kramer(res)	
			results.append([x, y, res])
			return True
		else:
			for i in range(len(results)):
				if abs(results[i][2] - res) < 0.01:
					return False
		x, y = solution_kramer(res)	
		results.append([x, y, res])
		return True
	if ind == 3:
		if len(results) == 0:
			results.append(res)
			return True
		else:
			for i in range(len(results)):
				if abs(results[i][0] - res[0]) < 0.01 and abs(results[i][1] - res[1]) < 0.01 and abs(results[i][2] - res[2]) < 0.01:
					return False
			results.append(res)
		return True

def system_newton(n):
	
	def func_sys(t):
		x = t[0]
		y = t[1]
		phi = t[2]
		return np.array([(x + k * math.cos(gamma1 + phi) - xB1)**2 + (y + k * math.sin(gamma1 + phi) - yB1)**2 - l**2,
			   (x + k * math.cos(gamma2 + phi) - xB2)**2 + (y + k * math.sin(gamma2 + phi) - yB2)**2 - l**2,
			   (x + k * math.cos(gamma3 + phi) - xB3)**2 + (y + k * math.sin(gamma3 + phi) - yB3)**2 - l**2])

	def x_derivative1(x, y, phi):
		return 2*(x + k*math.cos(gamma1+phi) - xB1)

	def y_derivative1(x, y, phi):
		return 2*(y + k*math.sin(gamma1+phi) - yB1)

	def phi_derivative1(x, y, phi):
		return 2*k*math.cos(gamma1+phi) * (y + k*math.sin(gamma1+phi) - yB1) - 2*k*math.sin(gamma1+phi) * (x + k*math.cos(gamma1+phi) - xB1)

	def x_derivative2(x, y, phi):
		return 2*(x + k*math.cos(gamma2+phi) - xB2)

	def y_derivative2(x, y, phi):
		return 2*(y + k*math.sin(gamma2+phi) - yB2)

	def phi_derivative2(x, y, phi):
		return 2*k*math.cos(gamma2+phi) * (y + k*math.sin(gamma2+phi) - yB2) - 2*k*math.sin(gamma2+phi) * (x + k*math.cos(gamma2+phi) - xB2)

	def x_derivative3(x, y, phi):
		return 2*(x + k*math.cos(gamma3+phi) - xB3)

	def y_derivative3(x, y, phi):
		return 2*(y + k*math.sin(gamma3+phi) - yB3)

	def phi_derivative3(x, y, phi):
		return 2*k*math.cos(gamma3+phi) * (y + k*math.sin(gamma3+phi) - yB3) - 2*k*math.sin(gamma3+phi) * (x + k*math.cos(gamma3+phi) - xB3)

	def hamiltonian(point):
		x = point[0]
		y = point[1]
		phi = point[2]
		return np.array([[x_derivative1(x, y, phi), y_derivative1(x, y, phi), phi_derivative1(x, y, phi)],
						[x_derivative2(x, y, phi), y_derivative2(x, y, phi), phi_derivative2(x, y, phi)],
						[x_derivative3(x, y, phi), y_derivative3(x, y, phi), phi_derivative3(x, y, phi)]])

	def newton(guess):
		eps = 0.000000001
		ind = 0
		while abs(func_sys(guess)[0])>eps and abs(func_sys(guess)[1])>eps and abs(func_sys(guess)[2])>eps:			
			if ind > 100:
				return[-1, -1, -1]
			try:			
				inv_ham = np.linalg.inv(hamiltonian(guess))
			except np.linalg.LinAlgError:
				return [-1, -1, -1]
			guess = guess - np.matmul(inv_ham, func_sys(guess))
			ind += 1
		return guess
	
	stepx = 3.5 / n
	stepy = 3.0 / n
	guess_x = []
	guess_y = []
	for i in range(n):
		guess_x.append(i*stepx)
		guess_y.append(i*stepy)
	results = []
	for i in range(n):
		for j in range(n):
			#print(i, j)
			res = newton(np.array([guess_x[i], guess_y[j], math.pi/4]))
			if res[0] == -1:
				continue
			res[2] = normalize(res[2])
			new_solution(results, res, 3)
	return results
			
 
#theta1 = float(input())
#theta2 = float(input())
#theta3 = float(input())

xB1 = x1 + l * math.cos(theta1)
yB1 = y1 + l * math.sin(theta1)
xB2 = x2 + l * math.cos(theta2)
yB2 = y2 + l * math.sin(theta2)
xB3 = x3 + l * math.cos(theta3) 
yB3 = y3 + l * math.sin(theta3)

results = system_newton(30)

if(len(results) == 0):
	print("Incorrect values")
else:
	for i in range(len(results)):
		draw(results[i][0], results[i][1], results[i][2])
	print_solution(results, "Newton System")	
