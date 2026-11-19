# Thư viện dựng hình dùng chung cho các script Blender của game (toạ độ hệ three.js: x phải, y lên, z ra camera)
import bpy,bmesh,math
from mathutils import Vector,Matrix,Euler,Quaternion
C=Matrix(((1,0,0,0),(0,0,-1,0),(0,1,0,0),(0,0,0,1)))
def cv(p):return (C@Vector((p[0],p[1],p[2],1))).to_3d()
MATS={};PARTS={}
def clear():
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete()
 for b in (bpy.data.meshes,bpy.data.materials,bpy.data.curves):
  for x in list(b):b.remove(x)
 MATS.clear();PARTS.clear()
def mat(n,col=None,metal=0,rough=0.5,emit=None):
 if n not in MATS:
  m=bpy.data.materials.new(n);m.use_nodes=True;MATS[n]=m
  bs=m.node_tree.nodes.get('Principled BSDF')
  if bs and col:
   bs.inputs['Base Color'].default_value=(*col,1);bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough
   if emit:bs.inputs['Emission Color'].default_value=(*emit,1);bs.inputs['Emission Strength'].default_value=2
 return MATS[n]
def add(node,o,m):
 o.data.materials.clear();o.data.materials.append(mat(m));PARTS.setdefault(node,[]).append(o);return o
def obj_from_bm(bm,node,m,smooth=True):
 me=bpy.data.meshes.new('m');bm.to_mesh(me);bm.free();o=bpy.data.objects.new('m',me);bpy.context.collection.objects.link(o)
 for p in me.polygons:p.use_smooth=smooth
 return add(node,o,m)
def crm(P,t):
 n=len(P)-1;f=t*n;i=min(int(f),n-1);u=f-i
 p0=Vector(P[max(i-1,0)]);p1=Vector(P[i]);p2=Vector(P[i+1]);p3=Vector(P[min(i+2,n)])
 return 0.5*((2*p1)+(-p0+p2)*u+(2*p0-5*p1+4*p2-p3)*u*u+(-p0+3*p1-3*p2+p3)*u*u*u)
def limb(node,P,rf,m='M',n=None,sub=2):
 n=n or max(6,len(P)*4)
 if rf(0.5)<0.05:sub=1
 me=bpy.data.meshes.new('l');bm=bmesh.new();vs=[]
 for i in range(n+1):vs.append(bm.verts.new(cv(crm(P,i/n))))
 for i in range(n):bm.edges.new((vs[i],vs[i+1]))
 bm.to_mesh(me);bm.free();o=bpy.data.objects.new('l',me);bpy.context.collection.objects.link(o)
 o.modifiers.new('sk','SKIN');o.modifiers.new('ss','SUBSURF').levels=sub
 for i,d in enumerate(me.skin_vertices[0].data):r=rf(i/n);d.radius=(r,r)
 me.skin_vertices[0].data[0].use_root=True
 return add(node,o,m)
def ell(node,c,r,rot=(0,0,0),m='M',seg=24):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=max(8,seg*2//3),radius=1);o=bpy.context.object
 o.matrix_world=C@Matrix.Translation(Vector(c))@Euler(rot,'XYZ').to_matrix().to_4x4()@Matrix.Diagonal((r[0],r[1],r[2],1))
 bpy.ops.object.shade_smooth();return add(node,o,m)
def cone(node,base,d,r,h,m='E',seg=10):
 bpy.ops.mesh.primitive_cone_add(vertices=seg,radius1=r,radius2=0,depth=h);o=bpy.context.object
 dv=Vector(d).normalized();q=Vector((0,1,0)).rotation_difference(dv)
 o.matrix_world=C@Matrix.Translation(Vector(base))@q.to_matrix().to_4x4()@Matrix.Translation((0,h/2,0))@Matrix.Rotation(-math.pi/2,4,'X')
 bpy.ops.object.shade_smooth();return add(node,o,m)
def lathe(node,prof,m,seg=24,c=(0,0,0),d=(0,1,0),smooth=True,sx=1,sz=1):
 # prof: [(r,y)] quay quanh trục y (rồi hướng theo d, đặt tại c)
 bm=bmesh.new();rings=[]
 q=Vector((0,1,0)).rotation_difference(Vector(d).normalized());M=C@Matrix.Translation(Vector(c))@q.to_matrix().to_4x4()
 for r,y in prof:
  ring=[]
  for j in range(seg):
   a=j/seg*math.pi*2;ring.append(bm.verts.new((M@Vector((math.cos(a)*r*sx,y,math.sin(a)*r*sz,1))).to_3d()))
  rings.append(ring)
 for i in range(len(rings)-1):
  for j in range(seg):bm.faces.new((rings[i][j],rings[i][(j+1)%seg],rings[i+1][(j+1)%seg],rings[i+1][j]))
 if prof[0][0]>0:bm.faces.new(list(reversed(rings[0])))
 if prof[-1][0]>0:bm.faces.new(rings[-1])
 bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
 return obj_from_bm(bm,node,m,smooth)
def blade(node,L,wf,th,m='metal',n=24,xo=None,y0=0,single=False,c=(0,0,0),rot=(0,0,0),tipx=0):
 # lưỡi có sống và hai mép sắc: tiết diện hình thoi; xo(t): độ cong theo x; single: một lưỡi (đao)
 bm=bmesh.new();secs=[];M=C@Matrix.Translation(Vector(c))@Euler(rot,'XYZ').to_matrix().to_4x4()
 P=lambda x,y,z:bm.verts.new((M@Vector((x,y,z,1))).to_3d())
 for i in range(n):
  t=i/n;y=y0-t*L;w=wf(t);x0=xo(t) if xo else 0;tk=th*(1-0.6*t)
  if single:secs.append([P(x0-w*0.15,y,0),P(x0+w*0.1,y,tk),P(x0+w,y,0),P(x0+w*0.1,y,-tk)])
  else:secs.append([P(x0-w,y,0),P(x0,y,tk),P(x0+w,y,0),P(x0,y,-tk)])
 tip=P((xo(1) if xo else 0)+tipx,y0-L,0)
 for i in range(n-1):
  a,b=secs[i],secs[i+1]
  for j in range(4):bm.faces.new((a[j],a[(j+1)%4],b[(j+1)%4],b[j]))
 for j in range(4):bm.faces.new((secs[-1][j],secs[-1][(j+1)%4],tip))
 bm.faces.new(list(reversed(secs[0])))
 bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
 o=obj_from_bm(bm,node,m,False);md=o.modifiers.new('ew','EDGE_SPLIT');md.split_angle=0.6;return o
def box(node,c,s,m,rot=(0,0,0),bev=0.0):
 bpy.ops.mesh.primitive_cube_add(size=1);o=bpy.context.object
 o.matrix_world=C@Matrix.Translation(Vector(c))@Euler(rot,'XYZ').to_matrix().to_4x4()@Matrix.Diagonal((s[0],s[1],s[2],1))
 if bev:
  bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);b=o.modifiers.new('b','BEVEL');b.width=bev;b.segments=2
 return add(node,o,m)
def torus(node,c,R,r,m,rot=(0,0,0),arc=None,seg=32,mseg=8):
 bpy.ops.mesh.primitive_torus_add(major_radius=R,minor_radius=r,major_segments=seg,minor_segments=mseg);o=bpy.context.object
 o.matrix_world=C@Matrix.Translation(Vector(c))@Euler(rot,'XYZ').to_matrix().to_4x4()@Matrix.Rotation(math.pi/2,4,'X')
 bpy.ops.object.shade_smooth();return add(node,o,m)
def finish_nodes(tree,piv):
 objs={}
 for node,parts in PARTS.items():
  bpy.ops.object.select_all(action='DESELECT')
  for o in parts:
   o.select_set(True);bpy.context.view_layer.objects.active=o
   for md in list(o.modifiers):bpy.ops.object.modifier_apply(modifier=md.name)
   o.select_set(False)
  for o in parts:o.select_set(True)
  bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();o=bpy.context.object;o.name=node;o.data.name=node
  bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
  bpy.context.scene.cursor.location=cv(piv.get(node,(0,0,0)));bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
  objs[node]=o
 for ch,pa in tree.items():
  if ch in objs and pa in objs:
   c=objs[ch];mw=c.matrix_world.copy();c.parent=objs[pa];c.matrix_world=mw
 PARTS.clear();return objs
def tris(objs):return sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in objs)
def export(path,sel=None):
 bpy.ops.object.select_all(action='DESELECT')
 for o in (sel or bpy.context.scene.objects):o.select_set(True)
 bpy.ops.export_scene.gltf(filepath=path,export_format='GLB',use_selection=True,export_materials='EXPORT',export_normals=True,export_texcoords=False,export_apply=True,export_yup=True,export_animations=False)
