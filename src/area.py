import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ========= Config =========
CSV_PATH = ["safety/src/Aug-6th-noon.csv", "safety/src/Aug-13th-noon.csv"]
LON_COL  = "pos_x"       # longitude
LAT_COL  = "pos_y"       # latitude
OUT_IMG  = "area.png"

CENTER_COLOR = "red"
CENTER_MARKER = "X"
CENTER_SIZE = 90
CENTER_TEXT_DX = 6
CENTER_TEXT_DY = 6

POINT_SIZE = 4
# =======================

R_EARTH = 6371000.0

def haversine(lat1, lon1, lat2, lon2):
    p = math.pi/180.0
    dlat = (lat2-lat1)*p
    dlon = (lon2-lon1)*p
    a = math.sin(dlat/2)**2 + math.cos(lat1*p)*math.cos(lat2*p)*math.sin(dlon/2)**2

    return 2*R_EARTH*math.atan2(math.sqrt(a), math.sqrt(1-a))

# x-east y-north
def equirectangular_xy(lat, lon, lat0, lon0):
    x = (lon - lon0) * math.cos(lat0*math.pi/180) * (math.pi/180) * R_EARTH
    y = (lat - lat0) * (math.pi/180) * R_EARTH

    return x, y

# for print central point coor
def inverse_equirectangular_xy(x, y, lat0, lon0):
    lat = lat0 + (y / R_EARTH) * (180/math.pi)
    lon = lon0 + (x / (R_EARTH*math.cos(lat0*math.pi/180))) * (180/math.pi)

    return lat, lon

def convex_hull(points):
    pts = sorted(points)    # counter clock wise

    if len(pts) <= 1: return pts

    # sign: >0 left turn(CCW), <0 right turn(CW), =0 collinear
    def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2],lower[-1],p) <= 0: lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2],upper[-1],p) <= 0: upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]

def polygon_centroid(coords):
    n = len(coords)

    if n < 3:
        xs = [p[0] for p in coords]
        ys = [p[1] for p in coords]
        return (np.mean(xs), np.mean(ys))
    
    A = 0.0
    Cx = 0.0
    Cy = 0.0

    for i in range(n):
        x1,y1 = coords[i]
        x2,y2 = coords[(i+1)%n]

        cross = x1*y2 - x2*y1

        A  += cross
        Cx += (x1 + x2) * cross
        Cy += (y1 + y2) * cross

    if abs(A) < 1e-12:
        xs = [p[0] for p in coords]
        ys = [p[1] for p in coords]
        return (np.mean(xs), np.mean(ys))
    
    A *= 0.5
    return (Cx/(6*A), Cy/(6*A))

# read dataset
dfs = []
for path in CSV_PATH:
    df_i = pd.read_csv(path)
    df_i = df_i[df_i["CLASSIFICATION"].astype(str).str.strip().str.upper().eq("VEHICLE")]
    df_i = df_i[df_i["pos_x"].between(-180, 180) & df_i["pos_y"].between(-90, 90)]
    dfs.append(df_i)

df = pd.concat(dfs, ignore_index=True)

lons = df[LON_COL].to_numpy()
lats = df[LAT_COL].to_numpy()

lat_ref = float(pd.Series(lats).median())
lon_ref = float(pd.Series(lons).median())

xy0 = np.array([equirectangular_xy(lat, lon, lat_ref, lon_ref) for lat, lon in zip(lats, lons)])
xs, ys = xy0[:,0], xy0[:,1]

hull_xy = convex_hull(list(map(tuple, xy0)))
xmin, xmax = xs.min(), xs.max()
ymin, ymax = ys.min(), ys.max()

# get center point coor
center_x, center_y = polygon_centroid(hull_xy) if len(hull_xy)>=3 else (xs.mean(), ys.mean())
center_lat, center_lon = inverse_equirectangular_xy(center_x, center_y, lat_ref, lon_ref)

x_shift = xs - center_x
y_shift = ys - center_y

rect_xy = [(xmin-center_x, ymin-center_y),
           (xmax-center_x, ymin-center_y),
           (xmax-center_x, ymax-center_y),
           (xmin-center_x, ymax-center_y),
           (xmin-center_x, ymin-center_y)]
hull_xy_shift = [(x-center_x, y-center_y) for (x,y) in hull_xy]

# make diagram
fig, ax = plt.subplots(figsize=(7.6, 7.6))
ax.scatter(x_shift, y_shift, s=POINT_SIZE, alpha=0.6, label="Points")

rx = [p[0] for p in rect_xy]; ry = [p[1] for p in rect_xy]
ax.plot(rx, ry, lw=2, label="Bounding Box")

if len(hull_xy_shift) >= 3:
    hx = [p[0] for p in hull_xy_shift] + [hull_xy_shift[0][0]]
    hy = [p[1] for p in hull_xy_shift] + [hull_xy_shift[0][1]]
    ax.plot(hx, hy, lw=3, label="Convex Hull")

ax.scatter([0], [0], marker=CENTER_MARKER, s=CENTER_SIZE, color=CENTER_COLOR, label=f"Center: Hull Centroid")
center_text = f"Center (lat, lon)\n{center_lat:.7f}, {center_lon:.7f}"
ax.text(CENTER_TEXT_DX, CENTER_TEXT_DY, center_text,
        color=CENTER_COLOR, fontsize=9, ha="left", va="bottom",
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=CENTER_COLOR, lw=0.8, alpha=0.9))

ax.set_aspect("equal", adjustable="box")
ax.set_xlabel("X (meters, local)")
ax.set_ylabel("Y (meters, local)")
ax.set_title("Vehicle Coverage (meters)")
ax.legend(loc="best")
plt.tight_layout()
plt.savefig(OUT_IMG, dpi=250)
plt.close()

print(f"Center (lat, lon): {center_lat:.7f}, {center_lon:.7f}")
print(f"\nSaved figure: {OUT_IMG}")
