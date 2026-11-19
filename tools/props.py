# Đạo cụ chiêu thức: voi chiến (xám / trắng), ngựa sắt Phù Đổng, cọc Bạch Đằng – render khung hình bằng Cycles (nền trong suốt)
import sys,os,math;sys.path.insert(0,os.path.dirname(__file__))
from blib import *
A=sys.argv[sys.argv.index('--')+1:];OUT=A[0];WHAT=A[1].split(',');NF=int(A[2]) if len(A)>2 else 8
def setup(cx=0.1,cy=0.85,w=2.8,h=2.1,res=320):
 sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=16;sc.cycles.use_denoising=True;sc.cycles.device='CPU'
 sc.render.resolution_x=res;sc.render.resolution_y=int(res*h/w);sc.render.film_transparent=True;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
 sc.view_settings.view_transform='Standard';sc.view_settings.exposure=0
 cam=bpy.data.cameras.new('c');cam.type='ORTHO';cam.ortho_scale=max(w,h);co=bpy.data.objects.new('c',cam);sc.collection.objects.link(co)
 co.location=cv((cx,cy,10));co.rotation_euler=(math.pi/2,0,0);sc.camera=co
 # camera nhìn từ +z (three) = -y (blender) về phía +y
 w0=bpy.data.worlds.new('w');sc.world=w0;w0.use_nodes=True;w0.node_tree.nodes['Background'].inputs[0].default_value=(0.55,0.58,0.65,1);w0.node_tree.nodes['Background'].inputs[1].default_value=0.8
 l=bpy.data.lights.new('s','SUN');l.energy=3.2;lo=bpy.data.objects.new('s',l);sc.collection.objects.link(lo);lo.rotation_euler=(math.radians(50),math.radians(-20),math.radians(-30))
def skinmat(name,col,bump=0.6,metal=0,rough=0.7,emit=None):
 m=mat(name);nt=m.node_tree;bs=nt.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=(*col,1);bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal
 if emit:bs.inputs['Emission Color'].default_value=(*emit,1);bs.inputs['Emission Strength'].default_value=3
 tc=nt.nodes.new('ShaderNodeTexCoord');t=nt.nodes.new('ShaderNodeTexNoise');t.inputs['Scale'].default_value=9;t.inputs['Detail'].default_value=4
 nt.links.new(tc.outputs['Object'],t.inputs['Vector']);b=nt.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=bump;nt.links.new(t.outputs['Fac'],b.inputs['Height']);nt.links.new(b.outputs['Normal'],bs.inputs['Normal'])
 return m
def plain(name,col,rough=0.6,metal=0,emit=None):
 m=mat(name);bs=m.node_tree.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=(*col,1);bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal
 if emit:bs.inputs['Emission Color'].default_value=(*emit,1);bs.inputs['Emission Strength'].default_value=4
 return m
def render(path):
 for parts in PARTS.values():
  for o in parts:pass
 bpy.context.scene.render.filepath=path;bpy.ops.render.render(write_still=True)
def elephant(ph,white):
 clear();setup();skin=skinmat('M',(0.86,0.84,0.8) if white else (0.38,0.38,0.42),0.18)
 plain('ivory',(0.95,0.92,0.84),0.4);plain('cloth',(0.62,0.06,0.06),0.7);plain('gold',(0.9,0.68,0.2),0.3,1);plain('wood',(0.35,0.2,0.08),0.6);plain('eye',(0.02,0.02,0.02),0.2);plain('nail',(0.85,0.8,0.7),0.5)
 s=math.sin(ph);c=math.cos(ph);bob=abs(s)*0.03
 limb('a',[(-0.6,0.72+bob,0),(-0.2,0.78+bob,0),(0.25,0.8+bob,0),(0.5,0.82+bob,0)],lambda t:0.36+0.08*math.sin(math.pi*t),n=12)
 ell('a',(0.7,0.88+bob,0),(0.27,0.3,0.25))
 for z in(-1,1):ell('a',(0.52,0.86+bob,z*0.24),(0.07,0.3,0.25),(0,z*0.3,0.1))
 sw=0.08*math.sin(ph*1.5)
 limb('a',[(0.86,0.82+bob,0),(1.0,0.6+bob,0),(1.02+sw,0.3+bob,0),(1.08+sw*1.5,0.1+bob,0)],lambda t:0.11-0.06*t,n=12)
 for z in(-1,1):limb('a',[(0.8,0.66+bob,z*0.1),(0.98,0.58+bob,z*0.12),(1.1,0.68+bob,z*0.1)],lambda t:0.035-0.022*t,m='ivory',n=6)
 for z in(-1,1):ell('a',(0.82,0.98+bob,z*0.2),(0.025,0.025,0.02),m='eye',seg=10)
 for (lx,lz,p) in((0.38,0.18,ph),(0.38,-0.18,ph+math.pi),(-0.4,0.18,ph+math.pi),(-0.4,-0.18,ph)):
  a=0.3*math.sin(p);top=(lx,0.62+bob,lz);knee=(lx+0.22*math.sin(a),0.32+bob*0.5,lz);foot=(lx+0.42*math.sin(a),0.05+max(0,math.cos(p))*0.04,lz)
  limb('a',[top,knee,foot],lambda t:0.13-0.015*t,n=8)
 limb('a',[(-0.6,0.9+bob,0),(-0.74,0.72+bob,0.02),(-0.76+0.04*s,0.5+bob,0.02)],lambda t:0.025,n=6)
 # yên bành: tấm vải đỏ viền vàng + bành gỗ
 box('a',(-0.08,1.12+bob,0),(0.9,0.06,0.86),'cloth',bev=0.02)
 for z in(-1,1):box('a',(-0.08,0.92+bob,z*0.4),(0.86,0.42,0.04),'cloth',rot=(z*-0.15,0,0),bev=0.01);box('a',(-0.08,0.72+bob,z*0.43),(0.86,0.04,0.05),'gold')
 box('a',(-0.1,1.27+bob,0),(0.5,0.24,0.5),'wood',bev=0.02)
 for x in(-0.33,0.13):
  for z in(-0.23,0.23):lathe('a',[(0,1.6+bob),(0.025,1.58+bob),(0.025,1.38+bob),(0,1.36+bob)],'wood',seg=8,c=(x,0,z))
 box('a',(-0.1,1.62+bob,0),(0.56,0.05,0.56),'cloth',bev=0.01)
 render(OUT)
def horse(ph):
 clear();setup(cx=0.15,cy=0.75,w=2.6,h=1.9);iron=skinmat('M',(0.2,0.21,0.25),0.06,metal=1,rough=0.3);plain('glow',(1,0.5,0.1),0.4,emit=(1,0.45,0.08));plain('dark',(0.05,0.05,0.06),0.5)
 s=math.sin(ph);bob=0.05*math.sin(ph*2)
 limb('a',[(-0.5,0.62+bob,0),(-0.1,0.66+bob,0),(0.3,0.68+bob,0),(0.48,0.72+bob,0)],lambda t:0.25+0.05*math.sin(math.pi*t),n=10)
 limb('a',[(0.45,0.74+bob,0),(0.62,0.98+bob,0),(0.75,1.12+bob,0)],lambda t:0.13-0.04*t,n=8)
 limb('a',[(0.72,1.15+bob,0),(0.88,1.1+bob,0),(0.98,1.0+bob,0)],lambda t:0.09-0.03*t,n=6)
 for z in(-1,1):cone('a',(0.72,1.22+bob,z*0.05),(0,1,0.1*z),0.035,0.12,'M',seg=6);ell('a',(0.86,1.12+bob,z*0.07),(0.02,0.015,0.012),m='glow',seg=8)
 for (lx,lz,p) in((0.38,0.1,ph),(0.32,-0.1,ph+0.6),(-0.38,0.1,ph+math.pi),(-0.44,-0.1,ph+math.pi+0.6)):
  a=0.55*math.sin(p);top=(lx,0.55+bob,lz);knee=(lx+0.2*math.sin(a),0.3+bob+max(0,math.sin(p))*0.08,lz);foot=(lx+0.36*math.sin(a+0.3),0.04+max(0,math.sin(p))*0.12,lz)
  limb('a',[top,knee,foot],lambda t:0.07-0.02*t,n=8);ell('a',(foot[0]+0.02,foot[1],lz),(0.05,0.035,0.045),m='dark',seg=10)
 for i in range(8):u=i/7;cone('a',(0.5+0.24*u,0.9+0.3*u+bob,0),(-0.6,0.8,0),0.05,0.16,'glow',seg=6)
 limb('a',[(-0.45,0.7+bob,0),(-0.68,0.66+bob,0),(-0.8,0.48+bob+0.05*s,0)],lambda t:0.04,m='glow',n=6)
 render(OUT)
def stake():
 clear();setup(cx=0,cy=0.75,w=0.5,h=1.6,res=96);skinmat('M',(0.36,0.22,0.1),0.25);plain('iron',(0.75,0.78,0.82),0.3,1);plain('rope',(0.6,0.5,0.3),0.9)
 lathe('a',[(0,0.0),(0.07,0.0),(0.075,1.2),(0.07,1.25),(0,1.26)],'M',seg=14)
 lathe('a',[(0,1.18),(0.085,1.18),(0.07,1.32),(0.03,1.45),(0,1.52)],'iron',seg=14)
 for y in(0.4,1.1):torus('a',(0,y,0),0.078,0.012,'rope',rot=(math.pi/2,0,0),seg=20,mseg=5)
 render(OUT)
w=WHAT[0]
if w in('elephant','whiteelephant'):
 base=OUT
 for f in range(NF):OUT=base+'_%d.png'%f;elephant(f/NF*math.pi*2,w=='whiteelephant')
elif w=='horse':
 base=OUT
 for f in range(NF):OUT=base+'_%d.png'%f;horse(f/NF*math.pi*2)
else:
 OUT=OUT+'.png';stake()
