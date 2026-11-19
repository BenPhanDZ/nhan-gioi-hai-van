# Dựng 5 thần thú pháp tướng trong Blender (Skin + Subdivision + nguyên khối), xuất glTF
# Toạ độ viết theo hệ three.js (x phải, y lên, z hướng camera), đơn vị = chiều cao chuẩn S của tướng.
import bpy,bmesh,math,sys,os
from mathutils import Vector,Matrix,Euler
TARGET=12000
OUT=sys.argv[sys.argv.index('--')+1]
C=Matrix(((1,0,0,0),(0,0,-1,0),(0,1,0,0),(0,0,0,1)))  # three -> blender
def cv(p):return (C@Vector((p[0],p[1],p[2],1))).to_3d()
def clear():
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete()
 for b in (bpy.data.meshes,bpy.data.materials,bpy.data.curves):
  for x in list(b):b.remove(x)
 MATS.clear()
MATS={}
def mat(n):
 if n not in MATS:
  m=bpy.data.materials.new(n);m.use_nodes=True;MATS[n]=m
 return MATS[n]
PARTS={}
def add(node,o,m):o.data.materials.clear();o.data.materials.append(mat(m));PARTS.setdefault(node,[]).append(o)
# --- ống/chi có bán kính thay đổi: Skin modifier trên chuỗi đỉnh (Catmull-Rom) ---
def crm(P,t):
 n=len(P)-1;f=t*n;i=min(int(f),n-1);u=f-i
 p0=Vector(P[max(i-1,0)]);p1=Vector(P[i]);p2=Vector(P[i+1]);p3=Vector(P[min(i+2,n)])
 return 0.5*((2*p1)+(-p0+p2)*u+(2*p0-5*p1+4*p2-p3)*u*u+(-p0+3*p1-3*p2+p3)*u*u*u)
def limb(node,P,rf,m='M',n=None,sub=2):
 n=n or max(6,len(P)*4)
 if rf(0.5)<0.05:sub=1
 me=bpy.data.meshes.new('l');bm=bmesh.new();vs=[]
 for i in range(n+1):
  t=i/n;vs.append(bm.verts.new(cv(crm(P,t))))
 for i in range(n):bm.edges.new((vs[i],vs[i+1]))
 bm.to_mesh(me);bm.free();o=bpy.data.objects.new('l',me);bpy.context.collection.objects.link(o)
 sk=o.modifiers.new('sk','SKIN');o.modifiers.new('ss','SUBSURF').levels=sub
 for i,d in enumerate(me.skin_vertices[0].data):r=rf(i/n);d.radius=(r,r)
 me.skin_vertices[0].data[0].use_root=True
 add(node,o,m);return o
def ell(node,c,r,rot=(0,0,0),m='M',seg=24):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=max(8,seg*2//3),radius=1);o=bpy.context.object
 o.matrix_world=C@Matrix.Translation(Vector(c))@Euler(rot,'XYZ').to_matrix().to_4x4()@Matrix.Diagonal((r[0],r[1],r[2],1))
 bpy.ops.object.shade_smooth();add(node,o,m);return o
def cone(node,base,d,r,h,m='E',seg=10):
 bpy.ops.mesh.primitive_cone_add(vertices=seg,radius1=r,radius2=0,depth=h);o=bpy.context.object
 dv=Vector(d).normalized();q=Vector((0,1,0)).rotation_difference(dv)
 o.matrix_world=C@Matrix.Translation(Vector(base))@q.to_matrix().to_4x4()@Matrix.Translation((0,h/2,0))@Matrix.Rotation(-math.pi/2,4,'X')
 bpy.ops.object.shade_smooth();add(node,o,m);return o
def cyl(node,c,r1,r2,h,m='E'):
 bpy.ops.mesh.primitive_cone_add(vertices=14,radius1=r2,radius2=r1,depth=h);o=bpy.context.object
 o.matrix_world=C@Matrix.Translation(Vector(c))@Matrix.Rotation(-math.pi/2,4,'X');add(node,o,m);return o
def feather(node,root,ang,L,W,m='M',z=0,tilt=0):
 # lông vũ: khối elip dẹt dài, gốc tại root, hướng góc ang trong mặt phẳng XY
 c=(root[0]+math.cos(ang)*L/2,root[1]+math.sin(ang)*L/2,root[2]+z)
 return ell(node,c,(L/2,W,0.014),(tilt,0,ang),m,14)
def finish(name,tree,piv):
 # gộp các phần theo node, đặt gốc ở trục xoay, dựng cây cha-con
 objs={}
 for node,parts in PARTS.items():
  bpy.ops.object.select_all(action='DESELECT')
  for o in parts:
   o.select_set(True);bpy.context.view_layer.objects.active=o
   if o.modifiers:
    for md in list(o.modifiers):bpy.ops.object.modifier_apply(modifier=md.name)
  bpy.ops.object.select_all(action='DESELECT')
  for o in parts:o.select_set(True)
  bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();o=bpy.context.object;o.name=node;o.data.name=node
  bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
  bpy.ops.object.shade_smooth()
  bpy.context.scene.cursor.location=cv(piv.get(node,(0,0,0)));bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
  objs[node]=o
 for ch,pa in tree.items():
  if ch in objs and pa in objs:
   c=objs[ch];mw=c.matrix_world.copy();c.parent=objs[pa];c.matrix_world=mw
 tris=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in objs.values());print('RAW',name,tris);r=min(1,TARGET/max(1,tris))
 if r<1:
  for o in objs.values():
   bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
   d=o.modifiers.new('dc','DECIMATE');d.ratio=r;bpy.ops.object.modifier_apply(modifier='dc')
 bpy.ops.object.select_all(action='SELECT')
 tris=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in objs.values())
 bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,name+'.glb'),export_format='GLB',export_materials='EXPORT',export_normals=True,export_texcoords=False,export_apply=True,export_yup=True,export_animations=False)
 print('EXPORT',name,tris)
 PARTS.clear()

def tiger():
 limb('body',[(0,-0.3,-0.4),(0,-0.05,-0.25),(0,0.2,-0.08),(0,0.45,0.0)],lambda t:0.26+0.12*math.sin(math.pi*min(1,t*1.3)),n=14)
 for s in(-1,1):
  limb('body',[(0,0.22,-0.05),(s*0.34,0.2,0.0),(s*0.56,-0.05,0.2),(s*0.6,-0.42,0.34),(s*0.6,-0.5,0.42)],lambda t:0.2-0.1*t,n=16)
  ell('body',(s*0.6,-0.52,0.46),(0.13,0.07,0.14))
  for k in range(4):cone('glow',(s*0.6+(k-1.5)*0.055,-0.55,0.55),((k-1.5)*0.2,-0.5,1),0.022,0.11)
  for k in range(4):ell('body',(s*(0.6+(k-1.5)*0.055),-0.53,0.57),(0.032,0.03,0.04))
 # đầu
 H=(0,0.64,0.05)
 def hp(p):return (H[0]+p[0],H[1]+p[1],H[2]+p[2])
 ell('head',hp((0,0,0)),(0.29,0.25,0.27))
 limb('head',[hp((0,-0.04,0.06)),hp((0,-0.08,0.2)),hp((0,-0.05,0.31))],lambda t:0.16-0.08*t,n=8)
 ell('head',hp((0,-0.02,0.355)),(0.065,0.04,0.04))
 for s in(-1,1):
  limb('head',[hp((s*0.15,0.14,-0.02)),hp((s*0.2,0.23,-0.03)),hp((s*0.22,0.28,-0.04))],lambda t:0.07-0.04*t,n=6)
  for k in range(5):limb('head',[hp((s*0.2,-0.02-k*0.045,0.02)),hp((s*(0.33+0.02*(2-abs(k-2))),-0.1-k*0.05,-0.02)),hp((s*(0.42-abs(k-2)*0.03),-0.18-k*0.05,-0.06))],lambda t:0.07*(1-t)+0.01,n=6)
  ell('head',hp((s*0.11,0.1,0.22)),(0.1,0.03,0.04),(0,0,s*-0.35))
  ell('eye',hp((s*0.105,0.045,0.235)),(0.045,0.022,0.02),(0,0,s*0.3))
  cone('glow',hp((s*0.065,-0.11,0.3)),(0,-1,0.1),0.022,0.12)
 J=(0,-0.15,0.1)
 limb('jaw',[hp((0,-0.15,0.08)),hp((0,-0.17,0.2)),hp((0,-0.17,0.28))],lambda t:0.1-0.04*t,n=8)
 for s in(-1,1):cone('glow',hp((s*0.06,-0.15,0.26)),(0,1,0.1),0.018,0.09)
 finish('phap_kim',{'head':'body','jaw':'head','eye':'head','glow':'body'},{'body':(0,0,0),'head':H,'jaw':hp(J),'eye':H,'glow':(0,0,0)})

def dragon():
 P=[(0.62,-0.85,-0.3),(-0.55,-0.55,-0.05),(0.55,-0.12,0.05),(-0.5,0.32,-0.12),(0.12,0.72,0.02),(0.18,0.9,0.12)]
 rf=lambda t:0.025+0.11*math.sin(math.pi*min(1,t*1.15+0.05))*((1-(t-0.85)*2.5) if t>0.85 else 1)
 limb('body',P,rf,n=60,sub=1)
 for i in range(3,58,2):
  t=i/60;p=crm(P,t);q=crm(P,min(1,t+0.01));tg=(q-p).normalized();up=tg.cross(Vector((0,0,1))).cross(tg).normalized()
  if up.y<0:up=-up
  cone('glow',tuple(p+up*rf(t)*0.85),tuple(up-tg*0.5),0.02,0.04+0.07*math.sin(math.pi*t),seg=6)
 for t in(0.32,0.58):
  p=crm(P,t)
  for s in(-1,1):
   a=p+Vector((s*0.06,0,0.05));e=a+Vector((s*0.16,-0.08,0.08))
   limb('body',[tuple(a),tuple((a+e)/2+Vector((0,0.03,0))),tuple(e)],lambda u:0.045-0.02*u,n=6)
   for k in(-1,0,1):cone('glow',tuple(e),(s*0.6+k*0.3,-0.6,0.5+k*0.2),0.012,0.07,seg=5)
 H=tuple(crm(P,1.0))
 def hp(p):return (H[0]+p[0],H[1]+p[1],H[2]+p[2])
 ell('head',hp((0,0,0)),(0.14,0.12,0.16))
 limb('head',[hp((0,0,0.06)),hp((0,-0.01,0.18)),hp((0,0.0,0.3))],lambda t:0.1-0.04*t,n=8)
 ell('head',hp((0,0.035,0.33)),(0.05,0.03,0.035))
 for s in(-1,1):
  ell('head',hp((s*0.08,0.08,0.08)),(0.07,0.03,0.05),(0.3,0,s*-0.4))
  limb('glow',[hp((s*0.07,0.1,-0.02)),hp((s*0.14,0.22,-0.14)),hp((s*0.12,0.3,-0.3)),hp((s*0.18,0.34,-0.42))],lambda u:0.025-0.018*u,n=10)
  limb('glow',[hp((s*0.08,0.0,0.3)),hp((s*0.3,-0.05,0.32)),hp((s*0.45,-0.2,0.2)),hp((s*0.55,-0.32,0.0))],lambda u:0.008*(1-u*0.6),n=14,sub=1)
  for k in range(5):cone('head',hp((s*0.1,0.02-k*0.04,-0.06)),(s*0.6,0.2-k*0.2,-1),0.035,0.2,m='M',seg=6)
  cone('glow',hp((s*0.05,-0.06,0.28)),(0,-1,0),0.015,0.06,seg=5)
  ell('eye',hp((s*0.085,0.05,0.12)),(0.03,0.016,0.016),(0,0,s*0.3))
 limb('jaw',[hp((0,-0.08,0.04)),hp((0,-0.1,0.16)),hp((0,-0.1,0.27))],lambda t:0.07-0.03*t,n=8)
 for k in(-1,0,1):limb('jaw',[hp((k*0.04,-0.11,0.12)),hp((k*0.06,-0.21,0.07)),hp((k*0.05,-0.31,0.1))],lambda u:0.013*(1-u)+0.003,n=6,sub=1)
 finish('phap_moc',{'head':'body','jaw':'head','eye':'head','glow':'body'},{'body':(0,0,0),'head':H,'jaw':hp((0,-0.07,0.05)),'eye':H,'glow':(0,0,0)})

def phoenix():
 ell('body',(0,0.2,0),(0.14,0.3,0.14),(0.2,0,0))
 limb('body',[(0,0.4,0.02),(0,0.56,-0.04),(0,0.68,0.04),(0,0.75,0.1)],lambda u:0.075-0.035*u,n=10)
 H=(0,0.77,0.12)
 def hp(p):return (H[0]+p[0],H[1]+p[1],H[2]+p[2])
 ell('head',H,(0.08,0.075,0.09))
 cone('glow',hp((0,-0.01,0.06)),(0,-0.25,1),0.03,0.13)
 for s in(-1,1):ell('eye',hp((s*0.05,0.02,0.05)),(0.018,0.012,0.012))
 for k in(-1,0,1):
  limb('glow',[hp((k*0.02,0.06,-0.02)),hp((k*0.06,0.18,-0.08)),hp((k*0.1,0.28,-0.04+abs(k)*0.04))],lambda u:0.013*(1-u*0.5),n=8)
  ell('glow',hp((k*0.1,0.29,-0.04+abs(k)*0.04)),(0.026,0.026,0.026),seg=12)
 for k in range(-2,3):
  e=(k*0.28,-0.95,-0.15+abs(k)*0.05)
  limb('body',[(k*0.02,0.0,-0.04),(k*0.1,-0.35,-0.12),(k*0.24,-0.7,-0.1),e],lambda u:0.035-0.02*u,n=14)
  ell('glow',(e[0],e[1]-0.04,e[2]+0.005),(0.05,0.07,0.02),seg=14);ell('body',(e[0],e[1]-0.04,e[2]-0.01),(0.08,0.11,0.025),seg=16)
 for s,nm in((-1,'wingL'),(1,'wingR')):
  A=[(s*0.1,0.36,-0.04),(s*0.36,0.5,-0.04),(s*0.6,0.68,-0.06),(s*0.8,0.84,-0.08)]
  limb(nm,A,lambda u:0.045-0.03*u,n=10)
  for i in range(13):
   u=i/12;p=crm(A,u);L=0.3+0.38*u**1.3;a=-1.6+u*1.75
   if s<0:a=math.pi-a
   feather(nm,tuple(p),a,L,0.045+0.02*u,m=('glow' if i%2 else nm),z=-i*0.003)
  for i in range(8):
   u=i/7;p=crm(A,u*0.8);a=-1.5+u*0.6
   if s<0:a=math.pi-a
   feather(nm,tuple(p),a,0.16+0.08*u,0.05,m='glow',z=0.02)
 # đưa lông sáng của cánh vào chính node cánh để cùng vỗ
 for nm in('wingL','wingR'):
  for o in list(PARTS.get('glow',[])):
   pass
 finish('phap_hoa',{'head':'body','eye':'head','wingL':'body','wingR':'body','glow':'body'},{'body':(0,0,0),'head':H,'eye':H,'wingL':(-0.1,0.36,-0.04),'wingR':(0.1,0.36,-0.04),'glow':(0,0,0)})

def turtle():
 B=(0,-0.5,0)
 ell('body',(0,-0.42,0),(0.62,0.34,0.5),seg=32);ell('body',(0,-0.62,0.02),(0.6,0.12,0.48))
 for i in range(7):
  a=i/6*math.pi*2;r=0.33 if i<6 else 0
  bpy.ops.mesh.primitive_cylinder_add(vertices=6,radius=0.15,depth=0.05);o=bpy.context.object
  o.matrix_world=C@Matrix.Translation((math.cos(a)*r,-0.5+0.36-r*0.32,math.sin(a)*r*0.8))@Euler((math.sin(a)*0.45 if r else 0,0,-math.cos(a)*0.45 if r else 0),'XYZ').to_matrix().to_4x4()@Matrix.Rotation(-math.pi/2,4,'X')
  bm=o.modifiers.new('b','BEVEL');bm.width=0.015;bm.segments=2;add('glow',o,'glow')
 for sx,sz in((-1,1),(1,1),(-1,-1),(1,-1)):limb('body',[(sx*0.4,-0.6,sz*0.25),(sx*0.58,-0.66,sz*0.36)],lambda u:0.11-0.03*u,n=4)
 limb('body',[(0,-0.55,0.4),(0,-0.5,0.58)],lambda u:0.11-0.02*u,n=4)
 for s in(-1,1):ell('eye',(s*0.06,-0.46,0.66),(0.022,0.014,0.014))
 sp=[]
 for i in range(9):
  a=math.pi*1.1+i/8*math.pi*1.6;sp.append((math.cos(a)*0.68,-0.38+math.sin(i*0.9)*0.06,math.sin(a)*0.56))
 sp+= [(0.55,-0.05,-0.15),(0.2,0.35,-0.2),(0.32,0.68,-0.05),(0.15,0.9,0.08)]
 limb('body',sp,lambda t:0.03+0.055*math.sin(math.pi*min(1,t*1.1+0.04)),n=70,sub=1)
 H=sp[-1]
 def hp(p):return (H[0]+p[0],H[1]+p[1],H[2]+p[2])
 limb('head',[hp((0,0,-0.04)),hp((0,0.01,0.06)),hp((0,0.0,0.16))],lambda u:0.09-0.03*u,n=8)
 for s in(-1,1):
  ell('eye',hp((s*0.06,0.04,0.09)),(0.02,0.012,0.012),(0,0,s*0.3))
  cone('glow',hp((s*0.04,-0.02,0.14)),(0,-1,0.2),0.014,0.07,seg=5)
  ell('head',hp((s*0.06,0.06,0.0)),(0.06,0.025,0.06),(0.2,0,s*-0.3))
 limb('jaw',[hp((0,-0.05,0.0)),hp((0,-0.06,0.12)),hp((0,-0.05,0.18))],lambda u:0.06-0.03*u,n=6)
 limb('jaw',[hp((0,-0.05,0.18)),hp((0,-0.06,0.26)),hp((0.02,-0.04,0.32))],lambda u:0.008,n=6,sub=1)
 finish('phap_thuy',{'head':'body','jaw':'head','eye':'body','glow':'body'},{'body':(0,0,0),'head':H,'jaw':hp((0,-0.04,0)),'eye':(0,0,0),'glow':(0,0,0)})

def qilin():
 Y=-0.1
 ell('body',(0,-0.15,-0.1),(0.36,0.42,0.3))
 N=[(0,0.1,-0.06),(0,0.32,-0.02),(0,0.48,0.04)]
 limb('body',N,lambda u:0.18-0.06*u,n=10)
 H=(0,0.58,0.08)
 def hp(p):return (H[0]+p[0],H[1]+p[1],H[2]+p[2])
 ell('head',H,(0.16,0.14,0.17))
 limb('head',[hp((0,-0.03,0.08)),hp((0,-0.04,0.22)),hp((0,-0.02,0.36))],lambda u:0.11-0.03*u,n=8)
 limb('glow',[hp((0,0.12,0.02)),hp((0,0.26,-0.04)),hp((0,0.38,-0.16)),hp((0,0.42,-0.3))],lambda u:0.035-0.03*u,n=12)
 for s in(-1,1):
  ell('head',hp((s*0.09,0.09,0.1)),(0.07,0.03,0.06),(0.3,0,s*-0.35))
  cone('head',hp((s*0.11,0.08,-0.06)),(s*0.8,0.6,-0.4),0.04,0.12,m='M',seg=8)
  limb('glow',[hp((s*0.07,-0.02,0.34)),hp((s*0.22,-0.02,0.36)),hp((s*0.34,-0.14,0.26))],lambda u:0.008*(1-u*0.6),n=8,sub=1)
  ell('eye',hp((s*0.1,0.04,0.13)),(0.03,0.016,0.016),(0,0,s*0.3))
 for i in range(5):cone('head',hp((0,0.1-i*0.05,-0.12)),(0,0.4,-1),0.045,0.22,m='glow',seg=7)
 for i in range(10):
  p=crm(N,i/9);cone('glow',(0,p.y,p.z-0.12),(0,0.5+i*0.05,-1),0.05,0.18+0.1*math.sin(math.pi*i/9),seg=7)
 limb('jaw',[hp((0,-0.1,0.06)),hp((0,-0.11,0.18)),hp((0,-0.1,0.3))],lambda u:0.075-0.03*u,n=8)
 for k in(-1,0,1):cone('jaw',hp((k*0.05,-0.13,0.14)),(k*0.3,-1,0.4),0.03,0.18,m='glow',seg=7)
 for s in(-1,1):
  limb('body',[(s*0.26,0.0,0.06),(s*0.42,-0.1,0.36),(s*0.36,-0.42,0.42)],lambda u:0.1-0.055*u,n=10)
  cyl('glow',(s*0.36,-0.47,0.42),0.05,0.065,0.08)
  for k in range(3):cone('glow',(s*0.42,-0.05-k*0.06,0.32),(s,0.2,-0.4),0.03,0.12,seg=6)
 for (a,b,c) in((-0.45,-0.8,0.1),(0.4,-0.85,0.15),(0,-0.92,0.3),(-0.15,-0.78,-0.25),(0.25,-0.75,-0.2)):
  ell('glow',(a,b,c),(0.22,0.08,0.14));ell('body',(a+0.12,b+0.04,c),(0.14,0.1,0.1))
 finish('phap_tho',{'head':'body','jaw':'head','eye':'head','glow':'body'},{'body':(0,0,0),'head':H,'jaw':hp((0,-0.09,0.06)),'eye':H,'glow':(0,0,0)})

for f in(tiger,dragon,phoenix,turtle,qilin):
 clear();f()
