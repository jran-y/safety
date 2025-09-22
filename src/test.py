import math
import numpy as np
import functions as fc
from scenarios import init_scence


def main():
    # check scenarios running -- create vehicle success
    # vehicle1, vehicle2 = init_scence()
    # print("init_scence() OK, get two vehicles")
    # print("Vehicle 1: ", vehicle1)
    # print("Vehicle 1: ", vehicle2)

    # test rotation
    g = np.array([1.0, 2.0], float)
    l, w = 4.0, 2.0
    theta = math.radians(90)

    # p = (g[0]+l/2, g[1])
    # new_p = fc.rotation(p, theta)

    # print("p coor: ", p)
    # print("p after rotation coor: ", new_p)

    # all point check
    # points = fc.all_points(g, l, w, theta)
    # print("All points coor: ", points)

    v = 5
    w = 10
    a = 2

    print("Orignial coor = ", g, "v = ", v, "theta = ", theta)
    
    new_g, new_v, new_theta = fc.movement(g, v, w, a, theta, 0.1)
    print("After moving new central point coor = ",  new_g, "v = ", new_v, "theta = ", new_theta)

if __name__ == "__main__":
    main()
