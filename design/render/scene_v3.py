"""AeroSoul Design v3 – Lifestyle-Szene, weiß/silberblau. Einheiten: Meter.
Shots: SHOT=hero (Nachttisch, Headset + Basis) | SHOT=close (Sprühkopf-Innenseite). PREVIEW=1 für Vorschau."""
import bpy, math, os
from mathutils import Vector
mm = 0.001
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
SHOT = os.environ.get("SHOT", "hero"); PREV = os.environ.get("PREVIEW")

# ---------- Materialien ----------
def mat(name, base, rough=0.4, metal=0.0, coat=0.0, trans=0.0, sheen=0.0, ior=1.45):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal; b.inputs["Coat Weight"].default_value = coat
    b.inputs["Transmission Weight"].default_value = trans; b.inputs["IOR"].default_value = ior
    b.inputs["Sheen Weight"].default_value = sheen
    return m

WHITE = mat("white_gloss", (0.90, 0.90, 0.89), 0.22, coat=0.4)
SOFTW = mat("white_soft", (0.88, 0.88, 0.87), 0.6)
KNIT = mat("knit", (0.80, 0.81, 0.83), 0.9, sheen=0.6)
SILVERBLUE = mat("silverblue", (0.58, 0.68, 0.80), 0.26, metal=1.0)
STEEL = mat("steel", (0.75, 0.75, 0.76), 0.35, metal=1.0)
FROST = mat("frost", (0.94, 0.97, 1.0), 0.32, trans=1.0)
GLASS = mat("glass", (0.97, 0.99, 1.0), 0.02, trans=1.0, ior=1.5)
WATER = mat("water", (0.88, 0.95, 1.0), 0.01, trans=1.0, ior=1.33)
LED = mat("led", (1, 0.9, 0.75), 0.5)
lb = LED.node_tree.nodes["Principled BSDF"]
lb.inputs["Emission Color"].default_value = (1, 0.82, 0.6, 1); lb.inputs["Emission Strength"].default_value = 4
LINEN = mat("linen", (0.92, 0.91, 0.89), 0.85, sheen=0.8)
BOOK = mat("book", (0.30, 0.38, 0.42), 0.8, sheen=0.4)
PAGES = mat("pages", (0.93, 0.91, 0.86), 0.7)
WALL = mat("wall", (0.80, 0.77, 0.73), 0.9)

def grille_mat(base, hole, scale):
    m = bpy.data.materials.new("grille"); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = 0.45
    tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (scale, scale, scale)
    fr = nt.nodes.new("ShaderNodeVectorMath"); fr.operation = "FRACTION"
    sub = nt.nodes.new("ShaderNodeVectorMath"); sub.operation = "SUBTRACT"; sub.inputs[1].default_value = (0.5, 0.5, 0.5)
    ln = nt.nodes.new("ShaderNodeVectorMath"); ln.operation = "LENGTH"
    lt = nt.nodes.new("ShaderNodeMath"); lt.operation = "LESS_THAN"; lt.inputs[1].default_value = 0.42
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"
    mix.inputs[6].default_value = (*base, 1); mix.inputs[7].default_value = (*hole, 1)
    L = nt.links.new
    L(tc.outputs["Object"], mp.inputs["Vector"]); L(mp.outputs["Vector"], fr.inputs[0]); L(fr.outputs[0], sub.inputs[0])
    L(sub.outputs[0], ln.inputs[0]); L(ln.outputs["Value"], lt.inputs[0]); L(lt.outputs[0], mix.inputs[0])
    L(mix.outputs[2], b.inputs["Base Color"])
    return m
GRILLE = grille_mat((0.90, 0.90, 0.89), (0.18, 0.20, 0.24), 900)
MESH = grille_mat((0.70, 0.71, 0.73), (0.15, 0.15, 0.16), 2600)
MESH.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 1.0

def oak():
    m = bpy.data.materials.new("oak"); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = 0.55
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (6.0, 140.0, 6.0)
    n1 = nt.nodes.new("ShaderNodeTexNoise"); n1.inputs["Scale"].default_value = 3.0
    n1.inputs["Detail"].default_value = 10; n1.inputs["Distortion"].default_value = 1.2
    mp2 = nt.nodes.new("ShaderNodeMapping"); mp2.inputs["Scale"].default_value = (2.5, 9.0, 2.5)
    n2 = nt.nodes.new("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = 2.0
    mix = nt.nodes.new("ShaderNodeMath"); mix.operation = "MULTIPLY_ADD"; mix.inputs[1].default_value = 0.7
    mix2 = nt.nodes.new("ShaderNodeMath"); mix2.operation = "MULTIPLY_ADD"; mix2.inputs[1].default_value = 0.3
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].position = 0.42; cr.color_ramp.elements[1].position = 0.62
    cr.color_ramp.elements[0].color = (0.33, 0.20, 0.11, 1); cr.color_ramp.elements[1].color = (0.66, 0.50, 0.33, 1)
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.08
    L = nt.links.new
    L(tc.outputs["Object"], mp.inputs["Vector"]); L(mp.outputs["Vector"], n1.inputs["Vector"])
    L(tc.outputs["Object"], mp2.inputs["Vector"]); L(mp2.outputs["Vector"], n2.inputs["Vector"])
    L(n1.outputs["Fac"], mix.inputs[0]); L(n2.outputs["Fac"], mix2.inputs[0]); L(mix.outputs[0], mix2.inputs[2])
    L(mix2.outputs[0], cr.inputs["Fac"]); L(cr.outputs["Color"], b.inputs["Base Color"])
    L(n1.outputs["Fac"], bump.inputs["Height"]); L(bump.outputs["Normal"], b.inputs["Normal"])
    return m
OAK = oak()

# ---------- Geometrie-Helfer ----------
def smooth(o, m, bevel=0, sub=2, seg=5):
    if bevel:
        bv = o.modifiers.new("b", "BEVEL"); bv.width = bevel; bv.segments = seg; bv.limit_method = "ANGLE"
    if sub:
        s = o.modifiers.new("s", "SUBSURF"); s.levels = s.render_levels = sub
    bpy.context.view_layer.objects.active = o; o.select_set(True); bpy.ops.object.shade_smooth(); o.select_set(False)
    o.data.materials.append(m); return o

def profile(w, h, r):
    cu = bpy.data.curves.new("prof", "CURVE"); sp = cu.splines.new("POLY"); pts = []
    for cx, cy, a0 in [(w/2-r, h/2-r, 0), (-w/2+r, h/2-r, 90), (-w/2+r, -h/2+r, 180), (w/2-r, -h/2+r, 270)]:
        for k in range(7):
            a = math.radians(a0 + k*15); pts.append((cx + r*math.cos(a), cy + r*math.sin(a), 0))
    sp.points.add(len(pts) - 1)
    for p, c in zip(sp.points, pts): p.co = (*c, 1)
    sp.use_cyclic_u = True
    o = bpy.data.objects.new("prof", cu); sc.collection.objects.link(o); o.hide_render = True; return o

def sweep(pts, prof, m, round_r=None):
    cu = bpy.data.curves.new("c", "CURVE"); cu.dimensions = "3D"; cu.twist_mode = "Z_UP"
    sp = cu.splines.new("BEZIER"); sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = Vector(p); bp.handle_left_type = bp.handle_right_type = "AUTO"
    if round_r:
        cu.bevel_mode = "ROUND"; cu.bevel_depth = round_r; cu.bevel_resolution = 6
    else:
        cu.bevel_mode = "OBJECT"; cu.bevel_object = prof
    cu.use_fill_caps = True; cu.resolution_u = 24
    o = bpy.data.objects.new("sw", cu); sc.collection.objects.link(o); o.data.materials.append(m); return o

def ell(a0, a1, rx, ry, z, n):
    return [(rx*math.sin(math.radians(a)), -ry*math.cos(math.radians(a)), z) for a in [a0 + (a1-a0)*i/(n-1) for i in range(n)]]

def blob(loc, size, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, location=loc, rotation=rot)
    o = bpy.context.object; o.scale = size; bpy.ops.object.transform_apply(scale=True); return smooth(o, m, sub=1)

def rbox(loc, size, m, bevel):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object
    o.scale = size; bpy.ops.object.transform_apply(scale=True); return smooth(o, m, bevel=bevel, seg=6, sub=2)

def cyl(loc, r, depth, m, rot=(0, 0, 0), bevel=0.0, sub=1, verts=128, flat=False):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    o = smooth(bpy.context.object, m, bevel=bevel, sub=sub)
    if flat:
        bpy.context.view_layer.objects.active = o; o.select_set(True); bpy.ops.object.shade_flat(); o.select_set(False)
    return o

# ---------- Headset (lokal: Bandmitte = Ursprung, Gesicht schaut nach -Y, Träger-links = +X) ----------
RX, RY = 79*mm, 97*mm
def headset():
    objs = []
    objs.append(sweep(ell(-105, 105, RX, RY, 0, 15), profile(4*mm, 22*mm, 1.6*mm), WHITE))          # Front-Spange
    objs.append(sweep(ell(100, 260, RX - 1*mm, RY - 1*mm, -2*mm, 13), profile(2.8*mm, 15*mm, 1.3*mm), KNIT))  # Riemen hinten
    objs.append(sweep(ell(-100, 100, RX + 1.9*mm, RY + 1.9*mm, 10.6*mm, 15), profile(0.9*mm, 0.9*mm, 0.44*mm), SILVERBLUE))  # Kantenlinie
    objs.append(blob((RX - 1*mm, -34*mm, -7*mm), (7.5*mm, 15*mm, 22*mm), WHITE, rot=(0, 0, math.radians(12))))   # Schläfenmodul links
    objs.append(blob((-RX + 1*mm, -34*mm, -7*mm), (6.5*mm, 14*mm, 20*mm), SOFTW, rot=(0, 0, math.radians(-12)))) # Pad rechts
    bp = [(RX + 1*mm, -36*mm, -24*mm), (RX + 1*mm, -40*mm, -64*mm), (RX - 4*mm, -60*mm, -97*mm),
          (46*mm, -113*mm, -104*mm), (9*mm, -127*mm, -100*mm)]
    objs.append(sweep(bp, profile(4*mm, 7.5*mm, 1.9*mm), WHITE))                                    # Boom
    objs.append(cyl((RX + 1*mm, -37.6*mm, -44*mm), 4.6*mm, 2.6*mm, SILVERBLUE, rot=(math.radians(-8), math.radians(-2), 0), bevel=0.5*mm))  # Gelenkring
    hx, hy, hz = 0, -128*mm, -100*mm
    objs.append(rbox((hx, hy, hz), (23*mm, 7.5*mm, 17*mm), SILVERBLUE, 3.2*mm))                      # Rahmen
    objs.append(rbox((hx, hy - 3.0*mm, hz), (19.6*mm, 2.0*mm, 13.6*mm), GRILLE, 0.8*mm))             # Gitter außen (Design)
    objs.append(rbox((hx, hy + 3.0*mm, hz), (20.4*mm, 2.0*mm, 14.4*mm), WHITE, 0.8*mm))              # Innenseite
    objs.append(cyl((hx, hy + 4.05*mm, hz), 5.5*mm, 0.5*mm, MESH, rot=(math.radians(90), 0, 0), sub=0, flat=True))   # Mesh-Auslass
    objs.append(cyl((hx, hy + 4.0*mm, hz), 6.6*mm, 0.5*mm, SILVERBLUE, rot=(math.radians(90), 0, 0), sub=0, flat=True))  # Ring um Auslass
    anchor = bpy.data.objects.new("cable_anchor", None); sc.collection.objects.link(anchor)
    anchor.location = (RX + 3*mm, -26*mm, -20*mm); objs.append(anchor)
    grp = bpy.data.objects.new("headset", None); sc.collection.objects.link(grp)
    for o in objs: o.parent = grp
    return grp

# ---------- Basis (zylindrisch, weiß, Tankfenster, silberblauer Deckel + Krone) ----------
def base(x, y):
    R = 52*mm
    cyl((x, y, 23*mm), R, 46*mm, SOFTW, bevel=6*mm, sub=2)
    cyl((x, y, 60*mm), R - 0.6*mm, 28*mm, FROST, sub=0)
    cyl((x, y, 55*mm), R - 4*mm, 16*mm, WATER, sub=0)
    cyl((x, y, 80*mm), R, 14*mm, SOFTW, bevel=5*mm, sub=2)
    cyl((x, y, 87.6*mm), 40*mm, 2.4*mm, SILVERBLUE, bevel=1.0*mm)
    a = math.radians(-70)
    kx, ky = x + (R + 3*mm)*math.cos(a), y + (R + 3*mm)*math.sin(a)
    cyl((kx, ky, 24*mm), 9*mm, 7*mm, SILVERBLUE, rot=(0, math.radians(90), a), bevel=1.0*mm)
    a2 = math.radians(-110)
    blob((x + R*math.cos(a2), y + R*math.sin(a2), 14*mm), (2.2*mm, 2.2*mm, 2.2*mm), LED)
    return Vector((x, y + R, 12*mm))

# ---------- Szene ----------
floor_top = 0.0
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.0, 0.0, -0.015)); tb = bpy.context.object
tb.scale = (0.70, 0.55, 0.03); bpy.ops.object.transform_apply(scale=True); smooth(tb, OAK, bevel=3*mm, sub=0)
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0.42, 1.0), rotation=(math.radians(90), 0, 0))
bpy.context.object.data.materials.append(WALL)
# Bettdecke links hinten (unscharf)
bpy.ops.mesh.primitive_grid_add(x_subdivisions=220, y_subdivisions=220, size=1, location=(-0.80, 0.20, 0.06))
bd = bpy.context.object; bd.scale = (0.8, 1.2, 1); bpy.ops.object.transform_apply(scale=True)
tex = bpy.data.textures.new("folds", "CLOUDS"); tex.noise_scale = 0.12; tex.noise_depth = 2
dm = bd.modifiers.new("d", "DISPLACE"); dm.texture = tex; dm.strength = 0.07; dm.texture_coords = "GLOBAL"
smooth(bd, LINEN, sub=1)

if SHOT == "hero":
    # Headset liegt auf einem flachen Eichen-Ständer (Requisite)
    sx, sy = -0.07, 0.02
    cyl((sx, sy, 5*mm), 52*mm, 10*mm, OAK, bevel=3*mm, sub=1)
    cyl((sx, sy, 82*mm), 5*mm, 150*mm, STEEL, sub=0)
    bz = 172*mm
    bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=1, depth=36*mm, location=(sx, sy, bz))
    pk = bpy.context.object; pk.scale = (62*mm, 86*mm, 0.7); bpy.ops.object.transform_apply(scale=True)
    smooth(pk, OAK, bevel=8*mm, sub=1)
    hs = headset(); hs.location = (sx, sy, bz); hs.rotation_euler = (0, 0, math.radians(-12))
    bpy.context.view_layer.update()
    bx, by = 0.16, 0.10
    port = base(bx, by)
    a = bpy.data.objects["cable_anchor"].matrix_world.translation.copy()
    r = 1.2*mm
    sweep([tuple(a), (a.x + 0.006, a.y + 0.012, a.z - 0.05), (a.x + 0.02, a.y + 0.05, r + 0.01),
           (a.x + 0.06, a.y + 0.10, r), (port.x - 0.03, port.y + 0.07, r), (port.x, port.y + 0.004, port.z)],
          None, SOFTW, round_r=1.2*mm)
    # Glas Wasser + Buch
    gx, gy = 0.29, 0.20
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=34*mm, depth=95*mm, location=(gx, gy, 47.5*mm))
    g = bpy.context.object; so = g.modifiers.new("so", "SOLIDIFY"); so.thickness = 2.2*mm
    bpy.context.view_layer.objects.active = g; bpy.ops.object.mode_set(mode="EDIT")
    import bmesh
    bm = bmesh.from_edit_mesh(g.data)
    for f in bm.faces:
        if f.normal.z > 0.9: bm.faces.remove(f)
    bmesh.update_edit_mesh(g.data); bpy.ops.object.mode_set(mode="OBJECT"); smooth(g, GLASS, bevel=0.6*mm, sub=0)
    cyl((gx, gy, 32*mm), 31.5*mm, 60*mm, WATER, sub=0)
    for z, size, m_, bv in [(11*mm, (146*mm, 206*mm, 18*mm), PAGES, 0.6*mm), (21*mm, (152*mm, 212*mm, 2.2*mm), BOOK, 0.8*mm), (1.1*mm, (152*mm, 212*mm, 2.2*mm), BOOK, 0.8*mm)]:
        rbox((-0.25, 0.21, z), size, m_, bv).rotation_euler = (0, 0, math.radians(-16))
    cam_loc, cam_tgt, lens, fstop = (0.02, -0.60, 0.27), (0.04, 0.03, 0.085), 50, 3.5
else:
    sx, sy = 0.0, 0.0
    tb.hide_render = True; bd.hide_render = True
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=260, y_subdivisions=260, size=1, location=(0.0, -0.25, 0.0))
    bl = bpy.context.object; bl.scale = (1.0, 1.1, 1); bpy.ops.object.transform_apply(scale=True)
    tex2 = bpy.data.textures.new("folds2", "CLOUDS"); tex2.noise_scale = 0.07; tex2.noise_depth = 2
    dm2 = bl.modifiers.new("d", "DISPLACE"); dm2.texture = tex2; dm2.strength = 0.035; dm2.texture_coords = "GLOBAL"
    smooth(bl, mat("linen_blue", (0.50, 0.56, 0.64), 0.85, sheen=0.9), sub=1)
    hs = headset(); hs.location = (0, 0, 0.13); hs.rotation_euler = (0, 0, 0)
    bpy.context.view_layer.update()
    # Kamera ungefähr dort, wo das Gesicht ist: Blick auf Innenseite des Sprühkopfs
    cam_loc, cam_tgt, lens, fstop = (-0.075, 0.015, 0.125), (0.004, -0.122, 0.034), 70, 8.0
    kl = bpy.data.lights.new("key_close", "AREA"); kl.energy = 2; kl.size = 0.25; kl.color = (1.0, 0.95, 0.9)
    ko = bpy.data.objects.new("key_close", kl); sc.collection.objects.link(ko); ko.location = (-0.22, 0.05, 0.25)
    ko.rotation_euler = (Vector((0.0, -0.12, 0.03)) - ko.location).to_track_quat("-Z", "Y").to_euler()

# ---------- Licht: warmes Morgenlicht von links, kühles Umgebungslicht ----------
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.78, 0.84, 0.92, 1)
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.35
sun = bpy.data.lights.new("sun", "SUN"); sun.energy = 4.2; sun.angle = math.radians(1.2); sun.color = (1.0, 0.88, 0.74)
so_ = bpy.data.objects.new("sun", sun); sc.collection.objects.link(so_)
so_.rotation_euler = (math.radians(55), 0, math.radians(-60))
bpy.context.view_layer.update()
sd = so_.matrix_world.to_3x3() @ Vector((0, 0, -1))
up = Vector((0, 0, 1)); side = sd.cross(up).normalized(); vert = side.cross(sd).normalized()
ctr = Vector((0.0, 0.15, 0.1)) - sd * 0.5
for i in range(-14, 15):
    p = ctr + vert * (i * 0.06)
    bpy.ops.mesh.primitive_cube_add(size=1, location=p)
    sl = bpy.context.object; sl.scale = (1, 1, 1)
    sl.rotation_euler = sd.to_track_quat("Z", "Y").to_euler()
    sl.dimensions = (1.8, 0.03, 0.004)
    sl.visible_camera = False; sl.visible_glossy = False; sl.visible_transmission = False
ld = bpy.data.lights.new("fill", "AREA"); ld.energy = 25; ld.size = 1.2; ld.color = (0.9, 0.94, 1.0)
lo = bpy.data.objects.new("fill", ld); sc.collection.objects.link(lo); lo.location = (0.6, -0.6, 0.6)
lo.rotation_euler = (Vector((0, 0, 0.08)) - lo.location).to_track_quat("-Z", "Y").to_euler()

cd = bpy.data.cameras.new("cam"); cd.lens = lens; cd.dof.use_dof = True; cd.dof.aperture_fstop = fstop
co = bpy.data.objects.new("cam", cd); sc.collection.objects.link(co); co.location = cam_loc
d = Vector(cam_tgt) - Vector(cam_loc); co.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
cd.dof.focus_distance = d.length; sc.camera = co

sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"
sc.cycles.samples = 16 if PREV else int(os.environ.get("SAMPLES", "64")); sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = (640, 400) if PREV else (1800, 1125)
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"; sc.view_settings.exposure = -0.55 if SHOT == 'hero' else -0.9
sc.render.image_settings.file_format = "JPEG"; sc.render.image_settings.quality = 92
sc.render.filepath = f"/home/claude/aerosoul/design/render/aerosoul_v3_{SHOT}.jpg"
bpy.ops.render.render(write_still=True); print("rendered", SHOT)
