"""AeroSoul Design v2 – an Owner-Design angelehnt (schwarz/roségold), ohne Nasenauslässe. Einheiten: Meter."""
import bpy, math, os
from mathutils import Vector
mm = 0.001
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def mat(name, base, rough=0.4, metal=0.0, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal; b.inputs["Coat Weight"].default_value = coat
    return m

BLACK = mat("black", (0.018, 0.018, 0.02), 0.38, coat=0.3)
SOFT = mat("soft", (0.025, 0.025, 0.027), 0.7)
ROSE = mat("rose", (0.86, 0.70, 0.58), 0.22, metal=1.0)
WHITE = mat("white", (0.95, 0.95, 0.95), 0.8)

def grille_mat():
    m = bpy.data.materials.new("grille"); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = 0.5
    tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (950, 950, 950)
    fr = nt.nodes.new("ShaderNodeVectorMath"); fr.operation = "FRACTION"
    sub = nt.nodes.new("ShaderNodeVectorMath"); sub.operation = "SUBTRACT"; sub.inputs[1].default_value = (0.5, 0.5, 0.5)
    ln = nt.nodes.new("ShaderNodeVectorMath"); ln.operation = "LENGTH"
    lt = nt.nodes.new("ShaderNodeMath"); lt.operation = "LESS_THAN"; lt.inputs[1].default_value = 0.42
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"
    mix.inputs[6].default_value = (0.055, 0.055, 0.06, 1); mix.inputs[7].default_value = (0.0, 0.0, 0.0, 1)
    L = nt.links.new
    L(tc.outputs["Object"], mp.inputs["Vector"]); L(mp.outputs["Vector"], fr.inputs[0]); L(fr.outputs[0], sub.inputs[0])
    L(sub.outputs[0], ln.inputs[0]); L(ln.outputs["Value"], lt.inputs[0]); L(lt.outputs[0], mix.inputs[0])
    L(mix.outputs[2], b.inputs["Base Color"])
    return m
GRILLE = grille_mat()

def smooth(o, m, bevel=0, sub=2, seg=5):
    if bevel:
        bv = o.modifiers.new("b", "BEVEL"); bv.width = bevel; bv.segments = seg; bv.limit_method = "ANGLE"
    if sub:
        s = o.modifiers.new("s", "SUBSURF"); s.levels = s.render_levels = sub
    bpy.context.view_layer.objects.active = o; o.select_set(True); bpy.ops.object.shade_smooth(); o.select_set(False)
    o.data.materials.append(m); return o

def profile(w, h, r):
    cu = bpy.data.curves.new("prof", "CURVE"); sp = cu.splines.new("POLY")
    pts = []
    for cx, cy, a0 in [(w/2-r, h/2-r, 0), (-w/2+r, h/2-r, 90), (-w/2+r, -h/2+r, 180), (w/2-r, -h/2+r, 270)]:
        for k in range(7):
            a = math.radians(a0 + k*15); pts.append((cx + r*math.cos(a), cy + r*math.sin(a), 0))
    sp.points.add(len(pts) - 1)
    for p, c in zip(sp.points, pts): p.co = (*c, 1)
    sp.use_cyclic_u = True
    o = bpy.data.objects.new("prof", cu); sc.collection.objects.link(o); o.hide_render = True
    return o

def sweep(pts, prof, m, cyclic=False, tilt=0.0):
    cu = bpy.data.curves.new("c", "CURVE"); cu.dimensions = "3D"; cu.twist_mode = "Z_UP"
    sp = cu.splines.new("BEZIER"); sp.bezier_points.add(len(pts) - 1); sp.use_cyclic_u = cyclic
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = Vector(p); bp.handle_left_type = bp.handle_right_type = "AUTO"; bp.tilt = tilt
    cu.bevel_mode = "OBJECT"; cu.bevel_object = prof; cu.use_fill_caps = True; cu.resolution_u = 24
    o = bpy.data.objects.new("sw", cu); sc.collection.objects.link(o); o.data.materials.append(m); return o

def ell(a0, a1, rx, ry, z, n):
    return [(rx*math.sin(math.radians(a)), -ry*math.cos(math.radians(a)), z) for a in [a0 + (a1-a0)*i/(n-1) for i in range(n)]]

def blob(loc, size, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, location=loc, rotation=rot)
    o = bpy.context.object; o.scale = size; bpy.ops.object.transform_apply(scale=True)
    return smooth(o, m, sub=1)

def rbox(loc, size, m, bevel):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object
    o.scale = size; bpy.ops.object.transform_apply(scale=True); return smooth(o, m, bevel=bevel, seg=6, sub=2)

RX, RY = 79*mm, 97*mm
# Band: steife Front-Spange (schwarz glänzend) + dünnerer Riemen hinten (Stoff)
front = sweep(ell(-105, 105, RX, RY, 0, 15), profile(4*mm, 22*mm, 1.6*mm), BLACK)
rear = sweep(ell(100, 260, RX - 1*mm, RY - 1*mm, -2*mm, 13), profile(2.6*mm, 14*mm, 1.2*mm), SOFT)
edge = sweep(ell(-100, 100, RX + 1.9*mm, RY + 1.9*mm, 10.6*mm, 15), profile(0.9*mm, 0.9*mm, 0.44*mm), ROSE)
# Schläfenpads innen (beide Seiten) + Modul-Pod außen links
blob((-RX + 1*mm, -34*mm, -7*mm), (7.5*mm, 15*mm, 22*mm), BLACK, rot=(0, 0, math.radians(-12)))  # links: Schläfenmodul
blob((RX - 1*mm, -34*mm, -7*mm), (6.5*mm, 14*mm, 20*mm), BLACK, rot=(0, 0, math.radians(12)))
# Boom: flach, schwarz, Gelenkring roségold, Knick nach vorne
bp = [(-RX - 1*mm, -36*mm, -24*mm), (-RX - 1*mm, -40*mm, -64*mm), (-RX + 4*mm, -60*mm, -97*mm),
      (-46*mm, -113*mm, -104*mm), (-9*mm, -127*mm, -100*mm)]
sweep(bp, profile(4*mm, 7.5*mm, 1.9*mm), BLACK)
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=4.6*mm, depth=2.6*mm, location=(-RX - 1*mm, -37.6*mm, -44*mm),
                                    rotation=(math.radians(-8), math.radians(2), 0))
smooth(bpy.context.object, ROSE, bevel=0.5*mm, sub=1)
# Sprühkopf: flaches Rechteck, roségoldener Rahmen, gelochtes Gitter zum Mund
head = (0, -128*mm, -100*mm)
rbox(head, (23*mm, 7.5*mm, 17*mm), ROSE, 3.2*mm)
rbox((head[0], head[1] - 0.9*mm, head[2]), (20.4*mm, 6.6*mm, 14.4*mm), BLACK, 2.6*mm)
g = rbox((head[0], head[1] + 3.0*mm, head[2]), (19.6*mm, 2.0*mm, 13.6*mm), GRILLE, 0.8*mm)

# Spiegeln: Modul auf die linke Seite des Trägers (+X, Träger blickt nach -Y)
grp = bpy.data.objects.new("headset", None); sc.collection.objects.link(grp)
for o in list(sc.objects):
    if o is not grp and o.parent is None: o.parent = grp
grp.scale = (-1, 1, 1)
# Studio
bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, -0.125)); bpy.context.object.is_shadow_catcher = True
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (1, 1, 1, 1)
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.12
for name, loc, e, s in [("key", (-0.6, -0.5, 0.8), 30, 1.0), ("fill", (0.6, -0.6, 0.3), 8, 1.2), ("top", (0.0, 0.3, 0.9), 14, 1.5)]:
    ld = bpy.data.lights.new(name, "AREA"); ld.energy = e; ld.size = s
    lo = bpy.data.objects.new(name, ld); sc.collection.objects.link(lo); lo.location = loc
    lo.rotation_euler = (Vector((0, -0.04, -0.05)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
cd = bpy.data.cameras.new("cam"); cd.lens = 70
co = bpy.data.objects.new("cam", cd); sc.collection.objects.link(co)
shot = os.environ.get("SHOT", "hero")
if shot == "close":
    co.location = (-0.045, 0.02, -0.035); tgt = Vector((0.0, -0.128, -0.1)); cd.lens = 90
else:
    co.location = (-0.20, 0.42, 0.10); tgt = Vector((0.01, -0.055, -0.048))
co.rotation_euler = (tgt - co.location).to_track_quat("-Z", "Y").to_euler(); sc.camera = co

prev = os.environ.get("PREVIEW")
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 12 if prev else 64; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = (700, 700) if prev else (1600, 1600)
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"; sc.view_settings.exposure = -0.3
sc.render.film_transparent = True; sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGBA"
sc.render.filepath = "/home/claude/aerosoul/design/render/_v2_raw.png"
bpy.ops.render.render(write_still=True)
from PIL import Image
im = Image.open("/home/claude/aerosoul/design/render/_v2_raw.png").convert("RGBA")
bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
bg.convert("RGB").save(f"/home/claude/aerosoul/design/render/aerosoul_v2_{os.environ.get('SHOT','hero')}.jpg", quality=92); print("rendered")
