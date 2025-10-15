from typing import Dict
import numpy as np
from src.scenarios import get_scenario
from src.scenarios.car_following import VehicleState

def _clip(x, lo, hi):
    return lo if x < lo else hi if x > hi else x

def _gap(lead: VehicleState, foll: VehicleState) -> float:
    return (lead.g[1] - lead.length) - foll.g[1]

def lead_control_redlight(lead: VehicleState, env: Dict, a_brake: float = 2.5, roll_margin: float = 0.3) -> float:
    stop_y = float(env["stop_line_y"])
    dist = (stop_y - roll_margin) - lead.g[1]
    v = lead.v
    if dist <= 0.0:
        return -6.0 if v > 0.05 else 0.0
    a_need = - (v*v) / max(0.2, 2.0*dist)
    return -a_brake if a_need < -1e-6 else 0.0

def follower_control_simple(foll: VehicleState, lead: VehicleState, desired_gap: float = 8.0, a_plus: float = 1.2, a_minus: float = 2.0, v_des: float = 15.0) -> float:
    g = _gap(lead, foll)
    if g < desired_gap:
        return -a_minus
    elif (g > desired_gap + 2.0) and (foll.v < v_des):
        return a_plus
    else:
        return 0.0

def step(state: VehicleState, a_cmd: float, dt: float) -> VehicleState:
    v = _clip(state.v + a_cmd*dt, 0.0, 70.0)
    y = state.g[1] + v*dt
    return VehicleState(
        g=np.array([state.g[0], y], float),
        v=float(v),
        a=float(a_cmd),
        w=state.w,
        theta=state.theta,
        length=state.length,
        width=state.width
    )

def run_simple(name: str = "car_following", dt: float = 0.1, T: float = 30.0):
    v1, v2, env = get_scenario(name)
    steps = int(T/dt) + 1
    t = np.linspace(0.0, T, steps)
    lead_y = np.zeros(steps); lead_v = np.zeros(steps)
    foll_y = np.zeros(steps); foll_v = np.zeros(steps)
    gaps = np.zeros(steps)
    for k, tk in enumerate(t):
        lead_y[k], lead_v[k] = v1.g[1], v1.v
        foll_y[k], foll_v[k] = v2.g[1], v2.v
        gaps[k] = _gap(v1, v2)
        a_lead = lead_control_redlight(v1, env)
        a_foll = follower_control_simple(v2, v1)
        v1 = step(v1, a_lead, dt)
        v2 = step(v2, a_foll, dt)
    return {
        "t": t,
        "lead_y": lead_y, "lead_v": lead_v,
        "foll_y": foll_y, "foll_v": foll_v,
        "gap": gaps,
        "env": env,
        "dt": dt, "T": T
    }

def _print_summary(out):
    t = out["t"]
    gy1, gv1 = out["lead_y"], out["lead_v"]
    gy2, gv2 = out["foll_y"], out["foll_v"]
    gap = out["gap"]
    env = out["env"]
    dt = out["dt"]; T = out["T"]
    i_min = int(np.argmin(gap))
    print("=== car_following simulation ===")
    print(f"duration: {T:.1f}s | dt: {dt:.3f}s | steps: {len(t)}")
    print(f"env: type={env.get('type','?')}, stop_line_y={env.get('stop_line_y',float('nan')):.2f}, light_state={env.get('light_state','?')}")
    print("stats:")
    print(f"  min_gap: {gap[i_min]:.2f} m at t={t[i_min]:.1f}s")
    print(f"  final: lead(y={gy1[-1]:.2f}, v={gv1[-1]:.2f}), foll(y={gy2[-1]:.2f}, v={gv2[-1]:.2f})")
    kstep = max(1, int(round(1.0/dt)))
    idx = list(range(0, len(t), kstep))
    if idx[-1] != len(t)-1:
        idx.append(len(t)-1)
    print("\nTime[s]  lead_y[m]  lead_v[m/s]  foll_y[m]  foll_v[m/s]   gap[m]")
    for i in idx:
        print(f"{t[i]:6.1f}  {gy1[i]:9.2f}  {gv1[i]:11.2f}  {gy2[i]:9.2f}  {gv2[i]:11.2f}  {gap[i]:7.2f}")

if __name__ == "__main__":
    out = run_simple("car_following", dt=0.1, T=30.0)
    _print_summary(out)