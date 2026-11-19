# xem trước: nạp glb, xếp lưới các node gốc, render Workbench/Cycles
import bpy,sys,math
a=sys.argv[sys.argv.index('--')+1:];src,out=a[0],a[1];cols=int(a[2]) if len(a)>2 else 6;gap=float(a[3]) if len(a)>3 else 0.5;eng=a[4] if len(a)>4 else 'WB'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete()
bpy.ops.import_scene.gltf(filepath=src)
roots=[o for o in bpy.context.scene.objects if o.parent is None]
roots.sort(key=lambda o:o.name)
for i,o in enumerate(roots):o.location=(o.location.x+(i%cols)*gap,o.location.y,o.location.z-(i//cols)*gap*2.2)
rows=(len(roots)+cols-1)//cols
cam=bpy.data.cameras.new('c');cam.type='ORTHO';cam.ortho_scale=max(cols*gap,rows*gap*2.2)*1.05
co=bpy.data.objects.new('c',cam);bpy.context.collection.objects.link(co);co.location=((cols-1)*gap/2,-5,-(rows-1)*gap*1.1);co.rotation_euler=(math.pi/2,0,0);bpy.context.scene.camera=co
sc=bpy.context.scene;sc.render.resolution_x=1600;sc.render.resolution_y=int(1600*rows*2.2/cols*0.98);sc.render.film_transparent=False
if eng=='WB':
 sc.render.engine='BLENDER_WORKBENCH';sc.display.shading.light='STUDIO';sc.display.shading.color_type='MATERIAL';sc.display.shading.show_cavity=True
else:
 sc.render.engine='CYCLES';sc.cycles.samples=32;sc.cycles.device='CPU'
 w=bpy.data.worlds.new('w');sc.world=w;w.use_nodes=True;w.node_tree.nodes['Background'].inputs[1].default_value=1.2
 l=bpy.data.lights.new('s','SUN');l.energy=4;lo=bpy.data.objects.new('s',l);bpy.context.collection.objects.link(lo);lo.rotation_euler=(0.8,0.3,0.4)
for i,o in enumerate(roots):
 t=bpy.data.curves.new('t','FONT');t.body=o.name;t.size=0.06;to=bpy.data.objects.new('t',t);bpy.context.collection.objects.link(to);to.location=(o.location.x-0.15,0,o.location.z+0.35);to.rotation_euler=(math.pi/2,0,0)
sc.render.filepath=out;bpy.ops.render.render(write_still=True)
