import math
import scipy.optimize as so
import numpy as np
import datetime
import box
import jacobian

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
    res[2][0] = -math.pi
    res[3][0] = -math.pi
    res[4][0] = -math.pi
    res[5][0] = -math.pi

    res[0][1] = x_interval[1]
    res[1][1] = y_interval[1]
    res[2][1] = math.pi
    res[3][1] = math.pi
    res[4][1] = math.pi
    res[5][1] = math.pi

    return box.Box(res)

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

def is_a_zero(func, minus_func, method, box):

    args_b = box.get_bcoors()
    args_e = box.get_ecoors()   
    bnd = ((args_b[0], args_e[0]), (args_b[1], args_e[1]), (args_b[2], args_e[2]), (args_b[3], args_e[3]), (args_b[4], args_e[4]), (args_b[5], args_e[5]))

    min_solut = so.minimize(func,  (args_e + args_b) / 2., method=method, bounds = bnd)
    max_solut = so.minimize(minus_func, (args_e + args_b) / 2., method=method, bounds = bnd)

    max_of_f = -max_solut.fun
    min_of_f = min_solut.fun

    if not(max_of_f >= 0. and min_of_f <= 0.):
        return False

    return True

def optimization(box):

    if not(is_a_zero(first_equation, minus_first_equation, "SLSQP",box)):
        if not(is_a_zero(first_equation, minus_first_equation, "L-BFGS-B", box)):
            return False

    if not(is_a_zero(second_equation, minus_second_equation, "SLSQP", box)):
        if not(is_a_zero(second_equation, second_equation, "L-BFGS-B", box)):
            return False

    if not(is_a_zero(third_equation, minus_third_equation, "SLSQP", box)):
        if not(is_a_zero(third_equation, minus_third_equation, "L-BFGS-B", box)):
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

def inverse_problem(box):
    phi = 0
    while phi <= 2 * math.pi:
        if has_solution(box.centre_x, box.centre_y, phi):
            return True
        phi = phi + math.pi / 8.

    return False

def start_divide(result, box):
    if box.is_valid_size():
        return check_valid_size(result, box)
    all_valid = True
    all_notvalid = True
    for i in range(4):
        r = True
        if box.checks[i] == -1:
            r = False
        elif box.checks[i] == 1:
            r = True
        else:
            r = inverse_problem(box.get_angle_box(i))
            box.checks[i] = 1 if r else -1
        if r:
            all_notvalid = False
        else:
            all_valid = False
    if all_notvalid:
        if box.how_many_valid_size() > 5:
            if not optimization(box):
                return result
    elif all_valid:
        return devide_until_valid_size(result, box)
    box1, box2 = box.split()
    result = start_divide(result, box1)
    if box2 is not None:
        result = start_divide(result, box2)
    return result

def devide_until_valid_size(result, box):
    box1, box2 = box.split()
    if box1.is_valid_size():
        result = np.append(result, np.array([box1]), 0)
    else:
#        print("box1 ")
#        box1.print_box_only()
        result = devide_until_valid_size(result, box1)
    if box2 is not None:
        if box2.is_valid_size():
            result = np.append(result, np.array([box2]), 0)
        else:
#            print("box2 ")
#            box2.print_box_only()
            result = devide_until_valid_size(result, box2)
    return result

def check_valid_size(result, box):
    if inverse_problem(box):
        box.checks = np.array([1, 1, 1, 1])
        result = np.append(result, [box], 0)
    return result

def calculate_with_singularity(result, singularity, box):
    if box.is_valid_size():
        return check_valid_size_with_singularity(result, singularity, box)
    all_valid = True
    all_notvalid = True
    for i in range(4):
        r = True
        if box.checks[i] == -1:
            r = False
        elif box.checks[i] == 1:
            r = True
        else:
            r = inverse_problem(box.get_angle_box(i))
            box.checks[i] = 1 if r else -1
        if r:
            all_notvalid = False
        else:
            all_valid = False
    if all_notvalid:
        if box.how_many_valid_size() > 5:
            if not optimization(box):
                return result, singularity
    elif all_valid:
        return devide_until_valid_size_with_singularity(result, singularity, box)
    box1, box2 = box.split()
    result, singularity = calculate_with_singularity(result, singularity, box1)
    if box2 is not None:
        result, singularity = calculate_with_singularity(result, singularity, box2)
    return result, singularity

def check_valid_size_with_singularity(result, singularity, box):
    if inverse_problem(box):
        if jacobian.is_jacobian_deg(box.coordinates):
            singularity = np.append(singularity, box)
        else:
            box.checks = np.array([1, 1, 1, 1])
            result = np.append(result, [box], 0)
    return result, singularity


def devide_until_valid_size_with_singularity(result, singularity, box):
    box1, box2 = box.split()
    if box1.is_valid_size():
        if jacobian.is_jacobian_deg(box1.coordinates):
            singularity = np.append(singularity, box1)
        else:
            result = np.append(result, np.array([box1]), 0)
    else:
        if jacobian.is_jacobian_deg(box1.coordinates):
            result, singularity = devide_until_valid_size_with_singularity(result, singularity, box1)
        else:
            result = devide_until_valid_size(result, box1)
#        print("box1 ")
#        box1.print_box_only()
    if box2 is not None:
        if box2.is_valid_size():
            if jacobian.is_jacobian_deg(box2.coordinates):
                singularity = np.append(singularity, box2)
            else:
                result = np.append(result, np.array([box2]), 0)
        else:
#            print("box2 ")
#            box2.print_box_only()
            if jacobian.is_jacobian_deg(box2.coordinates):
                result, singularity = devide_until_valid_size_with_singularity(result, singularity, box2)
            else:
                result = devide_until_valid_size(result, box2)
    return result, singularity

