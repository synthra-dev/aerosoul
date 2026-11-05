import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import model

COL = dict(band=(0.20,0.24,0.28), pad=(0.82,0.84,0.86), boom=(0.20,0.24,0.28),
           spray=(0.93,0.94,0.95), cable=(0.30,0.33,0.36), shell=(0.93,0.94,0.95),
           tank=(0.62,0.78,0.86), lid=(0.20,0.24,0.28), knob=(0.85,0.55,0.30))
LIGHT = np.array([-0.4,-0.8,0.6]); LIGHT/=np.linalg.norm(LIGHT)

def mesh(wp, tol=0.3):
    v, t = wp.val().tessellate(tol)
    v = np.array([[p.x,p.y,p.z] for p in v]); t=np.array(t)
    return v[t]

def shade(tris, col, alpha=1.0):
    n = np.cross(tris[:,1]-tris[:,0], tris[:,2]-tris[:,0])
    n /= np.linalg.norm(n,axis=1,keepdims=True)+1e-9
    k = 0.35 + 0.65*np.clip(np.abs(n@LIGHT),0,1)
    c = np.clip(np.array(col)[None,:]*k[:,None],0,1)
    return np.c_[c, np.full(len(c),alpha)]

def head_tris():
    a,b,c = model.HEAD["ax"],model.HEAD["ay"],model.HEAD["az"]
    u=np.linspace(0,2*np.pi,48); w=np.linspace(-np.pi/2*0.85,np.pi/2,26)
    U,W=np.meshgrid(u,w); X=a*np.cos(W)*np.cos(U); Y=b*np.cos(W)*np.sin(U); Z=c*np.sin(W)
    tris=[]
    for i in range(len(w)-1):
        for j in range(len(u)-1):
            p=[(X[i,j],Y[i,j],Z[i,j]),(X[i+1,j],Y[i+1,j],Z[i+1,j]),(X[i+1,j+1],Y[i+1,j+1],Z[i+1,j+1]),(X[i,j+1],Y[i,j+1],Z[i,j+1])]
            tris += [[p[0],p[1],p[2]],[p[0],p[2],p[3]]]
    return np.array(tris)

def draw(ax, items, elev, azim, lim):
    for tris, fc in items:
        ax.add_collection3d(Poly3DCollection(tris, facecolors=fc, edgecolors=fc, linewidths=0.3, antialiased=False))
    ax.set_xlim(lim[0]); ax.set_ylim(lim[1]); ax.set_zlim(lim[2])
    ax.set_box_aspect([lim[i][1]-lim[i][0] for i in range(3)])
    ax.view_init(elev=elev, azim=azim); ax.set_axis_off()

p = model.parts()
hs = [(mesh(p["band"]),"band"),(mesh(p["pad_l"]),"pad"),(mesh(p["pad_r"]),"pad"),
      (mesh(p["boom"]),"boom"),(mesh(p["head_spray"]),"spray"),(mesh(p["cable"]),"cable")]
headset = [(t, shade(t, COL[c])) for t,c in hs]
head = head_tris(); head_item = (head, shade(head,(0.85,0.80,0.76),0.18))
lim = [(-130,130),(-160,110),(-180,140)]

fig = plt.figure(figsize=(15,5.6), dpi=130)
for i,(e,a,title) in enumerate([(12,-62,"Schräg vorne"),(5,-90,"Vorne"),(4,180,"Seite")]):
    ax = fig.add_subplot(1,3,i+1, projection="3d"); draw(ax,[head_item]+headset,e,a,lim)
    ax.set_title(title, fontsize=12)
fig.suptitle("AeroSoul Konzept v0 – Headset mit Boom (Kopf nur als Größenreferenz)", fontsize=13)
plt.subplots_adjust(wspace=0, left=0, right=1, top=0.9, bottom=0); fig.savefig("render_headset.png")

b = model.base()
bt = [(mesh(b[k]), shade(mesh(b[k]), COL[k], 0.75 if k=="tank" else 1)) for k in ("shell","tank","lid","knob")]
fig = plt.figure(figsize=(10,5.4), dpi=130)
for i,(e,a,title) in enumerate([(22,-55,"Basis schräg vorne"),(10,-90,"Basis vorne")]):
    ax = fig.add_subplot(1,2,i+1, projection="3d"); draw(ax, bt, e, a, [(-70,70),(-60,60),(-30,90)])
    ax.set_title(title, fontsize=12)
plt.subplots_adjust(wspace=0, left=0, right=1, top=0.92, bottom=0); fig.savefig("render_base.png")
print("done")
