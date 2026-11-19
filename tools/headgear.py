# Mũ trụ, mũ rồng, vương miện, nón lá – đơn vị theo bán kính đầu (=1), hệ toạ độ nhóm đầu HG của game
import sys,os,math;sys.path.insert(0,os.path.dirname(__file__))
from blib import *
OUT=sys.argv[sys.argv.index('--')+1]
clear()
def dome(n,m='metal',top=1.3):
 prof=[]
 for i in range(17):
  t=i/16;a=t*math.pi/2;r=1.14*math.cos(a)**0.9;y=0.08+math.sin(a)*(top-0.08)*(0.85+0.15*t)
  prof.append((max(r,0.001) if i<16 else 0,y))
 lathe(n,prof,m,seg=40)
def helm():
 n='hg_helm';dome(n,'metal',1.32)
 for i in range(10):
  a=i/10*math.pi*2;pts=[]
  for k in range(7):t=k/6;aa=t*math.pi/2*0.96;r=1.16*math.cos(aa)**0.9;pts.append((math.cos(a)*r,0.08+math.sin(aa)*1.2,math.sin(a)*r))
  limb(n,pts,lambda t:0.035*(1-t*0.6),m='gold',n=10,sub=1)
 torus(n,(0,0.1,-0.02),1.16,0.07,'gold',rot=(0,0,0),seg=48)
 # vành che trán cong
 import bmesh
 bm=bmesh.new();P=lambda x,y,z:bm.verts.new((C@Vector((x,y,z,1))).to_3d());rows=[]
 for k,(r,y) in enumerate(((1.16,0.08),(1.34,-0.02),(1.42,-0.06))):
  rows.append([P(math.sin(a)*r,y,math.cos(a)*r) for a in [-0.95+i/16*1.9 for i in range(17)]])
 for k in range(2):
  for i in range(16):bm.faces.new((rows[k][i],rows[k][i+1],rows[k+1][i+1],rows[k+1][i]))
 o=obj_from_bm(bm,n,'metal',True);o.modifiers.new('s','SOLIDIFY').thickness=0.04
 # chắn tai + che gáy (vảy)
 for s in(-1,1):
  for j in range(3):box(n,(s*1.12,-0.15-j*0.2,-0.12),(0.08,0.24,0.62-j*0.08),'metal',rot=(0,0,s*0.12),bev=0.02);box(n,(s*1.16,-0.15-j*0.2,-0.12),(0.02,0.04,0.6-j*0.08),'gold')
 for j in range(3):
  for i in range(7):
   a=math.pi*(1.16+i*0.68/6);r=1.14+j*0.03
   box(n,(math.cos(a)*r,-0.08-j*0.17,math.sin(a)*r),(0.36,0.2,0.05),'metal',rot=(0,-a+math.pi/2,0),bev=0.015)
 lathe(n,[(0,1.6),(0.05,1.55),(0.1,1.42),(0.07,1.32),(0,1.3)],'gold',seg=16)
 ell(n,(0,0.4,1.12),(0.14,0.18,0.06),m='gold',seg=16);ell(n,(0,0.4,1.17),(0.07,0.09,0.04),m='gem',seg=12)
def dragonhelm():
 n='hg_dragon';dome(n,'jade',1.3)
 torus(n,(0,0.1,-0.02),1.16,0.08,'gold',seg=48)
 for s in(-1,1):
  limb(n,[(s*0.55,0.85,-0.05),(s*0.9,1.25,-0.35),(s*1.0,1.6,-0.85),(s*0.9,1.85,-1.3)],lambda t:0.15*(1-t*0.85),m='ivory',n=16)
  for k in range(4):cone(n,(s*0.3,1.0-k*0.18,-0.75-k*0.1),(s*0.4,0.4,-1),0.07,0.3,'gold',seg=6)
 # đầu rồng nhỏ trên trán
 ell(n,(0,0.55,1.1),(0.2,0.16,0.22),m='gold',seg=16);ell(n,(0,0.5,1.32),(0.12,0.09,0.14),m='gold',seg=14)
 for s in(-1,1):ell(n,(s*0.1,0.62,1.24),(0.035,0.025,0.02),m='ec',seg=8);limb(n,[(s*0.08,0.68,1.15),(s*0.18,0.85,1.0),(s*0.2,0.95,0.85)],lambda t:0.03*(1-t*0.7),m='gold',n=6)
 for k in range(6):cone(n,(0,1.25-k*0.12,-0.2-k*0.17),(0,0.6,-1),0.06,0.28,'gold',seg=6)
def crown():
 # đặt tại toạ độ nhóm CG (0,0.78,-0.1), nghiêng -0.2 – dựng sẵn ở toạ độ HG
 n='hg_crown';import bmesh
 lathe(n,[(0.78,-0.18),(0.8,-0.14),(0.76,0.14),(0.74,0.18)],'gold',seg=48,c=(0,0.78,-0.1),smooth=True)
 o=PARTS[n][-1];o.modifiers.new('s','SOLIDIFY').thickness=0.04
 for y in(-0.17,0.17):torus(n,(0,0.78+y,-0.1),0.79 if y<0 else 0.75,0.035,'gold',seg=48)
 for i in range(9):
  a=i/9*math.pi*2+math.pi/2;cx,cz=math.cos(a)*0.74,math.sin(a)*0.74-0.1
  bm=bmesh.new();P=lambda x,y,z:bm.verts.new((C@Vector((x,y,z,1))).to_3d())
  t=Vector((-math.sin(a),0,math.cos(a)));nrm=Vector((math.cos(a),0,math.sin(a)))
  pts=[(-0.11,0.95),(-0.08,1.08),(-0.04,1.05),(0,1.24),(0.04,1.05),(0.08,1.08),(0.11,0.95)]
  f=[P(cx+t.x*u,y,cz+t.z*u) for u,y in pts];b2=[P(cx+t.x*u-nrm.x*0.03,y,cz+t.z*u-nrm.z*0.03) for u,y in pts]
  bm.faces.new(f);bm.faces.new(list(reversed(b2)))
  for k in range(len(pts)):j=(k+1)%len(pts);bm.faces.new((f[k],b2[k],b2[j],f[j]))
  bmesh.ops.recalc_face_normals(bm,faces=bm.faces);obj_from_bm(bm,n,'gold',False)
  ell(n,(math.cos(a)*0.8,0.8,math.sin(a)*0.8-0.1),(0.05,0.06,0.03),m='ruby',seg=10)
 ell(n,(0,0.84,0.72),(0.12,0.12,0.06),m='ec',seg=16)
 for s in(-1,1):limb(n,[(s*0.1,1.0,0.68),(s*0.35,1.15,0.6),(s*0.5,1.05,0.5)],lambda t:0.025,m='gold',n=8,sub=1)
def hat():
 n='hg_hat';prof=[(0,1.48)]
 for i in range(1,13):t=i/12;prof.append((2.1*t,1.48-0.85*t*(1.08-0.08*t)))
 prof.append((2.12,0.62));lathe(n,prof,'straw',seg=56)
 o=PARTS[n][-1];o.modifiers.new('s','SOLIDIFY').thickness=0.03
 for i in range(1,7):r=2.1*i/7;y=1.48-0.85*(i/7)*(1.08-0.08*i/7);torus(n,(0,y+0.012,-0.0),r,0.012,'straw2',seg=56,mseg=4)
 for i in range(24):
  a=i/24*math.pi*2;limb(n,[(math.cos(a)*0.05,1.46,math.sin(a)*0.05),(math.cos(a)*2.08,0.64,math.sin(a)*2.08)],lambda t:0.008,m='straw2',n=2,sub=1)
 torus(n,(0,0.66,0),2.1,0.025,'straw2',seg=56)
for f in(helm,dragonhelm,crown,hat):f()
objs=finish_nodes({},{})
for k,o in objs.items():
 t=tris([o])
 if t>4000:
  bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;d=o.modifiers.new('d','DECIMATE');d.ratio=4000/t;bpy.ops.object.modifier_apply(modifier='d')
print('TRIS',{k:tris([o]) for k,o in objs.items()})
COL={'metal':((0.6,0.62,0.66),1,0.3),'gold':((1,0.75,0.22),1,0.25),'gem':((0.1,0.8,0.5),0,0.1),'ec':((0.3,0.8,1),0,0.2),'jade':((0.2,0.5,0.35),0.3,0.3),'ivory':((0.96,0.94,0.88),0,0.4),'ruby':((0.8,0.05,0.08),0,0.1),'straw':((0.9,0.8,0.55),0,0.8),'straw2':((0.7,0.58,0.36),0,0.8)}
for nn,m in MATS.items():
 if nn in COL:c,mt,r=COL[nn];bs=m.node_tree.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=(*c,1);bs.inputs['Metallic'].default_value=mt;bs.inputs['Roughness'].default_value=r;m.diffuse_color=(*c,1)
export(os.path.join(OUT,'headgear.glb'))
