# scenarios for car-following

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

def init_scene():
    red_light_y = 50.0
    stop_margin = 2.0

    v1 = VehicleState(
        g=np.array([0.0, 20.0], float),
        v=6.0,
        a=0.0,
        w=0.0,
        theta=math.radians(90),
        length=4.5,
        width=1.9
    )

    v2 = VehicleState(
        g=np.array([0.0, 10.0], float),
        v=6.0,
        a=0.0,
        w=0.0,
        theta=math.radians(90),
        length=4.5,
        width=1.9
    )

    env = {
        "type": "signalized_straight",
        "red_light_y": red_light_y,
        "stop_line_y": red_light_y - stop_margin,
        "light_state": "red"
    }

    return v1, v2, env