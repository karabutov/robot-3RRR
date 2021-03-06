import math
import numpy as np
import scipy.optimize as so

size_side = 1.
k = (2./3.) * (size_side * math.sqrt(3.) / 2.)
l = 1.

gamma1 = math.pi * (0.5 + 1. * 2./3.) 
gamma2 = math.pi * (0.5 + 2. * 2./3.) 
gamma3 = math.pi * (0.5 + 3. * 2./3.)

x1 = 0.0
y1 = 0.0
x2 = 3.4
y2 = 0.0
x3 = 1.7
y3 = 2.94

def jacobian_matrix(x, y, phi, theta1, theta2, theta3):

    def dx1(x, y, phi, theta1, theta2, theta3):
        xB1 = x1 + l * math.cos(theta1)
        return 2*(x + k*math.cos(gamma1+phi) - xB1)

    def dy1(x, y, phi, theta1, theta2, theta3):
        yB1 = y1 + l * math.sin(theta1)
        return 2*(y + k*math.sin(gamma1+phi) - yB1)

    def dphi1(x, y, phi, theta1, theta2, theta3):
        xB1 = x1 + l * math.cos(theta1)		
        yB1 = y1 + l * math.sin(theta1)
        return 2*k*math.cos(gamma1+phi) * (y + k*math.sin(gamma1+phi) - yB1) - 2*k*math.sin(gamma1+phi) * (x + k*math.cos(gamma1+phi) - xB1)

    def dx2(x, y, phi, theta1, theta2, theta3):
        xB2 = x2 + l * math.cos(theta2)
        return 2*(x + k*math.cos(gamma2+phi) - xB2)

    def dy2(x, y, phi, theta1, theta2, theta3):
        yB2 = y2 + l * math.sin(theta2)
        return 2*(y + k*math.sin(gamma2+phi) - yB2)

    def dphi2(x, y, phi, theta1, theta2, theta3):
        xB2 = x2 + l * math.cos(theta2)
        yB2 = y2 + l * math.sin(theta2)
        return 2*k*math.cos(gamma2+phi) * (y + k*math.sin(gamma2+phi) - yB2) - 2*k*math.sin(gamma2+phi) * (x + k*math.cos(gamma2+phi) - xB2)

    def dx3(x, y, phi, theta1, theta2, theta3):
        xB3 = x3 + l * math.cos(theta3) 
        return 2*(x + k*math.cos(gamma3+phi) - xB3)

    def dy3(x, y, phi, theta1, theta2, theta3):
        yB3 = y3 + l * math.sin(theta3)	
        return 2*(y + k*math.sin(gamma3+phi) - yB3)

    def dphi3(x, y, phi, theta1, theta2, theta3):
        xB3 = x3 + l * math.cos(theta3) 
        yB3 = y3 + l * math.sin(theta3)	
        return 2*k*math.cos(gamma3+phi) * (y + k*math.sin(gamma3+phi) - yB3) - 2*k*math.sin(gamma3+phi) * (x + k*math.cos(gamma3+phi) - xB3)


    return np.array([[dx1(x, y, phi, theta1, theta2, theta3), dy1(x, y, phi, theta1, theta2, theta3), dphi1(x, y, phi, theta1, theta2, theta3)],
                     [dx2(x, y, phi, theta1, theta2, theta3), dy2(x, y, phi, theta1, theta2, theta3), dphi2(x, y, phi, theta1, theta2, theta3)],
                         [dx3(x, y, phi, theta1, theta2, theta3), dy3(x, y, phi, theta1, theta2, theta3), dphi3(x, y, phi, theta1, theta2, theta3)]])



def constr1(t):
    x = t[0]
    y = t[1]
    phi = t[2]
    theta1 = t[3]
    xB1 = x1 + l * math.cos(theta1)
    yB1 = y1 + l * math.sin(theta1)

    return (x + k * math.cos(gamma1 + phi) - xB1)**2 + (y + k * math.sin(gamma1 + phi) - yB1)**2 - l**2

def constr2(t):
    x = t[0]
    y = t[1]
    phi = t[2]
    theta2 = t[4]
    xB2 = x2 + l * math.cos(theta2)
    yB2 = y2 + l * math.sin(theta2)

    return (x + k * math.cos(gamma2 + phi) - xB2)**2 + (y + k * math.sin(gamma2 + phi) - yB2)**2 - l**2


def constr3(t):
    x = t[0]
    y = t[1]
    phi = t[2]
    theta3 = t[5]
    xB3 = x3 + l * math.cos(theta3) 
    yB3 = y3 + l * math.sin(theta3)
       
    return (x + k * math.cos(gamma3 + phi) - xB3)**2 + (y + k * math.sin(gamma3 + phi) - yB3)**2 - l**2


def params(centr_x, centr_y, angle_of_rot):			

    def triangl_evertex(i):
        return centr_x + k * math.cos(math.pi * (0.5 + i * 2 / 3.0) + angle_of_rot), centr_y + k * math.sin(math.pi * (0.5 + i * 2 / 3.0) + angle_of_rot)

    def angles(topx, topy, x, y):
        if abs(math.sqrt((x - topx)**2 + (y - topy)**2) / (2 * l)) > 1.:
            return 0, 0
        alpha = math.acos(math.sqrt((x - topx)**2 + (y - topy)**2) / (2 * l))
        if topx != x:
            betta = math.atan((topy - y) / (topx - x))
        elif topy - y > 0:
            betta = math.pi / 2
        elif topy - y < 0:
            betta = -math.pi / 2			
        if topx - x < 0:
            betta += math.pi
        return alpha + betta, betta - alpha
	
    top_x, top_y = triangl_evertex(1)	
    angle1, angle2 = angles(top_x, top_y, x1, y1)
    theta1 = angle1
    top_x, top_y = triangl_evertex(2)
    angle1, angle2 = angles(top_x, top_y, x2, y2)
    theta2 = angle1
    top_x, top_y = triangl_evertex(3)	
    angle1, angle2 = angles(top_x, top_y, x3, y3)
    theta3 = angle1
    return theta1, theta2, theta3


def det_jacobian_func(args):
    x =	args[0]
    y =	args[1] 
    phi = args[2]
    theta1 = args[3]
    theta2 = args[4]
    theta3 = args[5]
    #theta1, theta2, theta3 = params(x, y, phi)
    j = np.array(jacobian_matrix(x, y, phi, theta1, theta2, theta3))
    return np.linalg.det(j)
    #return j[0][0] * j[1][1] * j[2][2] + j[0][2] * j[1][0] * j[2][1] + j[2][0] * j[0][1] * j[1][2] - j[0][2] * j[1][1] * j[2][0] - j[0][0] * j[2][1] * j[1][2] - j[2][2] * j[1][0] * j[0][1]

def minus_det_jacobian_func(args):
    return -1 * det_jacobian_func(args)

def is_jacobian_deg(aria):
    args_b = np.array([aria[0][0], aria[1][0], 0.3, 0. , 0. , 0.])
    args_e = np.array([aria[0][1], aria[1][1], 0.3, 2. * math.pi, 2. * math.pi, 2. * math.pi])

    bnd = ((args_b[0], args_e[0]), (args_b[1], args_e[1]), (args_b[2], args_e[2]), (args_b[3], args_e[3]), (args_b[4], args_e[4]), (args_b[5], args_e[5]))

    cons = ({'type': 'eq', 'fun': constr1},
            {'type': 'eq', 'fun': constr2},
            {'type': 'eq', 'fun': constr3})

    min_solut = so.minimize(det_jacobian_func, (args_e + args_b) / 2., method="SLSQP", bounds = bnd, constraints = cons)
    max_solut = so.minimize(minus_det_jacobian_func, (args_e + args_b) / 2., method="SLSQP", bounds = bnd, constraints = cons)
    max_of_f = -max_solut.fun
    min_of_f = min_solut.fun


    if max_of_f >= 0. and min_of_f <= 0.:
        return True

    return False

def singularity_points(boxes):
    singularity = np.array([])
    valid_boxes = np.array([])
    for i in range(boxes.size):
        if is_jacobian_deg(boxes[i].coordinates):
            singularity = np.append(singularity, boxes[i])
        else:
            valid_boxes = np.append(valid_boxes, boxes[i])
    return singularity, valid_boxes
    
            