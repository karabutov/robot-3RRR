import math
import draw as dr
import box
import dijkstra as di
import scipy.optimize as so
import numpy as np


EPSILON = 0.1

size_side = 1.
k = (2./3.) * (size_side * math.sqrt(3.) / 2.)
l = 1.
a_phi = 0.;

gamma1 = math.pi * (0.5 + 1. * 2./3.) 
gamma2 = math.pi * (0.5 + 2. * 2./3.) 
gamma3 = math.pi * (0.5 + 3. * 2./3.)

x1 = 0.0
y1 = 0.0
x2 = 3.4
y2 = 0.33
x3 = 2.0
y3 = 3.0

def find_boundaries_x():
    min_x = max(x1 - 2 * l + k / 2, x2 - 2 * l + k / 2, x3 - 2 * l + k / 2)
    max_x = min(x1 + 2 * l - k / 2, x2 + 2 * l - k / 2, x3 + 2 * l - k / 2)
    #return np.array([min_x, max_x])
    return np.array([0, 3])

def find_boundaries_y():
    min_x = max(y1 - 2 * l + k / 2, y2 - 2 * l + k / 2, y3 - 2 * l + k / 2)
    max_x = min(y1 + 2 * l - k / 2, y2 + 2 * l - k / 2, y3 + 2 * l - k / 2)
    #return np.array([min_x, max_x])
    return np.array([0, 3])

def initial_limits():
    x_interval = find_boundaries_x()
    y_interval = find_boundaries_y()
    phi_interval = np.array([0, 2 * math.pi])
    theta1_interval = np.array([0, 2 * math.pi])
    theta2_interval = np.array([0, 2 * math.pi])
    theta3_interval = np.array([0, 2 * math.pi])

    res = np.zeros((6, 2))
    res[0][0] = x_interval[0]
    res[1][0] = y_interval[0]
    res[2][0] = phi_interval[0]
    res[3][0] = theta1_interval[0]
    res[4][0] = theta2_interval[0]
    res[5][0] = theta2_interval[0]

    res[0][1] = x_interval[1]
    res[1][1] = y_interval[1]
    res[2][1] = phi_interval[1]
    res[3][1] = theta1_interval[1]
    res[4][1] = theta2_interval[1]
    res[5][1] = theta2_interval[1]

    return res

def first_equation(args):
    x =	args[0]
    y =	args[1] 
    phi = args[2]
    theta1 = args[3]
    theta2 = args[4]
    theta3 = args[5]
    xB1 = x1 + l * math.cos(theta1)
    yB1 = y1 + l * math.sin(theta1)
    return (x + k * math.cos(gamma1 + phi) - xB1)**2 + (y + k * math.sin(gamma1 + phi) - yB1)**2 - l**2

def second_equation(args):
    x =	args[0]
    y =	args[1] 
    phi = args[2]
    theta1 = args[3]
    theta2 = args[4]
    theta3 = args[5]
    xB2 = x2 + l * math.cos(theta2)
    yB2 = y2 + l * math.sin(theta2)
    return (x + k * math.cos(gamma2 + phi) - xB2)**2 + (y + k * math.sin(gamma2 + phi) - yB2)**2 - l**2

def third_equation(args):
    x =	args[0]
    y =	args[1] 
    phi = args[2]
    theta1 = args[3]
    theta2 = args[4]
    theta3 = args[5]
    theta3 = args[4]
    xB3 = x3 + l * math.cos(theta3)
    yB3 = y3 + l * math.sin(theta3)
    return (x + k * math.cos(gamma3 + phi) - xB3)**2 + (y + k * math.sin(gamma3 + phi) - yB3)**2 - l**2

def minus_first_equation(args):
    return -first_equation(args)

def minus_second_equation(args):
    return -second_equation(args)

def minus_third_equation(args):
    return -third_equation(args)

def is_a_zero(func, minus_func, method, aria):
    args_b = np.array([aria[0][0], aria[1][0], aria[2][0], aria[3][0], aria[4][0], aria[5][0]])
    args_e = np.array([aria[0][1], aria[1][1], aria[2][1], aria[3][1], aria[4][1], aria[5][1]])
    
    min_solut = so.minimize(func,  (args_e + args_b) / 2., method=method, bounds = ((args_b[0], args_e[0]), (args_b[1], args_e[1]), (args_b[2], args_e[2]), (args_b[3], args_e[3]), (args_b[4], args_e[4]), (args_b[5], args_e[5])))
    max_solut = so.minimize(minus_func, (args_e + args_b) / 2., method=method, bounds = ((args_b[0], args_e[0]), (args_b[1], args_e[1]), (args_b[2], args_e[2]), (args_b[3], args_e[3]), (args_b[4], args_e[4]), (args_b[5], args_e[5])))

    max_of_f = -max_solut.fun
    min_of_f = min_solut.fun
    
    if not(max_of_f >= 0. and min_of_f <= 0.):
        return False
    
    return True

def there_is_a_solution(aria):

    if abs(aria[0][0] - aria[0][1]) >= EPSILON or abs(aria[1][0] - aria[1][1]) >= EPSILON:
        return True
        
    args_b = np.array([aria[0][0], aria[1][0], aria[2][0], aria[3][0], aria[4][0], aria[5][0]])
    args_e = np.array([aria[0][1], aria[1][1], aria[2][1], aria[3][1], aria[4][1], aria[5][1]])   

    if not(is_a_zero(first_equation, minus_first_equation, "SLSQP", aria)):
        if not(is_a_zero(first_equation, minus_first_equation, "L-BFGS-B", aria)):
            return False

    if not(is_a_zero(second_equation, minus_second_equation, "SLSQP", aria)):
        if not(is_a_zero(second_equation, second_equation, "L-BFGS-B", aria)):
            return False

    if not(is_a_zero(third_equation, minus_third_equation, "SLSQP", aria)):
        if not(is_a_zero(third_equation, minus_third_equation, "L-BFGS-B", aria)):
            return False

    return True

def calculating():

    res = np.array([initial_limits()])
    for i in range(2):
        cur_areas = res
        while res.size != 0:
            res = np.delete(res, 0, 0)
        while(cur_areas.size != 0):
            if(there_is_a_solution(np.array(cur_areas[0]))):
                if abs(cur_areas[0][i][1] - cur_areas[0][i][0]) < EPSILON or i >= 2:
                    res = np.append(res, np.array([cur_areas[0]]), 0)
                    cur_areas = np.delete(cur_areas, 0, 0)
                else :
                    tmp1 = np.array(cur_areas[0]);
                    tmp2 = np.array(cur_areas[0]);
                    cur_areas = np.delete(cur_areas, 0, 0)
                    middle = (tmp1[i][1] - tmp1[i][0]) / 2
                    tmp1[i][1] = tmp1[i][0] + middle
                    tmp2[i][0] = tmp1[i][0] + middle			
                    cur_areas = np.append(cur_areas, np.array([tmp1, tmp2]), 0)
            else :
                cur_areas = np.delete(cur_areas, 0, 0)

    return res


#a_phi = float(input("Enter angle of rootation\nangel = "))
a_phi = 0
areas = calculating()

print("Quontity of boxes = ", areas.size/12)

boxes = np.array([])
n = 0
while areas.size != 0:
    boxes = np.append(boxes, [box.Box(areas[0], n)], 0)
    n = n + 1
    areas = np.delete(areas, 0, 0)

for i in range(boxes.size):
    for j in range(boxes.size):
        if j == i:
            continue
        if boxes[i].is_neighbor(boxes[j]):
            boxes[i].add_neighbor(boxes[j])
            
#for i in range(boxes.size):
#    print(boxes[i].neighbors.size)

#x1 = float(input("x1 = "))
#y1 = float(input("y1 = "))
#x2 = float(input("x2 = "))
#y2 = float(input("y2 = "))

x1 = 1.0
y1 = 0.8
x2 = 2.0
y2 = 0.8

trajectory = di.trajectory_search(boxes, x1, y1, x2, y2)
dr.draw(boxes, trajectory)


