# Biểu tượng giao diện 3D (128px, nền trong suốt): xu, ngọc, vé, kiếm chéo, quà, tháp, chiêu mộ, bản đồ
import sys,os,math;sys.path.insert(0,os.path.dirname(__file__))
from blib import *
OUT=sys.argv[sys.argv.index('--')+1];WHAT=sys.argv[sys.argv.index('--')+2].split(',')
def setup():
 clear();sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=24;sc.cycles.use_denoising=True;sc.render.resolution_x=sc.render.resolution_y=128
 sc.render.film_transparent=True;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.view_settings.view_transform='Standard';sc.view_settings.look='Medium High Contrast'
 cam=bpy.data.cameras.new('c');cam.type='ORTHO';cam.ortho_scale=2.3;co=bpy.data.objects.new('c',cam);sc.collection.objects.link(co);co.location=cv((0,0,10));co.rotation_euler=(math.pi/2,0,0);sc.camera=co
 w=bpy.data.worlds.new('w');sc.world=w;w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(0.8,0.82,0.9,1);w.node_tree.nodes['Background'].inputs[1].default_value=1.0
 l=bpy.data.lights.new('k','AREA');l.energy=400;l.size=4;lo=bpy.data.objects.new('k',l);sc.collection.objects.link(lo);lo.location=cv((-3,4,5));lo.rotation_euler=(math.radians(-40),math.radians(-30),0)
 lo.constraints.new('TRACK_TO').target=co if False else None
def M2(n,col,metal=0,rough=0.4,emit=None,trans=0):
 m=mat(n);bs=m.node_tree.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=(*col,1);bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough
 if trans:bs.inputs['Transmission Weight'].default_value=trans;bs.inputs['IOR'].default_value=2.0
 if emit:bs.inputs['Emission Color'].default_value=(*emit,1);bs.inputs['Emission Strength'].default_value=1.5
def rnd(name):
 for parts in PARTS.values():
  for o in parts:
   for md in o.modifiers:pass
 bpy.context.scene.render.filepath=os.path.join(OUT,name+'.png');bpy.ops.render.render(write_still=True)
def coin():
 setup();M2('gold',(1,0.72,0.2),1,0.25);M2('dark',(0.35,0.2,0.02),1,0.5)
 lathe('a',[(0,0.09),(0.88,0.09),(0.95,0.04),(0.95,-0.04),(0.88,-0.09),(0,-0.09)],'gold',seg=48,d=(0,0,1))
 torus('a',(0,0,0.1),0.74,0.045,'gold',rot=(math.pi/2,0,0),seg=48)
 box('a',(0,0,0.1),(0.36,0.36,0.04),'dark',bev=0.01)
 for i in range(4):a=i*math.pi/2;box('a',(math.cos(a)*0.46,math.sin(a)*0.46,0.11),(0.1 if i%2==0 else 0.22,0.22 if i%2==0 else 0.1,0.04),'gold',bev=0.01)
 for o in PARTS['a']:o.matrix_world=C@Matrix.Rotation(0.35,4,'X')@Matrix.Rotation(-0.3,4,'Y')@C.inverted()@o.matrix_world
 rnd('coin')
def gem():
 setup();M2('g',(0.2,0.6,1),0,0.02,trans=0.6)
 bm=bmesh.new() if False else None
 bpy.ops.mesh.primitive_cone_add(vertices=8,radius1=0.75,radius2=0.5,depth=0.3,location=cv((0,0.25,0)));o=bpy.context.object;bpy.ops.object.transform_apply();add('a',o,'g')
 bpy.ops.mesh.primitive_cone_add(vertices=8,radius1=0.75,radius2=0,depth=0.9,location=cv((0,-0.35,0)),rotation=(math.pi/2,0,0));o=bpy.context.object;o.rotation_euler=(-math.pi/2+math.pi/2*0,0,0);o.matrix_world=C@Matrix.Translation((0,-0.35,0))@Matrix.Rotation(math.pi,4,'X')@Matrix.Rotation(-math.pi/2,4,'X');add('a',o,'g')
 for o in PARTS['a']:o.rotation_euler.x+=0.25
 rnd('gem')
def ticket():
 setup();M2('red',(0.8,0.1,0.08),0,0.5);M2('gold',(1,0.75,0.2),1,0.3);M2('paper',(1,0.92,0.7),0,0.6)
 box('a',(0,0,0),(1.7,0.95,0.06),'red',rot=(0.25,0.3,-0.15),bev=0.04)
 box('a',(0,0,0.05),(1.4,0.7,0.02),'paper',rot=(0.25,0.3,-0.15),bev=0.01)
 ell('a',(0.02,0.0,0.12),(0.2,0.2,0.05),(0.25,0.3,-0.15),m='gold',seg=20)
 rnd('ticket')
def swords():
 setup();M2('metal',(0.85,0.88,0.92),1,0.15);M2('gold',(1,0.75,0.2),1,0.3);M2('wood',(0.4,0.1,0.05),0,0.5)
 for s in(-1,1):
  r=s*0.75
  blade('a',1.4,lambda t:0.08*(1-0.3*t)+0.01,0.02,y0=-0.15,c=(0,0,s*0.05),rot=(0,0,0))
  box('a',(0,-0.15,s*0.05),(0.5,0.08,0.1),'gold',bev=0.02);lathe('a',[(0,0.35),(0.06,0.33),(0.06,-0.12),(0,-0.14)],'wood',seg=12,c=(0,0,s*0.05))
  ell('a',(0,0.38,s*0.05),(0.08,0.08,0.08),m='gold',seg=12)
  for o in PARTS['a'][-5:]:
   o.matrix_world=C@Matrix.Rotation(r,4,'Z')@Matrix.Translation((0,0.15,0))@C.inverted()@o.matrix_world
 rnd('swords')
def gift():
 setup();M2('red',(0.85,0.12,0.1),0,0.5);M2('gold',(1,0.78,0.2),1,0.3)
 R=(0.35,0.6,0)
 box('a',(0,-0.2,0),(1.2,0.95,1.2),'red',rot=R,bev=0.04);box('a',(0,0.33,0),(1.35,0.22,1.35),'red',rot=R,bev=0.04)
 box('a',(0,-0.1,0),(0.22,1.2,1.38),'gold',rot=R,bev=0.02);box('a',(0,-0.1,0),(1.38,1.2,0.22),'gold',rot=R,bev=0.02)
 for s in(-1,1):ell('a',(s*0.25,0.58,0),(0.28,0.16,0.1),(0,0,s*0.5),m='gold',seg=16)
 rnd('gift')
def tower():
 setup();M2('wall',(0.92,0.86,0.72),0,0.6);M2('roof',(0.55,0.12,0.08),0,0.5);M2('gold',(1,0.78,0.2),1,0.3)
 y=-0.95
 for i,w in enumerate((0.7,0.6,0.5,0.4,0.3)):
  box('a',(0,y+0.14,0),(w,0.28,w),'wall');lathe('a',[(0,y+0.36),(w*0.8+0.2,y+0.28),(w*0.8+0.32,y+0.22),(0,y+0.24)],'roof',seg=4);y+=0.36
 lathe('a',[(0,y+0.35),(0.04,y+0.3),(0.06,y),(0,y-0.02)],'gold',seg=10)
 for o in PARTS['a']:o.matrix_world=C@Matrix.Rotation(0.6,4,'Y')@C.inverted()@o.matrix_world
 rnd('tower')
def summon():
 setup();M2('glass',(0.7,0.4,1),0,0.02,emit=(0.5,0.2,1),trans=0.5);M2('gold',(1,0.78,0.2),1,0.3)
 ell('a',(0,0.15,0),(0.62,0.62,0.62),m='glass',seg=32)
 lathe('a',[(0,-0.45),(0.5,-0.45),(0.6,-0.6),(0.7,-0.85),(0,-0.85)],'gold',seg=32)
 for i in range(3):torus('a',(0,0.15,0),0.72,0.03,'gold',rot=(i*1.0,i*0.6,0.3))
 rnd('summon')
def mapic():
 setup();M2('paper',(0.95,0.85,0.6),0,0.7);M2('wood',(0.45,0.25,0.1),0,0.5);M2('red',(0.8,0.1,0.08),0,0.5);M2('green',(0.3,0.6,0.3),0,0.7)
 R=(0.3,0.25,-0.1)
 box('a',(0,0,0),(1.5,1.1,0.03),'paper',rot=R)
 for s in(-1,1):lathe('a',[(0,0.85),(0.09,0.84),(0.09,-0.84),(0,-0.85)],'wood',seg=14,c=(s*0.78,0,0.02),d=(0,1,0));PARTS['a'][-1].rotation_euler=R
 for p in((-0.3,0.2),(0.1,-0.1),(0.35,0.25)):ell('a',(p[0],p[1],0.04),(0.18,0.12,0.03),R,m='green',seg=12)
 ell('a',(0.3,-0.25,0.06),(0.08,0.08,0.04),R,m='red',seg=12)
 rnd('map')
import bmesh
for w in WHAT:globals()[w]()
