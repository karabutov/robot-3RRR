import math
import scipy.optimize as so
import numpy as np
import datetime

EPSILON = 0.3
ANGLE = 4.


size_side = 1.
k = (2./3.) * (size_side * math.sqrt(3.) / 2.)
l = 1.

gamma1 = math.pi * (0.5 + 1. * 2./3.) 
gamma2 = math.pi * (0.5 + 2. * 2./3.) 
gamma3 = math.pi * (0.5 + 3. * 2./3.)

tprof2 = 0
tprof3 = 0

x1 = 0.0
y1 = 0.0
x2 = 3.4
y2 = 0.0
x3 = 1.7
y3 = 2.94

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

    res = np.zeros((6, 2))
    res[0][0] = x_interval[0]
    res[1][0] = y_interval[0]
    res[2][0] = 0
    res[3][0] = 0
    res[4][0] = 0
    res[5][0] = 0

    res[0][1] = x_interval[1]
    res[1][1] = y_interval[1]
    res[2][1] = 2 * math.pi
    res[3][1] = 2 * math.pi
    res[4][1] = 2 * math.pi
    res[5][1] = 2 * math.pi

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



def function(args):
    return math.sqrt(first_equation(args)**2 + second_equation(args)**2 + third_equation(args)**2)

def function1(args):
    return abs(first_equation(args)) + abs(second_equation(args)) + abs(third_equation(args))

def convolution(args):
    args_b = np.array([aria[0][0], aria[1][0], aria[2][0], aria[3][0], aria[4][0], aria[5][0]])
    args_e = np.array([aria[0][1], aria[1][1], aria[2][1], aria[3][1], aria[4][1], aria[5][1]])

    bnd = ((args_b[0], args_e[0]), (args_b[1], args_e[1]), (args_b[2], args_e[2]), (args_b[3], args_e[3]), (args_b[4], args_e[4]), (args_b[5], args_e[5]))

    res = min_solut = so.minimize(function1,  (args_e + args_b) / 2., method="L-BFGS-B", bounds = bnd)
    if abs(res.fun < EPSILON):
        return True
    
    res = min_solut = so.minimize(function1,  (args_e + args_b) / 2., method="SLSQP", bounds = bnd)
    if abs(res.fun < EPSILON):
        return True
    
    res = min_solut = so.minimize(function1,  (args_e + args_b) / 2., method="TNC", bounds = bnd)
    if abs(res.fun < EPSILON):
        return True

    res = min_solut = so.minimize(function,  (args_e + args_b) / 2., method="L-BFGS-B", bounds = bnd)
    if abs(res.fun < EPSILON):
        return True
    
    res = min_solut = so.minimize(function,  (args_e + args_b) / 2., method="SLSQP", bounds = bnd)
    if abs(res.fun < EPSILON):
        return True
    
    res = min_solut = so.minimize(function,  (args_e + args_b) / 2., method="TNC", bounds = bnd)
    if abs(res.fun < EPSILON):
        return True
    
    return False



def is_a_zero(func, minus_func, method, bnd):
    
    min_solut = so.minimize(func,  (args_e + args_b) / 2., method=method, bounds = bnd)
    max_solut = so.minimize(minus_func, (args_e + args_b) / 2., method=method, bounds = bnd)

    max_of_f = -max_solut.fun
    min_of_f = min_solut.fun
    
    if not(max_of_f >= 0. and min_of_f <= 0.):
        return False
    
    return True

def optimization(aria):

    args_b = np.array([aria[0][0], aria[1][0], aria[2][0], aria[3][0], aria[4][0], aria[5][0]])
    args_e = np.array([aria[0][1], aria[1][1], aria[2][1], aria[3][1], aria[4][1], aria[5][1]])   
    bnd = ((args_b[0], args_e[0]), (args_b[1], args_e[1]), (args_b[2], args_e[2]), (args_b[3], args_e[3]), (args_b[4], args_e[4]), (args_b[5], args_e[5]))
    if not(is_a_zero(first_equation, minus_first_equation, "SLSQP",bnd)):
        if not(is_a_zero(first_equation, minus_first_equation, "L-BFGS-B", bnd)):
            return False

    if not(is_a_zero(second_equation, minus_second_equation, "SLSQP", bnd)):
        if not(is_a_zero(second_equation, second_equation, "L-BFGS-B", bnd)):
            return False

    if not(is_a_zero(third_equation, minus_third_equation, "SLSQP", bnd)):
        if not(is_a_zero(third_equation, minus_third_equation, "L-BFGS-B", bnd)):
            return False

    return True


def has_solution(centr_x, centr_y, angle_of_rot):			

    try:
        def triangl_evertex(i):
            return centr_x + k * math.cos(math.pi * (0.5 + i * 2 / 3.0) + angle_of_rot), centr_y + k * math.sin(math.pi * (0.5 + i * 2 / 3.0) + angle_of_rot)

        def angles(topx, topy, x, y):
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
    except ValueError:
        return False
    return True

def inverse_problem(aria):
    centre_x = aria[0][0] + (aria[0][1] - aria[0][0])/2
    centre_y = aria[1][0] + (aria[1][1] - aria[1][0])/2
    
    phi = 0
    while phi <= 2 * math.pi:
        if has_solution(centre_x, centre_y, phi):
            return True
        phi = phi + math.pi / 8.

    return False

def there_is_a_solution(aria, method):

    if abs(aria[0][0] - aria[0][1]) >= EPSILON or abs(aria[1][0] - aria[1][1]) >= EPSILON:
        return True

    if method == "op":    
        return optimization(aria)

    if method == "ip":
        return inverse_problem(aria)

    if method == "co":
        return convolution(aria)


def calculating(method):
    TPROF1 = 0
    TPROF2 = datetime.datetime.now()
    TPROF3 = datetime.datetime.now()
    res = np.array([initial_limits()])
    ncycle = 0
    for i in range(3):
        cur_areas = res
        res = np.empty((0,6,2,), dtype=np.float64)
#        print("Arrays", res, cur_areas.shape)
        print("cur_areas", cur_areas.shape)
        while(cur_areas.size != 0):
            c_area = cur_areas[0];
            cur_areas = np.delete(cur_areas, 0, 0)
            tps1 = datetime.datetime.now()
            issol = there_is_a_solution(np.array(c_area), method);
            tps2 = datetime.datetime.now() - tps1
            TPROF1 = TPROF1 + tps2.microseconds
            if(issol):
                if abs(c_area[i][1] - c_area[i][0]) < (EPSILON if i <= 1 else ANGLE):
                    res = np.append(res, np.array([c_area]), 0)
                else :
                    tmp1 = np.array(c_area);
                    tmp2 = np.array(c_area);

                    middle = (tmp1[i][1] - tmp1[i][0]) / 2
                    tmp1[i][1] = tmp1[i][0] + middle
                    tmp2[i][0] = tmp1[i][0] + middle			
                    cur_areas = np.append(cur_areas, np.array([tmp1, tmp2]), 0)
            ncycle += 1
            if (ncycle%1000 == 0):
                tps2 = datetime.datetime.now()
                delta_all = tps2 - TPROF2
                delta1000 = tps2 - TPROF3
                print("C: " + str(ncycle) + "; " + str(i) + "; " + str(cur_areas.size) + " : " + str(res.size) + "; da: " + str(delta_all.seconds - TPROF1/1000000) + "; d1000: " + str(delta1000.seconds) + "; all: " + str(delta_all.seconds))
                TPROF3 = tps2
#        print("I: ", i, "cycles", ncycle, res[:,0:2,:])
                
    print("TPROF1", TPROF1, "cycles", ncycle)
    return res