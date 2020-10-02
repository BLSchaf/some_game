import math
# Intersection Stuff ---------------------------------------------- #

def get_slope(p1, p2):
    return (p2[1] - p1[1])*1. / (p2[0] - p1[0]) # y = mx + b | m := slope
    # ZeroDivisionError Bug - what if lines are vertical/horizontal

   
def get_y_intercept(slope, p1):
    return p1[1] - 1.*slope * p1[0] # y = mx+b -> b = y-mb | b:= y_intercept


def calc_intersect(line1, line2) :
    min_allowed = 1e-5   # guard against overflow
    big_value = 1e10     # use instead (if overflow would have occurred)

    try:
        m1 = get_slope(line1[0], line1[1])
    except ZeroDivisionError:
        m1 = big_value
        
    b1 = get_y_intercept(m1, line1[0])

    try:
        m2 = get_slope(line2[0], line2[1])
    except ZeroDivisionError:
        m2 = big_value
        
    b2 = get_y_intercept(m2, line2[0])

    if abs(m1 - m2) < min_allowed:
        x = big_value
    else:
        x = (b2 - b1) / (m1 - m2)
      
    y = m1 * x + b1
    #y2 = m2 * x + b2
    return (x,y)


def get_intersection(line1, line2):
    if line1[0] == line2[1] or line1[1] == line2[1] or line1[0] == line2[0] or line1[1] == line2[0]:
        return None
    intersection_pt = calc_intersect(line1, line2)

    if (line1[0][0] < line1[1][0]):
        if intersection_pt[0] < line1[0][0] or intersection_pt[0] > line1[1][0]:
            return None
    else:
        if intersection_pt[0] > line1[0][0] or intersection_pt[0] < line1[1][0]:
            return None
         
    if (line2[0][0] < line2[1][0]):
        if intersection_pt[0] < line2[0][0] or intersection_pt[0] > line2[1][0]:
            return None
    else:
        if intersection_pt[0] > line2[0][0] or intersection_pt[0] < line2[1][0]:
            return None

    return list(map(int, calc_intersect(line1, line2)))


# Line Stuff ---------------------------------------------- #
def get_coord_diff(start, end):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    return dx, dy

def get_distance(start, end):
    dx, dy = get_coord_diff(start, end)
    return math.sqrt(dx**2 + dy**2)

def get_angle(start, end):
    dx, dy = get_coord_diff(start, end)
    return math.atan2(-dy,dx) + math.pi #rads
##    degs = degrees(rads)
