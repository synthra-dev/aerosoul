"""AeroSoul Konzeptmodell v0 – Headset, Boom, Sprühkopf, Basis. Maße in mm."""
import math, cadquery as cq

# Kopf-Referenz (nur für Proportionen): Halbachsen
HEAD = dict(ax=75, ay=95, az=112)
MOUTH = (0, -92, -58)
GAP = 30            # Abstand Sprühkopf-Front zu Lippen

def sweep_circle(pts, r):
    path = cq.Workplane("XY").spline([cq.Vector(*p) for p in pts], includeCurrent=False)
    p0, p1 = cq.Vector(*pts[0]), cq.Vector(*pts[1])
    plane = cq.Plane(origin=p0, normal=(p1 - p0).normalized())
    return cq.Workplane(plane).circle(r).sweep(path, isFrenet=True)

def headband():
    pts = [(-86*math.cos(t), 0, 6 + 116*math.sin(t)) for t in [i*math.pi/16 for i in range(17)]]
    path = cq.Workplane("XY").spline([cq.Vector(*p) for p in pts], includeCurrent=False)
    plane = cq.Plane(origin=pts[0], xDir=(1, 0, 0), normal=(0, 0, 1))
    band = cq.Workplane(plane).rect(5, 20).sweep(path, isFrenet=True)
    return band

def pad(side):
    x = side * 90
    return (cq.Workplane("YZ").workplane(offset=x - 5*side).ellipse(16, 24).extrude(10*side)
            .edges().fillet(3))

def spray_head():
    y = MOUTH[1] - GAP
    body = (cq.Workplane("XZ", origin=(0, y - 6, MOUTH[2])).circle(9.5).extrude(-12)
            .faces("<Y or >Y").edges().fillet(3))
    window = cq.Workplane("XZ", origin=(0, y + 6.1, MOUTH[2])).circle(4.5).extrude(-1.2)
    return body.cut(window)

def boom():
    y = MOUTH[1] - GAP
    pts = [(-92, -10, -4), (-86, -48, -24), (-62, y - 2, -48), (-24, y - 6, -57), (-9, y - 6, MOUTH[2])]
    return sweep_circle(pts, 2.6)

def cable():
    pts = [(-92, 6, -14), (-96, 20, -60), (-90, 40, -120), (-80, 60, -175)]
    return sweep_circle(pts, 1.6)

def base():
    w, d, h = 112, 82, 46
    shell = cq.Workplane("XY").box(w, d, h).edges("|Z").fillet(18).faces(">Z").edges().fillet(6)
    tank = (cq.Workplane("XY", origin=(18, 6, h/2)).circle(26).extrude(52)
            .faces(">Z").edges().fillet(8))
    lid = cq.Workplane("XY", origin=(18, 6, h/2 + 52)).circle(22).extrude(6).edges(">Z").fillet(2)
    knob = (cq.Workplane("XZ", origin=(-30, -d/2, 4)).circle(11).extrude(9)
            .faces("<Y").edges().fillet(2.5))
    jack = cq.Workplane("XZ", origin=(-30, -d/2 + 0.5, -14)).circle(3).extrude(2)
    return dict(shell=shell.cut(jack), tank=tank, lid=lid, knob=knob)

def parts():
    p = dict(band=headband(), pad_l=pad(-1), pad_r=pad(1), boom=boom(),
             head_spray=spray_head(), cable=cable())
    return p

if __name__ == "__main__":
    import sys
    for name, wp in {**parts(), **{"base_" + k: v for k, v in base().items()}}.items():
        cq.exporters.export(wp, f"out/{name}.stl", tolerance=0.2)
    print("ok")
