import numpy as np
import math
import sys

# print(round(1.100001,2), 'test')
# for i in np.arange(2,-0.1,-0.4):
#     print(i, "ttttttestttt")
# sys.exit()

# theta is radian
# coor from points, min_dis points set
# new_x new_y for current 
def rotation(coor, theta): # theta = "COUNTER"ClockW;
    new_x = coor[0] * np.cos(theta) - coor[1] * np.sin(theta)
    new_y = coor[0] * np.sin(theta) + coor[1] * np.cos(theta)
    return (new_x,new_y)


# g for central point coor, l for length, w for width, n for 4 corner points
def all_points(g, l, w, theta): # x+ (axis) is from rear to front of the vehicle
    points = []
    n = [g[0] + l / 2, g[1] + w / 2]
    # points on upper boundary, from right to left
    # lose point?
    for i in np.arange(n[0],n[0]-l-0.1,-0.2):
        points.append([round(i,2), n[1]])
    n = [g[0] - l / 2, g[1] + w / 2]
    # points on left boundary, from top to bottom
    for j in np.arange(n[1],n[1]-w-0.1,-0.2):
        points.append([n[0], round(j,2)])
    # points on bottom boundary, from left to right
    n = [g[0] - l / 2, g[1] - w / 2]
    for i in np.arange(n[0],n[0]+l+0.1,0.2):
        points.append([round(i,2), n[1]])
    # points on right boundary, from bottom to top
    n = [g[0] + l / 2, g[1] - w / 2]
    for j in np.arange(n[1],n[1]+w+0.1,0.2):
        points.append([n[0], round(j,2)])
    points = [rotation(p, theta) for p in points]
    return points
    

# central point movement
def movement(g, v, w, a, theta, step): 
    g[0] += v * np.cos(theta)*step
    g[1] += v * np.sin(theta)*step
    v += a * step
    theta += w*step
    return g, v, theta

# return min_distance and points 
def min_dis(points1, points2):
    distance = float("inf") # float max value
    min_p1 = []
    min_p2 = []
    for i in points1:
        for j in points2:
            d = math.hypot(j[0]-i[0], j[1]-i[1])
            if d < distance:
                distance = d
                min_p1 = i
                min_p2 = j
    return distance, min_p1, min_p2

# alpha is the relative angle of min_distance and x-axis
def relative_speed(p1,p2,v1,v2,theta1, theta2, alpha): # alpha as the input is the min distance angle of the last time. Used when p1=p2
    # consider np.arctan2(dy,dx)？
    if p2[1]-p1[1] != 0:
        alpha = np.arctan((p2[0]-p1[0])/(p2[1]-p1[1]))
    # min_dis relative speed
    delta_speed = v1 * np.cos(theta1 - alpha) - v2 * np.cos(theta2 - alpha)
    return delta_speed

#---- in main.py (better to be another file in pycharm) ----------
# Step 0: find P_1 and P_2 as (0,0) and (min_distance, 0). find g1 and g2 accordingly.
# Step 0.5 (optional maybe): use [all_points] to find all points of one/each vehicle at the current time
# Step 1: simulation:
#   for t in range(0, 10000000):
#       [movement]
#       [all_points]
#       [min_dis]
#       [relative_speed]
#       if relative_speed == 0:
#           ... and break
#   calculate d1, d2, dm_n etc.


# PDF Example: suppose X ~ Uniform(-1,1), Y ~ Uniform(-1,1)
# PS: for each sample in n, derive one dm_n value so the simulation above should be within another loop for N in range(n)
# n, v1, v2 and a should be derived from Chattanooga data
n = 100000000 # sample size
v1 = np.random.uniform(-1, 1, n)
v2 = np.random.uniform(-1, 1, n)
a = np.random.uniform(-1, 1, n)


dm_n = np.sqrt(v1**2 + v2**2 + a)
k, section = np.histogram(dm_n, bins=100, density=True)
section_center = (section[:-1] + section[1:]) / 2