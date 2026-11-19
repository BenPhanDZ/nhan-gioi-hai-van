# Nền chiến trường cho 5 chương mới – dựng & render bằng Blender Cycles
# Mỗi cảnh xuất 2 ảnh: <tên>.jpg (toàn cảnh) và <tên>_gr.png (lớp nền đất phía trước, trong suốt phần trên)
import bpy,math,random,sys,os
from mathutils import Vector
A=sys.argv[sys.argv.index('--')+1:];OUT=A[0];WHICH=A[1].split(',');SAMP=int(A[2]) if len(A)>2 else 24;RES=float(A[3]) if len(A)>3 else 1.0
def reset():
 bpy.ops.wm.read_factory_settings(use_empty=True)
 sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=SAMP;sc.cycles.use_denoising=True
 sc.render.resolution_x=int(1900*RES);sc.render.resolution_y=int(720*RES);sc.render.resolution_percentage=100
 sc.view_settings.view_transform='AgX';sc.view_settings.exposure=-2.5;sc.view_settings.look='AgX - Punchy';sc.cycles.max_bounces=4
 for n in('GROUND','BACK'):c=bpy.data.collections.new(n);sc.collection.children.link(c)
 return sc
def coll(n):return bpy.data.collections[n]
def link(o,c='BACK'):
 for u in list(o.users_collection):u.objects.unlink(o)
 coll(c).objects.link(o);return o
def M(name,col,rough=0.6,metal=0,emit=None,es=3,tex=None,scale=4,bump=0.3,col2=None,alpha=None,trans=0):
 m=bpy.data.materials.new(name);m.use_nodes=True;nt=m.node_tree;bs=nt.nodes['Principled BSDF']
 bs.inputs['Base Color'].default_value=(*col,1);bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal
 if trans:bs.inputs['Transmission Weight'].default_value=trans
 if emit:bs.inputs['Emission Color'].default_value=(*emit,1);bs.inputs['Emission Strength'].default_value=es
 if tex:
  tc=nt.nodes.new('ShaderNodeTexCoord')
  if tex=='brick' and False:
   t=nt.nodes.new('ShaderNodeTexBrick');t.inputs['Scale'].default_value=scale;t.inputs['Color1'].default_value=(*col,1);t.inputs['Color2'].default_value=(*(col2 or [c*0.8 for c in col]),1);t.inputs['Mortar'].default_value=(0.55,0.5,0.45,1);t.inputs['Mortar Size'].default_value=0.015
   nt.links.new(tc.outputs['Object'],t.inputs['Vector']);nt.links.new(t.outputs['Color'],bs.inputs['Base Color'])
   b=nt.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=bump;nt.links.new(t.outputs['Fac'],b.inputs['Height']);nt.links.new(b.outputs['Normal'],bs.inputs['Normal'])
  else:
   t=nt.nodes.new('ShaderNodeTexNoise');t.inputs['Scale'].default_value=scale;t.inputs['Detail'].default_value=8
   nt.links.new(tc.outputs['Object'],t.inputs['Vector'])
   r=nt.nodes.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(*[c*0.6 for c in col],1) if not col2 else (*col2,1);r.color_ramp.elements[1].color=(*[min(1,c*1.25) for c in col],1)
   nt.links.new(t.outputs['Fac'],r.inputs['Fac']);nt.links.new(r.outputs['Color'],bs.inputs['Base Color'])
   b=nt.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=bump;nt.links.new(t.outputs['Fac'],b.inputs['Height']);nt.links.new(b.outputs['Normal'],bs.inputs['Normal'])
 if alpha is not None:bs.inputs['Alpha'].default_value=alpha
 return m
def setm(o,m):o.data.materials.clear();o.data.materials.append(m);return o
def box(c,s,m,rot=(0,0,0),col='BACK',bev=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=c,rotation=rot);o=bpy.context.object;o.scale=s;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bev:md=o.modifiers.new('b','BEVEL');md.width=bev;md.segments=2
 return link(setm(o,m),col)
def cyl(c,r,h,m,col='BACK',v=24,r2=None,rot=(0,0,0)):
 if r2 is None:bpy.ops.mesh.primitive_cylinder_add(vertices=v,radius=r,depth=h,location=(c[0],c[1],c[2]+h/2),rotation=rot)
 else:bpy.ops.mesh.primitive_cone_add(vertices=v,radius1=r,radius2=r2,depth=h,location=(c[0],c[1],c[2]+h/2),rotation=rot)
 o=bpy.context.object;bpy.ops.object.shade_smooth();return link(setm(o,m),col)
def sph(c,r,m,col='BACK',sub=2,sc=(1,1,1)):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=r,location=c);o=bpy.context.object;o.scale=sc;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);bpy.ops.object.shade_smooth();return link(setm(o,m),col)
def terrain(c,size,height,m,col='BACK',seed=1,noise=2.0,sub=6,falloff=True):
 bpy.ops.mesh.primitive_grid_add(x_subdivisions=2**sub,y_subdivisions=2**sub,size=1,location=c);o=bpy.context.object;o.scale=(size[0],size[1],1)
 bpy.ops.object.transform_apply(scale=True)
 rnd=random.Random(seed);ph=[rnd.random()*10 for _ in range(6)]
 for v in o.data.vertices:
  x,y=v.co.x/size[0],v.co.y/size[1]
  h=0.5*math.sin(x*noise*3+ph[0])*math.cos(y*noise*2+ph[1])+0.3*math.sin(x*noise*7+ph[2]+y*3)+0.2*math.sin(x*noise*13+ph[3])*math.sin(y*noise*11+ph[4])
  h=(h+1)/2
  if falloff:h*=max(0,1-((x*2)**2+(y*2)**2)**0.5)
  v.co.z=h*height
 bpy.ops.object.shade_smooth();md=o.modifiers.new('s','SUBSURF');md.levels=1
 return link(setm(o,m),col)
def peak(c,r,h,m,col='BACK',seed=1):
 bpy.ops.mesh.primitive_cone_add(vertices=48,radius1=r,radius2=0,depth=h,location=(c[0],c[1],c[2]+h/2));o=bpy.context.object
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.subdivide(number_cuts=4);bpy.ops.object.mode_set(mode='OBJECT')
 rnd=random.Random(seed)
 for v in o.data.vertices:
  k=1-(v.co.z+h/2)/h;n=0.75+0.25*math.sin(math.atan2(v.co.y,v.co.x)*5+seed)+0.12*math.sin(v.co.z*0.4+seed*3)
  v.co.x*=n;v.co.y*=n;v.co.z+=rnd.uniform(-0.03,0.03)*h
 md=o.modifiers.new('d','DISPLACE');tx=bpy.data.textures.new('t%d'%seed,'CLOUDS');tx.noise_scale=r*0.25;md.texture=tx;md.strength=r*0.15
 o.modifiers.new('s','SUBSURF').levels=1;bpy.ops.object.shade_smooth();return link(setm(o,m),col)
def tree(c,s,mt,ml,col='BACK',kind='round',seed=0):
 rnd=random.Random(seed)
 cyl(c,0.12*s,1.6*s,mt,col,v=8,r2=0.07*s)
 if kind=='pine':
  for i in range(4):cyl((c[0],c[1],c[2]+(1.0+i*0.75)*s),(1.1-i*0.22)*s,1.3*s,ml,col,v=10,r2=0.05*s)
 elif kind=='palm':
  o=cyl(c,0.13*s,5.5*s,mt,col,v=8,r2=0.09*s);o.rotation_euler=(0.12,0.1,0)
  top=(c[0]+0.3*s,c[1]+0.5*s,c[2]+5.4*s)
  for i in range(8):
   a=i/8*math.pi*2;f=box((top[0]+math.cos(a)*1.2*s,top[1]+math.sin(a)*1.2*s,top[2]-0.3*s),(2.6*s,0.5*s,0.03*s),ml,rot=(0,0.35,a),col=col)
 else:
  for i in range(5):sph((c[0]+rnd.uniform(-0.6,0.6)*s,c[1]+rnd.uniform(-0.6,0.6)*s,c[2]+(1.9+rnd.uniform(0,1.0))*s),(0.9+rnd.random()*0.5)*s,ml,col,sub=2)
def roof(c,w,d,h,m,col='BACK',curl=0.25,over=0.6):
 # mái ngói: lăng trụ tam giác cong nhẹ đầu đao
 import bmesh
 me=bpy.data.meshes.new('r');bm=bmesh.new();W=w/2+over;D=d/2+over;n=8
 rows=[]
 for i in range(n+1):
  x=-W+2*W*i/n;e=curl*h*((abs(x)/W)**4)
  rows.append([bm.verts.new((x,-D,c[2]+e)),bm.verts.new((x,0,c[2]+h)),bm.verts.new((x,D,c[2]+e))])
 for i in range(n):
  a,b=rows[i],rows[i+1]
  bm.faces.new((a[0],b[0],b[1],a[1]));bm.faces.new((a[1],b[1],b[2],a[2]))
 bm.faces.new((rows[0][0],rows[0][1],rows[0][2]));bm.faces.new((rows[-1][2],rows[-1][1],rows[-1][0]))
 bm.to_mesh(me);o=bpy.data.objects.new('r',me);bpy.context.collection.objects.link(o);o.location=(c[0],c[1],0)
 md=o.modifiers.new('s','SOLIDIFY');md.thickness=0.12
 return link(setm(o,m),col)
VAR='day'
def sky(sc,elev=25,rot=0,strength=1.0,dust=1.0,air=1.0):
 if VAR=='dusk':elev=4;dust=max(dust,2.5);strength*=0.8
 if VAR=='mist':dust=6;air=2;elev=max(elev,10)
 night=VAR=='night'
 if night:elev=8;strength=0.03
 w=bpy.data.worlds.new('w');sc.world=w;w.use_nodes=True;nt=w.node_tree;bg=nt.nodes['Background']
 s=nt.nodes.new('ShaderNodeTexSky');s.sky_type='NISHITA';s.sun_elevation=math.radians(elev);s.sun_rotation=math.radians(rot);s.dust_density=dust;s.air_density=air
 nt.links.new(s.outputs['Color'],bg.inputs['Color']);bg.inputs['Strength'].default_value=strength*0.3
 l=bpy.data.lights.new('sun','SUN');l.energy=0.35 if night else (1.2 if VAR=='dusk' else 2.2);l.color=(0.6,0.7,1.0) if night else (1,1,1);l.angle=math.radians(2);lo=bpy.data.objects.new('sun',l);sc.collection.objects.link(lo)
 lo.rotation_euler=(math.radians(90-elev),0,math.radians(rot+180));return l
def camera(sc,h=1.7,fov=62,pitch=3.8):
 cam=bpy.data.cameras.new('cam');cam.sensor_fit='HORIZONTAL';cam.angle=math.radians(fov);cam.clip_end=3000
 co=bpy.data.objects.new('cam',cam);sc.collection.objects.link(co);co.location=(0,-12,h);co.rotation_euler=(math.radians(90+pitch),0,0);sc.camera=co
def water(c,size,col=(0.05,0.25,0.35),colr='BACK'):
 bpy.ops.mesh.primitive_plane_add(size=1,location=c);o=bpy.context.object;o.scale=(size[0],size[1],1)
 m=bpy.data.materials.new('water');m.use_nodes=True;nt=m.node_tree;bs=nt.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=(*col,1);bs.inputs['Roughness'].default_value=0.05;bs.inputs['IOR'].default_value=1.33;bs.inputs['Specular IOR Level'].default_value=0.8
 tc=nt.nodes.new('ShaderNodeTexCoord');t=nt.nodes.new('ShaderNodeTexWave');t.inputs['Scale'].default_value=0.6;t.inputs['Distortion'].default_value=6;t.inputs['Detail'].default_value=4
 nt.links.new(tc.outputs['Object'],t.inputs['Vector']);b=nt.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=0.15;nt.links.new(t.outputs['Fac'],b.inputs['Height']);nt.links.new(b.outputs['Normal'],bs.inputs['Normal'])
 return link(setm(o,m),colr)
def ground_plane(m,z=0):
 bpy.ops.mesh.primitive_plane_add(size=1,location=(0,40,z));o=bpy.context.object;o.scale=(160,110,1);return link(setm(o,m),'GROUND')
def render(sc,name):
 sc.render.image_settings.file_format='JPEG';sc.render.image_settings.quality=85;sc.render.film_transparent=False
 if VAR=='night':
  for m in bpy.data.materials:
   bs=m.node_tree.nodes.get('Principled BSDF') if m.use_nodes else None
   if bs and bs.inputs['Emission Strength'].default_value>0:bs.inputs['Emission Strength'].default_value*=2.5
  sc.view_settings.exposure=0.4
 if VAR=='dusk':sc.view_settings.exposure=-1.2
 if VAR=='mist':
  w=sc.world;nt=w.node_tree;vs=nt.nodes.new('ShaderNodeVolumePrincipled');vs.inputs['Density'].default_value=0.004;nt.links.new(vs.outputs[0],nt.nodes['World Output'].inputs['Volume'])
 sc.render.filepath=os.path.join(OUT,name+'_'+VAR+'.jpg');bpy.ops.render.render(write_still=True)

# ---------------- CẢNH ----------------
def dienhai():
 sc=reset();sky(sc,elev=28,rot=200);camera(sc)
 stone=M('stone',(0.42,0.38,0.33),0.85,tex='noise',scale=0.5,bump=0.4);ground_plane(stone)
 brick=M('brick',(0.48,0.22,0.14),0.85,tex='brick',scale=1.5,col2=(0.36,0.16,0.1),bump=0.6)
 # đường lát đá dẫn vào cổng
 path=M('path',(0.6,0.56,0.5),0.8,tex='brick',scale=0.35,col2=(0.5,0.47,0.42),bump=0.3);box((0,40,0.01),(9,70,0.02),path,col='GROUND')
 # tường thành + hào nước
 for x in(-1,1):box((x*52,78,3.2),(88,5,6.4),brick,bev=0.1)
 for x in range(-46,47,4):
  if abs(x)>9:box((x*2.2/2.2,75.3,6.9),(2.2,1.2,1.0),brick)
 # cổng: khối cổng có vòm, lầu mái ngói 2 tầng
 box((0,78,4),(18,7,8),brick,bev=0.1);
 arch=cyl((0,74,0),3.0,8,M('dark',(0.03,0.03,0.03),1),v=32,rot=(math.pi/2,0,0));arch.location=(0,78,3.0);arch.scale=(1,1,1.2)
 box((0,74.4,1.5),(6,0.6,3.0),M('dark2',(0.03,0.03,0.03),1))
 wood=M('wood',(0.35,0.12,0.06),0.6);tile=M('tile',(0.32,0.12,0.07),0.7,tex='noise',scale=6,bump=0.5)
 for i,x in enumerate((-6,-2,2,6)):cyl((x,77,8),0.35,4,wood,v=12)
 box((0,78,8.1),(15,6,0.4),wood);roof((0,78,12.0),15,6,2.8,tile);box((0,78,12.4),(10,4.5,2.2),wood);roof((0,78,14.6),10,4.5,2.4,tile)
 # hào nước phía trước tường
 water((0,72,-0.1),(160,4))
 # thần công trên bệ
 bronze=M('bronze',(0.35,0.28,0.12),0.35,metal=1)
 for x,y in((-9,28),(9,28),(-14,46),(14,46)):
  box((x,y,0.45),(1.6,2.6,0.9),wood,col='GROUND',bev=0.06)
  for s in(-1,1):cyl((x+s*0.85,y-0.4,0.6),0.55,0.18,wood,col='GROUND',rot=(0,math.pi/2,0),v=16)
  c=cyl((x,y,1.1),0.38,4.0,bronze,col='GROUND',r2=0.26,v=24);c.rotation_euler=(math.radians(-80),0,0);c.location=(x,y+1.8,1.2)
 # cờ đỏ trên lầu cổng
 cyl((0,78,16.8),0.08,7,wood,v=8);box((1.6,78,22),(3.2,0.05,2.0),M('flag',(0.75,0.06,0.04),0.7))
 # bán đảo Sơn Trà và núi phía xa, cây
 hill=M('hill',(0.18,0.32,0.2),0.9,tex='noise',scale=0.05,bump=0.2,col2=(0.1,0.2,0.12))
 peak((-160,520,0),260,180,hill,seed=3);peak((230,600,0),300,140,hill,seed=5);peak((40,700,0),250,110,hill,seed=8)
 leaf=M('leaf',(0.12,0.3,0.1),0.8,tex='noise',scale=3,bump=0.5);bark=M('bark',(0.2,0.12,0.06),0.9)
 rnd=random.Random(2)
 for i in range(26):x=rnd.uniform(-120,120);y=rnd.uniform(84,110);tree((x,y,0),rnd.uniform(1.8,2.8),bark,leaf,seed=i)
 for x in(-28,-20,20,28,-36,36):tree((x,16+abs(x)*0.6,0),1.6,bark,leaf,'GROUND',seed=x+50)
 grass=M('grass',(0.2,0.33,0.12),0.9,tex='noise',scale=2,bump=0.3)
 for x in(-1,1):box((x*62,40,0.03),(70,70,0.05),grass,col='GROUND')
 render(sc,'dienhai')
def bana():
 sc=reset();sky(sc,elev=12,rot=150,dust=2.5,air=1.5);camera(sc)
 rock=M('rock',(0.35,0.35,0.33),0.9,tex='noise',scale=0.6,bump=0.8);ground_plane(rock)
 grass=M('grass',(0.22,0.36,0.14),0.9,tex='noise',scale=1.5,bump=0.4)
 terrain((0,40,-0.2),(150,110),1.2,grass,'GROUND',seed=4,falloff=False)
 hill=M('mt',(0.14,0.28,0.18),0.9,tex='noise',scale=0.03,bump=0.3,col2=(0.08,0.16,0.12))
 far=M('mtf',(0.3,0.4,0.48),0.9)
 for i,(x,y,r,h) in enumerate([(-120,260,140,120),(80,300,180,150),(260,420,200,170),(-300,480,240,160),(20,900,500,260)]):peak((x,y,-60),r,h,hill if i<3 else far,seed=i+11)
 # biển mây
 cl=M('cloud',(0.82,0.86,0.93),1.0);cl.node_tree.nodes['Principled BSDF'].inputs['Subsurface Weight'].default_value=0.4
 rnd=random.Random(7)
 for i in range(60):sph((rnd.uniform(-450,450),rnd.uniform(300,800),rnd.uniform(-30,-5)),rnd.uniform(25,55),cl,sub=3,sc=(2.4,1.4,0.3))
 bark=M('bark',(0.2,0.12,0.06),0.9);pine=M('pine',(0.08,0.22,0.12),0.85,tex='noise',scale=4,bump=0.6)
 for i in range(30):x=rnd.uniform(-90,90);y=rnd.uniform(50,120);tree((x,y,0),rnd.uniform(2.5,4),bark,pine,'BACK','pine',seed=i)
 for x,y in((-26,20),(-34,30),(27,22),(36,34),(-44,48),(46,52)):tree((x,y,0),2.2,bark,pine,'GROUND','pine',seed=x)
 # cáp treo: dây cáp và cabin
 steel=M('steel',(0.6,0.6,0.62),0.3,metal=1);cab=M('cab',(0.85,0.2,0.15),0.4)
 import bmesh
 for dx in(0,2.5):
  bpy.ops.curve.primitive_bezier_curve_add();cu=bpy.context.object;sp=cu.data.splines[0];p=sp.bezier_points
  p[0].co=(-300+dx,400,140);p[0].handle_left=p[0].co;p[0].handle_right=(-100+dx,300,60);p[1].co=(250+dx,180,40);p[1].handle_right=p[1].co;p[1].handle_left=(60+dx,260,55)
  cu.data.bevel_depth=0.15;link(setm(cu,steel))
 for t in(0.3,0.62):
  x=-300+550*t;y=400-220*t;z=140-100*t-25*math.sin(math.pi*t)
  box((x,y,z-3),(3,2.4,2.6),cab,bev=0.3);cyl((x,y,z-1.7),0.06,1.7,steel,v=6)
 render(sc,'bana')
def hoian():
 sc=reset();sky(sc,elev=4,rot=250,dust=3,air=1.2,strength=0.6);camera(sc)
 st=M('st',(0.45,0.4,0.33),0.75,tex='brick',scale=0.6,col2=(0.38,0.33,0.28),bump=0.3);ground_plane(st)
 wall=M('wall',(0.85,0.62,0.2),0.85,tex='noise',scale=1.2,bump=0.25);tile=M('tile',(0.28,0.13,0.08),0.7,tex='noise',scale=5,bump=0.6)
 wood=M('wood',(0.3,0.15,0.07),0.6);dark=M('dk',(0.05,0.04,0.03),0.8)
 lamps=[M('l1',(0.9,0.2,0.1),0.5,emit=(1,0.25,0.08),es=4),M('l2',(1,0.7,0.2),0.5,emit=(1,0.6,0.15),es=4),M('l3',(0.9,0.1,0.3),0.5,emit=(1,0.15,0.3),es=4)]
 rnd=random.Random(5)
 # hai dãy nhà phố cổ (hai bên), sông Thu Bồn ở giữa phía xa
 for side in(-1,1):
  x=side*24
  for j in range(9):
   y=18+j*9.5;w=rnd.uniform(7,9);h=rnd.uniform(5,7)
   bx=side*(16+w/2+rnd.uniform(0,2));box((bx,y,h/2),(w,8.6,h),wall,col='GROUND' if y<50 else 'BACK')
   roof((bx,y,h),8.6,w,2.2,tile,col='GROUND' if y<50 else 'BACK',curl=0.1,over=0.7).rotation_euler=(0,0,math.pi/2)
   for k in(-1,1):box((bx-side*w/2-0.02,y+k*2.3,1.6),(0.1,1.6,3.0),wood,col='GROUND' if y<50 else 'BACK')
   for k in range(3):
    lp=sph((bx-side*(w/2+0.9),y-2.5+k*2.5,h-0.6),0.42,lamps[(j+k)%3],'GROUND' if y<50 else 'BACK',sub=2,sc=(1,1,1.25))
 # dây đèn lồng ngang phố
 for y in(24,40,58):
  for i in range(9):x=-12+i*3;z=6.5-0.8*math.sin(math.pi*i/8);sph((x,y,z),0.38,lamps[i%3],'GROUND' if y<50 else 'BACK',sub=2,sc=(1,1,1.25))
 water((0,140,-0.2),(400,60),col=(0.04,0.12,0.12))
 # Chùa Cầu: cầu gỗ có mái, nằm ngang cuối phố
 cy=110;box((0,cy,1.2),(18,6,0.6),M('bridge',(0.5,0.25,0.12),0.6));
 for x in(-8,-4,0,4,8):
  for s in(-1,1):cyl((x,cy+s*2.6,1.5),0.22,4,wood,v=10)
 box((0,cy,0.4),(20,6.4,0.8),M('pier',(0.55,0.52,0.48),0.9,tex='brick',scale=0.7,col2=(0.45,0.42,0.38)))
 roof((0,cy,5.4),18,5.6,2.4,tile,curl=0.35,over=0.9);box((0,cy,5.6),(6,3.2,2.0),wall);roof((0,cy,7.6),6,3.2,1.6,tile,curl=0.4,over=0.6)
 for s in(-1,1):sph((s*3.5,cy-3.4,4.6),0.45,lamps[1],sub=2,sc=(1,1,1.25))
 # cây và thuyền
 leaf=M('leaf',(0.1,0.25,0.08),0.8,tex='noise',scale=3,bump=0.5);bark=M('bark',(0.2,0.12,0.06),0.9)
 for i in range(14):tree((rnd.uniform(-80,80),rnd.uniform(118,150),0),rnd.uniform(1.6,2.4),bark,leaf,seed=i)
 for i in range(4):
  b=sph((rnd.uniform(-30,30),rnd.uniform(125,140),0.1),1,M('boat%d'%i,(0.15,0.12,0.1),0.7),sub=2,sc=(3.2,1.0,0.5));sph((b.location.x+1.4,b.location.y-1.1,0.5),0.3,lamps[i%3],sub=1)
 l=bpy.data.lights.new('pt','POINT');l.energy=8000;l.color=(1,0.6,0.3);lo=bpy.data.objects.new('pt',l);sc.collection.objects.link(lo);lo.location=(0,30,9)
 render(sc,'hoian')
def myson():
 sc=reset();sky(sc,elev=9,rot=210,dust=2,air=1.3);camera(sc)
 earth=M('earth',(0.33,0.26,0.17),0.9,tex='noise',scale=0.8,bump=0.5);ground_plane(earth)
 grass=M('grass',(0.2,0.32,0.1),0.9,tex='noise',scale=1.2,bump=0.4);terrain((0,50,-0.25),(150,100),0.8,grass,'GROUND',seed=9,falloff=False)
 brick=M('cham',(0.55,0.24,0.13),0.85,tex='brick',scale=1.6,col2=(0.42,0.18,0.1),bump=0.7)
 moss=M('moss',(0.3,0.3,0.15),0.9,tex='noise',scale=2,bump=0.6)
 def kalan(x,y,s,col='BACK'):
  # tháp Chăm: thân vuông, trụ áp tường, các tầng thu nhỏ dần, chóp
  box((x,y,0.4*s),(7.4*s,7.4*s,0.8*s),moss,col=col)
  box((x,y,4.6*s),(6*s,6*s,7.6*s),brick,col=col,bev=0.05*s)
  for k in(-1,0,1):
   for d in((1,0),(0,1),(-1,0),(0,-1)):box((x+d[0]*3.05*s+d[1]*k*1.9*s,y+d[1]*3.05*s+d[0]*k*1.9*s,4.6*s),(0.55*s if d[0] else 0.8*s,0.55*s if d[1] else 0.8*s,7.6*s),brick,col=col)
  box((x,y-3.4*s,3.2*s),(2.6*s,1.4*s,5.2*s),brick,col=col);box((x,y-4.1*s,2.4*s),(1.2*s,0.2*s,3.6*s),M('door',(0.03,0.02,0.02),1),col=col)
  z=8.4*s
  for i,w in enumerate((5.6,4.4,3.3,2.3)):
   box((x,y,z+0.9*s),(w*s,w*s,1.8*s),brick,col=col,bev=0.04*s);z+=1.8*s
   for d in((1,1),(1,-1),(-1,1),(-1,-1)):box((x+d[0]*w*0.45*s,y+d[1]*w*0.45*s,z+0.3*s),(0.6*s,0.6*s,0.8*s),brick,col=col)
  cyl((x,y,z),1.0*s,2.6*s,brick,col=col,r2=0.25*s,v=12)
 kalan(0,95,1.6);kalan(-26,110,1.1);kalan(24,104,1.2);kalan(-48,130,0.9);kalan(52,135,0.85)
 # phế tích đổ nát phía trước
 rnd=random.Random(3)
 for i in range(10):x=rnd.uniform(-30,30);y=rnd.uniform(28,60);box((x,y,0.4),(rnd.uniform(0.8,2.4),rnd.uniform(0.6,1.6),rnd.uniform(0.5,1.4)),brick,rot=(0,0,rnd.random()),col='GROUND')
 for x in(-14,14):kalan(x,52,0.32,'GROUND')
 hill=M('hill',(0.12,0.26,0.12),0.9,tex='noise',scale=0.05,bump=0.3,col2=(0.06,0.14,0.07))
 peak((0,520,-20),220,240,hill,seed=21);peak((-260,420,-20),220,150,hill,seed=22);peak((260,460,-20),230,170,hill,seed=23)
 leaf=M('leaf',(0.1,0.28,0.08),0.8,tex='noise',scale=3,bump=0.5);bark=M('bark',(0.2,0.12,0.06),0.9)
 for i in range(60):tree((rnd.uniform(-160,160),rnd.uniform(120,220),0),rnd.uniform(2.5,4.5),bark,leaf,seed=i)
 for x,y in((-30,22),(-40,36),(32,24),(42,40),(-52,58),(55,62)):tree((x,y,0),1.9,bark,leaf,'GROUND',seed=x)
 render(sc,'myson')
def culaocham():
 sc=reset();sky(sc,elev=18,rot=130,dust=1,air=1);camera(sc)
 sand=M('sand',(0.82,0.72,0.52),0.9,tex='noise',scale=1.5,bump=0.25);ground_plane(sand,z=0)
 water((0,170,-0.4),(1600,240),col=(0.02,0.25,0.32))
 wet=M('wet',(0.55,0.48,0.36),0.3);box((0,60,-0.05),(320,12,0.1),wet,col='GROUND')
 isl=M('isl',(0.13,0.3,0.12),0.9,tex='noise',scale=0.04,bump=0.3,col2=(0.07,0.17,0.07));rk=M('rk',(0.35,0.33,0.3),0.9,tex='noise',scale=0.5,bump=0.9)
 peak((-140,330,-30),140,120,isl,seed=31);peak((120,420,-30),190,150,isl,seed=32);peak((-20,600,-30),180,90,isl,seed=33);peak((330,520,-30),160,110,isl,seed=34)
 rnd=random.Random(4)
 for i in range(14):x=rnd.choice([-1,1])*rnd.uniform(18,60);y=rnd.uniform(30,70);sph((x,y,0),rnd.uniform(0.8,2.6),rk,'GROUND',sub=2,sc=(1.3,1,0.7))
 for i in range(8):sph((rnd.uniform(-200,200),rnd.uniform(110,240),0),rnd.uniform(3,8),rk,sub=2,sc=(1.3,1,0.8))
 bark=M('bark',(0.35,0.25,0.15),0.9);palm=M('palm',(0.15,0.4,0.12),0.7)
 for x,y in((-30,28),(-40,44),(33,30),(44,48),(-60,58),(64,62)):tree((x,y,0),1.3,bark,palm,'GROUND','palm',seed=x)
 # thuyền thúng và thuyền đánh cá
 bt=M('basket',(0.3,0.2,0.1),0.8,tex='noise',scale=8,bump=0.6);hull=M('hull',(0.08,0.3,0.55),0.5);red=M('red',(0.7,0.08,0.05),0.6)
 for x,y in((-16,40),(-11,47),(15,44)):
  bpy.ops.mesh.primitive_uv_sphere_add(radius=1.3,location=(x,y,0.5));o=bpy.context.object;o.scale=(1,1,0.45);bpy.ops.object.shade_smooth();bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='DESELECT');bpy.ops.object.mode_set(mode='OBJECT')
  for v in o.data.vertices:
   if v.co.z>0:v.select=True
  bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.delete(type='VERT');bpy.ops.object.mode_set(mode='OBJECT');o.modifiers.new('s','SOLIDIFY').thickness=0.08;link(setm(o,bt),'GROUND')
 for i,(x,y) in enumerate(((-60,120),(40,140),(110,170))):
  sph((x,y,0.4),1,hull,sub=2,sc=(5,1.4,0.9));box((x,y,1.4),(4,2.2,0.3),red);cyl((x,y,1.4),0.08,5,bark,v=6)
 render(sc,'culaocham')
for w in WHICH:
 sc_,VAR=w.split(':');globals()[sc_]()
