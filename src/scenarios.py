import math
import numpy as np
from dataclasses import dataclass

@dataclass
class VehicleState:
    g: np.ndarray
    v: float
    a: float
    w: float
    theta: float #radiam
    length: float
    width:  float

def init_scence():
    vehicle1 = VehicleState(
        g = np.array([0.0, 0.0], float),
        v = 6.0,
        a = 0.0,
        w = 0.0,
        theta = math.radians(0),
        length = 4.5,
        width = 1.9
    )

    vehicle2 = VehicleState(
        g = np.array([8.0, 1.0], float),
        v = 6.0,
        a = 0.0,
        w = 0.0,
        theta = math.radians(0),
        length = 4.5,
        width = 1.9
    )

    return vehicle1, vehicle2