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

import math
import numpy as np

import functions as fc
from scenarios import init_scence

def main():
    # get g1 g2 coor at (0, 0)
    vehicle1, vehicle2 = init_scence()

    print("Vehicle1 state: ", vehicle1, "Vehicle2 state: ", vehicle2)

    # find all points at initial moment -- step 0.5?
    # pts1 = fc.all_points(vehicle1.g, vehicle1.length, vehicle1.width, vehicle1.theta)
    # pts2 = fc.all_points(vehicle2.g, vehicle2.length, vehicle2.width, vehicle2.theta)

    # intialization setting
    dt = 0.05   # delta t -- step
    max_step = 100
    alpha_prev = 0.0

    for step in range(max_step):
        # g1 g2 coor after moving
        vehicle1.g, vehicle1.v, vehicle1.theta = fc.movement(vehicle1.g, vehicle1.v, vehicle1.w, vehicle1.a, vehicle1.theta, dt)
        vehicle2.g, vehicle2.v, vehicle2.theta = fc.movement(vehicle2.g, vehicle2.v, vehicle2.w, vehicle2.a, vehicle2.theta, dt)

        print("After moving Vehicle1 state: ", vehicle1, "Vehicle2 state: ", vehicle2)

        # find all points
        pts1 = fc.all_points(vehicle1.g, vehicle1.length, vehicle1.width, vehicle1.theta)
        pts2 = fc.all_points(vehicle2.g, vehicle2.length, vehicle2.width, vehicle2.theta)

        # find min distance and p1 p2 coor
        d_min, p1, p2 = fc.min_dis(pts1, pts2)

        rel_v, alpha_prev = fc.relative_speed(p1, p2, vehicle1.v, vehicle2.v, vehicle1.theta, vehicle2.theta, alpha_prev)

        # if d_min <= 0:
        #     print("!! Collision")
        #     print("Min distance: ", d_min, "point on V1: ", p1, "point on V2: ", p2)
        #     print("Relative speed: ", rel_v)
        #     break
        
        # print("Min distance: ", d_min, "point on V1: ", p1, "point on V2: ", p2)
        # print("Relative speed: ", rel_v)

        # if rel_v ≈ 0
        if abs(rel_v) < 1e-3:
            print(f"[break] step={step}, d_min={d_min:.3f}, rel_v≈0")
            break

if __name__ == "__main__":
    main()