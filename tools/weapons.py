# 23 loại vũ khí – mỗi loại là một node gốc (tên = mã vũ khí) trong một file glTF.
# Hệ toạ độ khung vũ khí của game: chuôi quanh y=0..0.18, mũi/lưỡi hướng -y, đơn vị khung (game nhân 0.6*S).
import sys,os,math;sys.path.insert(0,os.path.dirname(__file__))
from blib import *
OUT=sys.argv[sys.argv.index('--')+1]
clear()
def grip(n,y0=0.0,L=0.18,r=0.024,wrap=True):
 prof=[(0,y0+L+0.012),(r*0.9,y0+L+0.01),(r,y0+L)]
 k=10
 for i in range(k+1):
  yy=y0+L-i*L/k;prof.append((r*(1.08 if (i%2 and wrap) else 0.96),yy))
 prof.append((0,y0-0.004));lathe(n,prof,'cloth' if wrap else 'wood',seg=14)
def pommel(n,y,r=0.034,m='gold'):lathe(n,[(0,y+r*1.6),(r*0.5,y+r*1.4),(r,y+r*0.6),(r*0.9,y),(r*0.5,y-r*0.2),(0,y-r*0.25)],m,seg=18)
def shaft(n,y1,y2,r=0.024,m='wood',rings=()):
 lathe(n,[(0,y1+0.002),(r,y1),(r,y2),(0,y2-0.002)],m,seg=14)
 for y in rings:lathe(n,[(0,y+0.02),(r*1.25,y+0.018),(r*1.35,y),(r*1.25,y-0.018),(0,y-0.02)],'gold',seg=14)
def tassel(n,y,col='red'):
 for i in range(7):
  a=i/7*math.pi*2;limb(n,[(0,y,0),(math.cos(a)*0.03,y-0.06,math.sin(a)*0.03),(math.cos(a)*0.05,y-0.16,math.sin(a)*0.05)],lambda t:0.011*(1-t*0.6),m=col,n=3,sub=1)
 lathe(n,[(0,y+0.02),(0.025,y+0.015),(0.028,y-0.005),(0,y-0.01)],'gold',seg=12)
W={}
def sword():
 n='sword';grip(n,0.0,0.17);pommel(n,0.19)
 lathe(n,[(0,0.005),(0.04,0.0),(0.045,-0.02),(0.03,-0.04),(0,-0.045)],'gold',seg=16,sx=1,sz=0.55)
 box(n,(0,-0.03,0),(0.24,0.035,0.06),'gold',bev=0.01)
 for s in(-1,1):ell(n,(s*0.13,-0.03,0),(0.03,0.025,0.035),m='gold',seg=12)
 blade(n,0.72,lambda t:0.032*(1-0.25*t)+0.006*(1-t),0.008,y0=-0.045,tipx=0)
 ell(n,(0,-0.03,0.03),(0.016,0.016,0.008),m='gem',seg=12)
def katana():
 n='katana';grip(n,0.0,0.24,r=0.022);lathe(n,[(0,0.26),(0.024,0.255),(0.024,0.24),(0,0.238)],'dark',seg=12)
 lathe(n,[(0,0.006),(0.055,0.004),(0.058,-0.004),(0,-0.006)],'dark',seg=24,sx=1.1,sz=0.8)
 lathe(n,[(0,-0.006),(0.024,-0.006),(0.024,-0.03),(0,-0.03)],'gold',seg=12)
 blade(n,0.78,lambda t:0.022*(1-0.15*t),0.007,y0=-0.03,single=True,xo=lambda t:0.06*t*t,tipx=-0.01)
def spear():
 n='spear';shaft(n,0.62,-0.95,r=0.022,rings=(0.55,-0.9))
 lathe(n,[(0,-0.92),(0.03,-0.94),(0.028,-1.0),(0.018,-1.03),(0,-1.035)],'gold',seg=12)
 blade(n,0.26,lambda t:0.045*math.sin(math.pi*(0.15+0.85*t))*(1-t*0.4)+0.004,0.012,y0=-1.03)
 tassel(n,-0.96)
def glaive():
 n='glaive';shaft(n,0.6,-0.9,r=0.024,rings=(0.52,-0.86))
 lathe(n,[(0,0.62),(0.03,0.61),(0.012,0.7),(0,0.72)],'metal',seg=10)
 lathe(n,[(0,-0.88),(0.034,-0.9),(0.036,-0.96),(0,-0.97)],'gold',seg=12)
 blade(n,0.46,lambda t:0.06+0.035*math.sin(math.pi*t*0.9)-0.05*t*t,0.012,y0=-0.96,single=True,xo=lambda t:0.07*t*t,tipx=0.02)
 for i in range(4):cone(n,(-0.01,-1.0-i*0.06,0),(-1,0.6,0),0.012,0.05,'gold',seg=6)
 tassel(n,-0.93)
 ell(n,(0.02,-1.0,0.012),(0.022,0.022,0.008),m='gem',seg=10)
def trident():
 n='trident';shaft(n,0.55,-0.9,r=0.022,rings=(0.48,))
 lathe(n,[(0,-0.88),(0.03,-0.9),(0.034,-0.95),(0,-0.96)],'gold',seg=12)
 limb(n,[(-0.11,-1.08,0),(-0.11,-1.0,0),(-0.06,-0.95,0),(0,-0.95,0),(0.06,-0.95,0),(0.11,-1.0,0),(0.11,-1.08,0)],lambda t:0.016,m='metal',n=24,sub=1)
 for x in(-0.11,0,0.11):blade(n,0.16 if x else 0.22,lambda t:0.022*(1-t*0.5),0.008,y0=-1.07 if x else -0.96,c=(x,0,0))
 for s in(-1,1):cone(n,(s*0.11,-1.12,0),(s*-1,0.5,0),0.01,0.05,'metal',seg=6)
def staff():
 n='staff';shaft(n,0.5,-0.78,r=0.026,rings=(0.42,0.0,-0.7))
 lathe(n,[(0,0.52),(0.03,0.51),(0.02,0.56),(0,0.58)],'gold',seg=12)
 ell(n,(0,-0.88,0),(0.09,0.09,0.09),m='ec',seg=24)
 torus(n,(0,-0.88,0),0.12,0.012,'gold',rot=(0,0,0));torus(n,(0,-0.88,0),0.12,0.01,'gold',rot=(0,math.pi/2,0))
 for i in range(4):
  a=i/4*math.pi*2;limb(n,[(0,-0.76,0),(math.cos(a)*0.08,-0.78,math.sin(a)*0.08),(math.cos(a)*0.11,-0.88,math.sin(a)*0.11)],lambda t:0.012,m='gold',n=6,sub=1)
def oar():
 n='oar';shaft(n,0.45,-0.7,r=0.024)
 lathe(n,[(0,0.5),(0.03,0.48),(0.03,0.44),(0,0.43)],'wood',seg=12)
 bm=bmesh.new();import bmesh as B
 o=box(n,(0,-0.92,0),(0.15,0.42,0.028),'wood',bev=0.012)
 box(n,(0,-0.74,0),(0.07,0.06,0.04),'gold',bev=0.006)
def hammer():
 n='hammer';shaft(n,0.42,-0.52,r=0.026,rings=(0.0,));pommel(n,0.44,0.03)
 lathe(n,[(0,-0.48),(0.06,-0.5),(0.11,-0.56),(0.12,-0.66),(0.11,-0.76),(0.06,-0.82),(0,-0.84)],'metal',seg=20)
 for i in range(8):
  a=i/8*math.pi*2;cone(n,(math.cos(a)*0.1,-0.66,math.sin(a)*0.1),(math.cos(a),0,math.sin(a)),0.025,0.06,'metal',seg=6)
 torus(n,(0,-0.66,0),0.12,0.012,'gold',rot=(math.pi/2,0,0))
def axe():
 n='axe';shaft(n,0.4,-0.62,r=0.026);pommel(n,0.42,0.03)
 lathe(n,[(0,-0.48),(0.035,-0.49),(0.035,-0.66),(0,-0.67)],'dark',seg=12)
 import bmesh
 bm=bmesh.new();M=C;P=lambda x,y,z:bm.verts.new((M@Vector((x,y,z,1))).to_3d())
 pts=[(0.03,-0.5),(0.12,-0.46),(0.26,-0.4),(0.3,-0.56),(0.26,-0.72),(0.12,-0.66),(0.03,-0.64)]
 top=[P(x,y,0.018 if x<0.2 else 0.004) for x,y in pts];bot=[P(x,y,-(0.018 if x<0.2 else 0.004)) for x,y in pts]
 bm.faces.new(top);bm.faces.new(list(reversed(bot)))
 for i in range(len(pts)):j=(i+1)%len(pts);bm.faces.new((top[i],bot[i],bot[j],top[j]))
 bmesh.ops.recalc_face_normals(bm,faces=bm.faces);o=obj_from_bm(bm,n,'metal',False);b=o.modifiers.new('b','BEVEL');b.width=0.004;b.segments=1
 cone(n,(-0.03,-0.57,0),(-1,0,0),0.03,0.1,'metal',seg=8)
def scythe():
 n='scythe';shaft(n,0.5,-0.82,r=0.024,rings=(0.4,-0.78))
 box(n,(0.0,-0.85,0),(0.06,0.08,0.05),'dark',bev=0.008)
 blade(n,0.55,lambda t:0.05*(1-t)+0.006,0.008,y0=0,single=True,c=(0.02,-0.85,0),rot=(0,0,math.pi/2+0.25),xo=lambda t:-0.12*t*t)
def kunai():
 n='kunai';blade(n,0.24,lambda t:0.045*math.sin(math.pi*(0.2+0.8*t))+0.004,0.01,y0=-0.04)
 lathe(n,[(0,0.0),(0.02,-0.005),(0.02,-0.04),(0,-0.045)],'dark',seg=8)
 grip(n,0.0,0.1,r=0.014);torus(n,(0,0.14,0),0.032,0.008,'metal',rot=(0,math.pi/2,0))
def claw():
 n='claw';box(n,(0,-0.02,0.03),(0.13,0.06,0.03),'dark',bev=0.008)
 for x in(-0.045,0,0.045):blade(n,0.28,lambda t:0.012*(1-t*0.5),0.006,y0=-0.05,c=(x,0,0.03),xo=lambda t:0.0,tipx=0)
def shuriken():
 n='shuriken';import bmesh
 bm=bmesh.new();P=lambda x,y,z:bm.verts.new((C@Vector((x,y-0.14,z+0.03,1))).to_3d());ring=[];top=P(0,0,0.014);bot=P(0,0,-0.014)
 for i in range(16):
  a=i/16*math.pi*2;r=0.17 if i%4==0 else (0.05 if i%4==2 else 0.07);aa=a+(0.12 if i%4==1 else 0)
  ring.append(P(math.cos(aa)*r,math.sin(aa)*r,0))
 for i in range(16):j=(i+1)%16;bm.faces.new((top,ring[i],ring[j]));bm.faces.new((bot,ring[j],ring[i]))
 o=obj_from_bm(bm,n,'metal',False)
 lathe(n,[(0,0.018),(0.03,0.016),(0.034,0),(0.03,-0.016),(0,-0.018)],'dark',seg=16,c=(0,-0.14,0.03),d=(0,0,1))
def bow():
 n='bow';P=[(0,0.55,0),(0,0.35,0.1),(0,0.12,0.06),(0,0.0,0.05),(0,-0.12,0.06),(0,-0.35,0.1),(0,-0.55,0)]
 limb(n,P,lambda t:0.022*(0.6+0.4*math.sin(math.pi*t))+0.008,m='wood',n=20,sub=1)
 grip(n,-0.08,0.16,r=0.032)
 for y in(0.53,-0.53):lathe(n,[(0,y+0.02),(0.02,y+0.01),(0.02,y-0.01),(0,y-0.02)],'gold',seg=10,c=(0,0,0))
 limb(n,[(0,0.54,-0.005),(0,0,-0.03),(0,-0.54,-0.005)],lambda t:0.004,m='string',n=4,sub=1)
def crossbow():
 n='crossbow';box(n,(0,-0.1,0.2),(0.06,0.06,0.56),'wood',bev=0.01)
 box(n,(0,-0.02,0.0),(0.05,0.16,0.07),'wood',rot=(0.3,0,0),bev=0.01)
 P=[(-0.32,-0.1,0.36),(-0.15,-0.1,0.44),(0,-0.1,0.46),(0.15,-0.1,0.44),(0.32,-0.1,0.36)]
 limb(n,P,lambda t:0.016+0.01*math.sin(math.pi*t),m='gold',n=20,sub=1)
 limb(n,[(-0.32,-0.1,0.36),(0,-0.1,0.12),(0.32,-0.1,0.36)],lambda t:0.004,m='string',n=4,sub=1)
 box(n,(0,-0.06,0.25),(0.012,0.012,0.3),'wood');cone(n,(0,-0.06,0.4),(0,0,1),0.015,0.05,'metal',seg=6)
 ell(n,(0,-0.06,0.46),(0.03,0.03,0.03),m='gem',seg=12)
def fan():
 n='fan';import bmesh
 for i in range(13):
  a=math.pi+i/12*math.pi;box(n,(math.cos(a)*0.17,-0.04+math.sin(a)*0.17,0.025),(0.34,0.012,0.006),'wood',rot=(0,0,a))
 bm=bmesh.new();P=lambda x,y,z:bm.verts.new((C@Vector((x,y,z,1))).to_3d());rows=[]
 for k,r in enumerate((0.12,0.24,0.34)):
  row=[]
  for i in range(25):
   a=math.pi+i/24*math.pi;row.append(P(math.cos(a)*r,-0.04+math.sin(a)*r,0.03+(0.008 if i%2 else -0.008)*(r/0.34)))
  rows.append(row)
 for k in range(2):
  for i in range(24):bm.faces.new((rows[k][i],rows[k][i+1],rows[k+1][i+1],rows[k+1][i]))
 o=obj_from_bm(bm,n,'acc',False);o.modifiers.new('s','SOLIDIFY').thickness=0.004
 for i in range(24):
  a=math.pi+(i+0.5)/24*math.pi
 limb(n,[(math.cos(a)*0.335,-0.04+math.sin(a)*0.335,0.03) for a in [math.pi+k/16*math.pi for k in range(17)]],lambda t:0.006,m='gold',n=32,sub=1)
 lathe(n,[(0,0.012),(0.02,0.01),(0.02,-0.01),(0,-0.012)],'gold',seg=10,c=(0,-0.04,0.03),d=(0,0,1))
 tassel(n,-0.03)
def scroll():
 n='scroll';lathe(n,[(0,0.24),(0.05,0.23),(0.05,-0.23),(0,-0.24)],'paper',seg=20,c=(0,-0.1,0.05),d=(1,0,0))
 for s in(-1,1):lathe(n,[(0,0.0),(0.03,0.0),(0.035,0.03),(0.022,0.06),(0,0.065)],'wood',seg=12,c=(s*0.24,-0.1,0.05),d=(s,0,0))
 torus(n,(0,-0.1,0.05),0.052,0.006,'red',rot=(0,math.pi/2,0))
def orb():
 n='orb';ell(n,(0,-0.2,0.12),(0.11,0.11,0.11),m='ec',seg=28)
 for i in range(3):torus(n,(0,-0.2,0.12),0.135,0.006,'gold',rot=(i*1.05,i*0.7,0))
 lathe(n,[(0,-0.06),(0.05,-0.08),(0.03,-0.1),(0,-0.1)],'gold',seg=14,c=(0,0,0.12))
def bell():
 n='bell';lathe(n,[(0,0.0),(0.02,-0.005),(0.04,-0.03),(0.05,-0.08),(0.07,-0.17),(0.1,-0.24),(0.095,-0.25),(0.06,-0.2),(0,-0.19)],'gold',seg=28,c=(0,-0.05,0.05))
 torus(n,(0,-0.04,0.05),0.025,0.008,'gold',rot=(0,math.pi/2,0))
 for y in(-0.13,-0.2):torus(n,(0,-0.05+y+0.05,0.05),0.07+(0.02 if y<-0.15 else 0),0.006,'gold',rot=(math.pi/2,0,0))
 ell(n,(0,-0.27,0.05),(0.025,0.025,0.025),m='dark',seg=12)
def brush():
 n='brush';shaft(n,0.22,-0.26,r=0.016,m='wood');lathe(n,[(0,0.24),(0.02,0.23),(0.018,0.21),(0,0.2)],'red',seg=10)
 lathe(n,[(0,-0.24),(0.02,-0.26),(0.022,-0.3),(0,-0.31)],'gold',seg=10)
 lathe(n,[(0,-0.3),(0.026,-0.31),(0.03,-0.36),(0.018,-0.42),(0,-0.46)],'ink',seg=14)
def flag():
 n='flag';shaft(n,0.62,-0.8,r=0.02,rings=(0.55,))
 lathe(n,[(0,-0.78),(0.03,-0.8),(0.012,-0.88),(0,-0.94)],'gold',seg=10)
 ell(n,(0,-0.82,0),(0.03,0.03,0.03),m='gold',seg=12)
def lantern():
 n='lantern';lathe(n,[(0,-0.04),(0.035,-0.05),(0.035,-0.07),(0.08,-0.09),(0.12,-0.16),(0.13,-0.22),(0.12,-0.28),(0.08,-0.35),(0.035,-0.37),(0.035,-0.39),(0,-0.4)],'lamp',seg=24,c=(0,0,0.06))
 for i in range(8):
  a=i/8*math.pi*2;limb(n,[(math.cos(a)*0.08,-0.09,0.06+math.sin(a)*0.08),(math.cos(a)*0.13,-0.22,0.06+math.sin(a)*0.13),(math.cos(a)*0.08,-0.35,0.06+math.sin(a)*0.08)],lambda t:0.005,m='dark',n=4,sub=1)
 for y in(-0.05,-0.38):lathe(n,[(0,y+0.015),(0.045,y+0.012),(0.045,y-0.012),(0,y-0.015)],'gold',seg=16,c=(0,0,0.06))
 tassel(n,-0.41)
 limb(n,[(0,0.1,0.06),(0,0.0,0.06),(0,-0.04,0.06)],lambda t:0.008,m='dark',n=4,sub=1)
for f in(sword,katana,spear,glaive,trident,staff,oar,hammer,axe,scythe,kunai,claw,shuriken,bow,crossbow,fan,scroll,orb,bell,brush,flag,lantern):f()
objs=finish_nodes({},{})
for k,o in objs.items():
 t=tris([o])
 if t>1500:
  bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;d=o.modifiers.new('d','DECIMATE');d.ratio=1500/t;bpy.ops.object.modifier_apply(modifier='d')
COL={'metal':((0.78,0.8,0.85),1,0.25),'gold':((0.95,0.7,0.2),1,0.3),'wood':((0.35,0.2,0.08),0,0.6),'cloth':((0.15,0.1,0.1),0,0.8),'dark':((0.08,0.08,0.1),0.5,0.4),'red':((0.8,0.08,0.06),0,0.7),'gem':((0.1,0.5,1),0,0.1),'ec':((0.3,0.8,1),0,0.2),'acc':((0.9,0.3,0.2),0,0.6),'paper':((0.95,0.92,0.8),0,0.8),'string':((0.9,0.9,0.85),0,0.8),'ink':((0.05,0.05,0.05),0,0.6),'lamp':((1,0.3,0.15),0,0.5)}
for n,m in MATS.items():
 if n in COL:
  c,mt,r=COL[n];bs=m.node_tree.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=(*c,1);bs.inputs['Metallic'].default_value=mt;bs.inputs['Roughness'].default_value=r;m.diffuse_color=(*c,1)
print('TRIS',{k:tris([o]) for k,o in objs.items()})
export(os.path.join(OUT,'weapons.glb'))
