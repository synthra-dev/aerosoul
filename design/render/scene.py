"""AeroSoul Design-Konzept v1 – Blender/Cycles Produktrender. Einheiten: Meter."""
import bpy, math, sys
from mathutils import Vector

mm = 0.001
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def mat(name, base, rough=0.4, metal=0.0, trans=0.0, sheen=0.0, ior=1.45):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Transmission Weight"].default_value = trans
    b.inputs["IOR"].default_value = ior
    if sheen: b.inputs["Sheen Weight"].default_value = sheen
    return m

M = dict(
    fabric=mat("fabric", (0.10, 0.105, 0.11), 0.92, sheen=0.5),
    white=mat("white", (0.90, 0.90, 0.89), 0.32),
    graphite=mat("graphite", (0.05, 0.05, 0.055), 0.45),
    alu=mat("alu", (0.80, 0.80, 0.82), 0.28, metal=1.0),
    glass=mat("glass", (0.92, 0.96, 0.98), 0.18, trans=1.0, ior=1.45),
    floor=mat("floor", (0.62, 0.62, 0.64), 0.7),
    led=mat("led", (1, 0.85, 0.6), 0.5),
)
led = M["led"].node_tree.nodes["Principled BSDF"]
led.inputs["Emission Color"].default_value = (1, 0.8, 0.55, 1); led.inputs["Emission Strength"].default_value = 3

def finish(o, m, bevel=0.0, seg=4, sub=2, smooth=True):
    if bevel:
        b = o.modifiers.new("bevel", "BEVEL"); b.width = bevel; b.segments = seg; b.limit_method = "ANGLE"
    if sub:
        s = o.modifiers.new("sub", "SUBSURF"); s.levels = sub; s.render_levels = sub
    if smooth:
        bpy.context.view_layer.objects.active = o; o.select_set(True)
        bpy.ops.object.shade_smooth(); o.select_set(False)
    o.data.materials.append(m); return o

def ring(rx, ry, width, thick):
    bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=1, depth=width, end_fill_type="NOTHING")
    o = bpy.context.object; o.scale = (rx, ry, 1); bpy.ops.object.transform_apply(scale=True)
    so = o.modifiers.new("solid", "SOLIDIFY"); so.thickness = thick; so.offset = 1
    return finish(o, M["fabric"], bevel=1.5*mm, seg=3, sub=1)

def pebble(loc, size, m, rot=(0, 0, 0), bevel=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.scale = size; bpy.ops.object.transform_apply(scale=True)
    return finish(o, m, bevel=bevel or min(size)*0.48, seg=6, sub=2)

def disc(loc, r, depth, m, rot, bevel=0.8*mm):
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=r, depth=depth, location=loc, rotation=rot)
    return finish(bpy.context.object, m, bevel=bevel, seg=5, sub=1)

def tube(pts, w, h, m):
    cu = bpy.data.curves.new("c", "CURVE"); cu.dimensions = "3D"
    sp = cu.splines.new("BEZIER"); sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = Vector(p); bp.handle_left_type = bp.handle_right_type = "AUTO"
    cu.bevel_mode = "ROUND"; cu.bevel_depth = w/2; cu.bevel_resolution = 6; cu.use_fill_caps = True
    o = bpy.data.objects.new("tube", cu); bpy.context.collection.objects.link(o)
    o.scale = (1, 1, 1); o.data.materials.append(m)
    if h != w:  # flache Ellipse
        cu.taper_radius_mode = "OVERRIDE"
    return o

def headset(origin=Vector((0, 0, 0)), tilt=0.0):
    objs = []
    objs.append(ring(78*mm, 96*mm, 24*mm, 3.5*mm))
    # Schläfenmodul links, flach
    mx, my = -80.5*mm, -32*mm
    objs.append(pebble((mx - 2.5*mm, my, 0), (5.5*mm, 36*mm, 24*mm), M["white"], rot=(0, 0, math.radians(-14))))
    # Boom: dünn, weiß
    pts = [(mx - 3*mm, my - 14*mm, -6*mm), (mx + 2*mm, my - 46*mm, -38*mm),
           (-46*mm, -118*mm, -78*mm), (-11*mm, -127*mm, -88*mm)]
    objs.append(tube(pts, 3.6*mm, 3.6*mm, M["white"]))
    # Sprühkopf: flache Linse, zum Mund (+Y) gerichtet
    sh = disc((0, -128*mm, -88*mm), 8*mm, 4.5*mm, M["white"], rot=(math.radians(90), 0, 0), bevel=1.6*mm)
    win = disc((0, -125.6*mm, -88*mm), 3.6*mm, 0.6*mm, M["graphite"], rot=(math.radians(90), 0, 0), bevel=0.2*mm)
    objs += [sh, win]
    cab = bpy.data.objects.new("cable_anchor", None); sc.collection.objects.link(cab)
    cab.location = (mx - 2*mm, my + 13*mm, -10*mm); objs.append(cab)
    emp = bpy.data.objects.new("headset", None); sc.collection.objects.link(emp)
    for o in objs: o.parent = emp
    emp.rotation_euler = (0, 0, tilt); emp.location = origin
    bpy.context.view_layer.update()
    return emp

def base(loc):
    x, y, z = loc
    body = pebble((x, y, z + 17*mm), (104*mm, 104*mm, 34*mm), M["white"], bevel=16*mm)
    tank = pebble((x, y, z + 38*mm), (92*mm, 92*mm, 16*mm), M["glass"], bevel=14*mm)
    cap = pebble((x, y, z + 47.5*mm), (60*mm, 60*mm, 3.5*mm), M["white"], bevel=1.6*mm)
    knob = disc((x - 52.5*mm, y - 18*mm, z + 17*mm), 11*mm, 7*mm, M["alu"], rot=(0, math.radians(90), 0), bevel=1.2*mm)
    ledo = pebble((x, y - 52.4*mm, z + 9*mm), (14*mm, 0.6*mm, 1.6*mm), M["led"], bevel=0.25*mm)
    return [body, tank, cap, knob, ledo]

def studio():
    bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, -0.30))
    fl = bpy.context.object; fl.data.materials.append(M["floor"])
    # Hohlkehle
    bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 1.2, 2.7), rotation=(math.radians(90), 0, 0))
    bpy.context.object.data.materials.append(M["floor"])
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.9, 0.9, 0.92, 1)
    w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.12
    for name, loc, energy, size in [("key", (-0.7, -0.9, 1.1), 40, 1.4), ("fill", (0.9, -0.6, 0.4), 10, 1.2),
                                    ("rim", (0.3, 1.0, 0.8), 18, 1.0)]:
        ld = bpy.data.lights.new(name, "AREA"); ld.energy = energy; ld.size = size
        lo = bpy.data.objects.new(name, ld); sc.collection.objects.link(lo); lo.location = loc
        d = Vector((0, 0, -0.1)) - Vector(loc); lo.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()

def camera(loc, target, lens):
    cd = bpy.data.cameras.new("cam"); cd.lens = lens
    cd.dof.use_dof = True; cd.dof.aperture_fstop = 5.6
    co = bpy.data.objects.new("cam", cd); sc.collection.objects.link(co); co.location = loc
    d = Vector(target) - Vector(loc); co.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    cd.dof.focus_distance = d.length; sc.camera = co

shot = sys.argv[-1]
studio()
if shot == "hero":
    floor_z = -0.30
    emp = headset(Vector((-0.02, 0.0, floor_z + 0.095)), tilt=math.radians(-20))
    bx, by = 0.19, 0.03
    base((bx, by, floor_z))
    a = bpy.data.objects["cable_anchor"].matrix_world.translation
    r = 1.2*mm
    tube([tuple(a), (a.x - 0.012, a.y + 0.02, a.z - 0.05), (a.x + 0.02, a.y + 0.07, floor_z + r),
          (bx - 0.02, by + 0.12, floor_z + r), (bx + 0.03, by + 0.07, floor_z + r), (bx + 0.02, by + 0.05, floor_z + 0.02)],
         2.4*mm, 2.4*mm, M["white"])
    camera((-0.36, -0.56, -0.02), (0.07, 0.0, floor_z + 0.05), 52)
else:  # Nahaufnahme Modul + Boom + Sprühkopf
    headset(Vector((0, 0, 0)), tilt=0)
    camera((-0.36, -0.50, -0.04), (-0.045, -0.07, -0.05), 70)

sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = int(__import__("os").environ.get("SAMPLES","80"))
sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = (900, 550) if __import__("os").environ.get("PREVIEW") else (1800, 1100)
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
sc.render.image_settings.file_format = "JPEG"; sc.render.image_settings.quality = 92
sc.render.filepath = f"/home/claude/aerosoul/design/render/aerosoul_v1_{shot}.jpg"
bpy.ops.render.render(write_still=True)
print("rendered", shot)
