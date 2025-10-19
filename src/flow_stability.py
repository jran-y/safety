import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

FILE = "Aug-13th-noon.csv"
LABEL = "2024-08-13"
# 5 minutes rolling window
ROLL_W = 5
# max time in CSV is 1.7e+9 us, so us is enough
TIME_UNIT = "us"
FILTER_CLASS = "VEHICLE"

SRC_DIR = Path(__file__).resolve().parent
ROOT_DIR = SRC_DIR.parent
DATA_DIR = ROOT_DIR / "data"
OUT_DIR = SRC_DIR / "outputs"
GRAPHS_DIR = OUT_DIR / "graphs"
GRAPHS_DIR.mkdir(parents=True, exist_ok=True)

# Load data and aggregate vehicle counts per minute
def load_and_aggregate(csv_name: str) -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / csv_name, usecols=["UUID", "CLASSIFICATION", "frame_ts"])

    df = df[df["CLASSIFICATION"] == "VEHICLE"].copy()

    ts = df["frame_ts"].astype("float64")
    df["t_sec"] = (ts - ts.min())/1e6  # to seconds

    df["minute"] = (df["t_sec"] // 60).astype(int)
    g = (
        df.groupby("minute")["UUID"]
          .nunique()
          .reset_index(name="veh_count")
          .sort_values("minute")
    )
    return g

def main():
    g = load_and_aggregate(FILE)

    mean_val = g["veh_count"].mean()
    std_val  = g["veh_count"].std(ddof=1)
    cv_val   = std_val / mean_val if mean_val > 0 else float("nan")

    g_s = g.assign(veh_count_smooth=g["veh_count"].rolling(ROLL_W, center=True, min_periods=1).mean())

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(g["minute"], g["veh_count"], lw=1.2, alpha=0.45, label="per-minute (raw)")
    ax.plot(g_s["minute"], g_s["veh_count_smooth"], lw=2.2, label=f"rolling mean ({ROLL_W} min)")

    ax.axhline(mean_val, ls=":", lw=1, alpha=0.35)
    ax.set_xlim(0, 60)
    ax.set_title(f"Vehicle Flow Stability ({LABEL}) — CV = {cv_val:.2f} (<0.20 → stable)")
    ax.set_xlabel("Minute of Hour")
    ax.set_ylabel("Vehicle Count per Minute")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="upper right", frameon=False)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    info = f"mean = {mean_val:.1f}\nCV   = {cv_val:.2f}"
    ax.text(0.985, 0.1, info, transform=ax.transAxes,
        ha="right", va="bottom",
        bbox=dict(boxstyle="round", alpha=0.15, pad=0.35))

    out_png = GRAPHS_DIR / "flow_stability_single.png"
    fig.savefig(out_png, dpi=220, bbox_inches="tight")
    print(f"[OK] Figure saved: {out_png}")

if __name__ == "__main__":
    main()