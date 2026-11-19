# Thần Binh riêng của tướng UR/SSS – mỗi món một node 'tb_<mã tướng>' + vòng phù văn 'tb_aura' dùng chung
import sys,os,math;sys.path.insert(0,os.path.dirname(__file__))
exec(open(os.path.join(os.path.dirname(__file__),'weapons.py')).read().split('W={}')[0])
def gem(n,c,r=0.02,m='gem'):ell(n,c,(r,r,r*0.6),m=m,seg=12)
def dragon_guard(n,y=-0.03,w=0.17):
 # chắn tay hình hai đầu rồng
 box(n,(0,y,0),(0.09,0.04,0.07),'gold',bev=0.012)
 for s in(-1,1):
  limb(n,[(0,y,0),(s*w*0.5,y+0.01,0),(s*w*0.85,y+0.04,0),(s*w,y+0.08,0)],lambda t:0.026-0.012*t,m='gold',n=10)
  ell(n,(s*w,y+0.095,0.0),(0.026,0.022,0.03),m='gold',seg=12);cone(n,(s*w,y+0.11,0),(s*0.4,1,-0.3),0.008,0.04,'gold',seg=6)
  gem(n,(s*w*1.02,y+0.1,0.022),0.006,'ec')
def leloi():
 n='tb_leloi';grip(n,0.0,0.2,r=0.023);pommel(n,0.22,0.03)
 torus(n,(0,0.27,0),0.03,0.008,'gold',rot=(0,math.pi/2,0))
 dragon_guard(n);gem(n,(0,-0.03,0.04),0.018)
 blade(n,0.82,lambda t:0.034*(1-0.2*t)+0.004,0.009,y0=-0.05)
 for s in(-1,1):box(n,(0,-0.33,s*0.0085),(0.006,0.5,0.002),'glow')
 for i in range(3):gem(n,(0,-0.1-i*0.05,0.009),0.006,'ec')
def giong():
 n='tb_giong';lathe(n,[(0,0.45),(0.03,0.44)]+[(0.03 if i%2 else 0.036,0.4-i*0.11) for i in range(14)]+[(0.034,-1.14),(0.045,-1.16),(0.02,-1.22),(0,-1.24)],'iron',seg=16)
 for y in(0.3,-0.2,-0.7,-1.1):torus(n,(0,y,0),0.042,0.01,'gold',rot=(math.pi/2,0,0))
 grip(n,-0.02,0.24,r=0.04)
def anduongvuong():
 n='tb_anduongvuong';box(n,(0,-0.1,0.22),(0.07,0.07,0.6),'bronze',bev=0.012)
 for z in(0.05,0.2,0.35,0.5):torus(n,(0,-0.1,z),0.05,0.008,'gold',rot=(0,0,0))
 box(n,(0,-0.02,-0.02),(0.06,0.18,0.08),'bronze',rot=(0.3,0,0),bev=0.012)
 P=[(-0.42,-0.1,0.4),(-0.2,-0.1,0.5),(0,-0.1,0.52),(0.2,-0.1,0.5),(0.42,-0.1,0.4)]
 limb(n,P,lambda t:0.02+0.014*math.sin(math.pi*t),m='bronze',n=24)
 for s in(-1,1):cone(n,(s*0.42,-0.1,0.4),(s,0,-0.5),0.018,0.06,'gold',seg=6)
 limb(n,[(-0.42,-0.1,0.4),(0,-0.1,0.16),(0.42,-0.1,0.4)],lambda t:0.004,m='string',n=4,sub=1)
 # lẫy móng rùa vàng
 for k in(-1,0,1):limb(n,[(k*0.018,-0.14,0.12),(k*0.026,-0.2,0.1),(k*0.022,-0.24,0.13)],lambda t:0.012*(1-t*0.6),m='goldglow',n=6)
 ell(n,(0,-0.13,0.12),(0.04,0.025,0.04),m='goldglow',seg=14)
 box(n,(0,-0.065,0.3),(0.012,0.012,0.36),'wood');cone(n,(0,-0.065,0.48),(0,0,1),0.016,0.06,'bronze',seg=6)
def kimquy():
 n='tb_kimquy';ell(n,(0,-0.02,0.03),(0.075,0.05,0.05),m='goldglow',seg=16)
 for i,x in enumerate((-0.05,0,0.05)):
  limb(n,[(x,-0.05,0.04),(x*1.3,-0.16,0.07),(x*1.4,-0.28,0.06),(x*1.2,-0.36,0.02)],lambda t:0.022*(1-t*0.75)+0.003,m='goldglow',n=12)
 for a in range(6):
  th=a/6*math.pi*2;ell(n,(math.cos(th)*0.045,-0.02+math.sin(th)*0.03,0.07),(0.018,0.014,0.006),m='jade',seg=8)
def ngoquyen():
 n='tb_ngoquyen';lathe(n,[(0,0.5),(0.04,0.49),(0.045,-0.6),(0.04,-0.62),(0,-0.63)],'wood',seg=14)
 lathe(n,[(0,-0.6),(0.05,-0.6),(0.048,-0.78),(0.03,-0.9),(0,-1.02)],'iron',seg=14)
 for y in(-0.58,-0.4,0.2):
  for k in range(4):torus(n,(0,y-k*0.016,0),0.048,0.006,'rope',rot=(math.pi/2,0,0),seg=20,mseg=5)
 for i in range(4):a=i/4*math.pi*2;cone(n,(math.cos(a)*0.04,-0.7,math.sin(a)*0.04),(math.cos(a),0.8,math.sin(a)),0.01,0.05,'iron',seg=5)
def tranquoctoan():
 n='tb_tranquoctoan';shaft(n,0.62,-0.82,r=0.022,m='redwood',rings=(0.55,0.0,-0.6))
 lathe(n,[(0,-0.8),(0.035,-0.82),(0.05,-0.86),(0.02,-0.94),(0,-1.0)],'gold',seg=12)
 torus(n,(0,-0.9,0),0.06,0.008,'gold',rot=(0,math.pi/2,0));tassel(n,-0.84,'yellow')
def chudongtu():
 n='tb_chudongtu';P=[(0,0.5,0),(0.01,0.2,0.01),(-0.01,-0.2,0),(0.015,-0.6,-0.01),(0,-0.9,0)]
 limb(n,P,lambda t:0.03-0.008*t+0.006*math.sin(t*30),m='oldwood',n=40)
 # nón thần trên đầu gậy
 lathe(n,[(0,-0.86),(0.02,-0.88),(0.16,-1.0),(0.17,-1.01),(0,-1.0)],'straw',seg=28,d=(0,1,0))
 torus(n,(0,-0.99,0),0.16,0.006,'gold',rot=(math.pi/2,0,0),seg=40)
 gem(n,(0,-0.86,0),0.03,'ec')
def hungdao():
 n='tb_hungdao';lathe(n,[(0,0.26),(0.035,0.25),(0.035,-0.25),(0,-0.26)],'gold',seg=16,c=(0,-0.08,0.06),d=(1,0,0))
 for s in(-1,1):limb(n,[(s*0.26,-0.08,0.06),(s*0.3,-0.08,0.06),(s*0.32,-0.05,0.06)],lambda t:0.02,m='gold',n=4)
 box(n,(0,-0.3,0.06),(0.46,0.42,0.004),'silk')
 for i in range(6):box(n,(0.17-i*0.065,-0.3,0.064),(0.012,0.34,0.002),'ink')
 lathe(n,[(0,0.25),(0.03,0.24),(0.03,-0.24),(0,-0.25)],'gold',seg=16,c=(0,-0.52,0.06),d=(1,0,0))
 box(n,(0,-0.3,0.055),(0.48,0.44,0.003),'red')
def nguyentrai():
 n='tb_nguyentrai';lathe(n,[(0,0.26),(0.022,0.25),(0.02,0.0),(0.018,-0.24),(0,-0.25)],'jade',seg=14)
 for y in(0.22,0.0,-0.22):torus(n,(0,y,0),0.022,0.005,'gold',rot=(math.pi/2,0,0),seg=16,mseg=5)
 lathe(n,[(0,-0.24),(0.026,-0.26),(0.03,-0.3),(0,-0.31)],'gold',seg=12)
 lathe(n,[(0,-0.3),(0.034,-0.31),(0.04,-0.38),(0.026,-0.46),(0,-0.52)],'ink',seg=16)
 tassel(n,0.27,'red')
def lycongtuan():
 n='tb_lycongtuan';box(n,(0,-0.24,0.06),(0.4,0.4,0.004),'yellowsilk')
 for i in range(5):box(n,(0.13-i*0.065,-0.24,0.064),(0.014,0.3,0.002),'red')
 for y in(-0.02,-0.46):
  lathe(n,[(0,0.24),(0.028,0.23),(0.028,-0.23),(0,-0.24)],'redwood',seg=14,c=(0,y,0.06),d=(1,0,0))
  for s in(-1,1):ell(n,(s*0.25,y,0.06),(0.03,0.03,0.03),m='gold',seg=12)
def quangtrung():
 n='tb_quangtrung';shaft(n,0.62,-0.9,r=0.026,m='redwood',rings=(0.54,0.1,-0.4,-0.86))
 lathe(n,[(0,0.64),(0.032,0.63),(0.014,0.72),(0,0.75)],'gold',seg=10)
 lathe(n,[(0,-0.88),(0.04,-0.9),(0.042,-0.98),(0,-0.99)],'gold',seg=12)
 blade(n,0.56,lambda t:0.08+0.05*math.sin(math.pi*t*0.9)-0.07*t*t,0.014,y0=-0.98,single=True,xo=lambda t:0.09*t*t,tipx=0.03)
 for i in range(6):cone(n,(-0.012,-1.02-i*0.07,0),(-1,0.5,0),0.014,0.06,'gold',seg=6)
 limb(n,[(0.05,-1.0,0.016),(0.1,-1.2,0.016),(0.13,-1.38,0.016)],lambda t:0.008,m='gold',n=8,sub=1)
 tassel(n,-0.94,'red');gem(n,(0.03,-1.02,0.016),0.02,'ec')
def haibatrung():
 n='tb_haibatrung';grip(n,0.0,0.17,r=0.022);pommel(n,0.19,0.028)
 box(n,(0,-0.03,0),(0.18,0.03,0.05),'gold',bev=0.01)
 for s in(-1,1):limb(n,[(s*0.09,-0.03,0),(s*0.12,-0.0,0),(s*0.12,0.04,0)],lambda t:0.012,m='gold',n=5,sub=1)
 blade(n,0.66,lambda t:0.028*(1-0.25*t)+0.004,0.008,y0=-0.045)
 box(n,(0,-0.3,0.0075),(0.005,0.42,0.002),'glow');gem(n,(0,-0.03,0.028),0.012)
 tassel(n,0.2,'red')
def batrieu():
 n='tb_batrieu';grip(n,0.0,0.18,r=0.024);pommel(n,0.2,0.032,'gold')
 # chắn tay hình đầu voi trắng có ngà
 ell(n,(0,-0.05,0),(0.07,0.06,0.06),m='ivory',seg=16)
 for s in(-1,1):
  ell(n,(s*0.08,-0.04,-0.01),(0.05,0.06,0.012),m='ivory',seg=12)
  limb(n,[(s*0.03,-0.08,0.04),(s*0.06,-0.12,0.08),(s*0.05,-0.08,0.13)],lambda t:0.012*(1-t*0.6),m='ivory',n=6)
 limb(n,[(0,-0.08,0.05),(0,-0.14,0.07),(0.0,-0.2,0.06)],lambda t:0.018*(1-t*0.5),m='ivory',n=6)
 gem(n,(0,-0.03,0.06),0.012,'ec')
 blade(n,0.74,lambda t:0.034*(1-0.2*t)+0.005,0.009,y0=-0.1,m='goldglow')
def lephunghieu():
 n='tb_lephunghieu';shaft(n,0.55,-0.8,r=0.026,rings=(0.48,-0.76))
 lathe(n,[(0,-0.78),(0.04,-0.8),(0.042,-0.86),(0,-0.87)],'gold',seg=12)
 blade(n,0.5,lambda t:0.1*(1-0.4*t)+0.02*math.sin(math.pi*t),0.016,y0=-0.86,single=True,xo=lambda t:0.05*t,tipx=0.02)
 torus(n,(-0.01,-1.0,0),0.035,0.008,'gold',rot=(0,0,0))
 tassel(n,-0.83,'yellow')
def dinhbolinh():
 n='tb_dinhbolinh';lathe(n,[(0,0.6),(0.02,0.59)]+[(0.02 if i%2 else 0.024,0.5-i*0.12) for i in range(12)]+[(0.02,-0.96),(0,-0.97)],'bamboo',seg=12)
 for k in range(7):
  a=k/7*math.pi*2;base=(0,-0.9,0);tip=(math.cos(a)*0.12,-1.25+0.04*math.sin(k*1.7),math.sin(a)*0.1)
  limb(n,[base,((base[0]+tip[0])/2,-1.08,(base[2]+tip[2])/2),tip],lambda t:0.005,m='reed',n=6,sub=1)
  ell(n,(tip[0]*1.1,tip[1]-0.07,tip[2]*1.1),(0.03,0.09,0.03),m='plume',seg=10)
def aura():
 n='tb_aura';torus(n,(0,0,0),0.16,0.006,'glow',rot=(0,0,0),seg=40)
 for i in range(6):
  a=i/6*math.pi*2;ell(n,(math.cos(a)*0.16,math.sin(a)*0.16,0),(0.018,0.03,0.006),(0,0,a),m='glow',seg=8)
 torus(n,(0,0,0),0.11,0.004,'glow',rot=(0,0,0),seg=32)
for f in(leloi,giong,anduongvuong,kimquy,ngoquyen,tranquoctoan,chudongtu,hungdao,nguyentrai,lycongtuan,quangtrung,haibatrung,batrieu,lephunghieu,dinhbolinh,aura):f()
objs=finish_nodes({},{})
for k,o in objs.items():
 t=tris([o])
 if t>2200:
  bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;d=o.modifiers.new('d','DECIMATE');d.ratio=2200/t;bpy.ops.object.modifier_apply(modifier='d')
COL={'metal':((0.85,0.88,0.92),1,0.2),'gold':((1,0.75,0.22),1,0.25),'goldglow':((1,0.82,0.3),1,0.2),'wood':((0.35,0.2,0.08),0,0.6),'redwood':((0.45,0.08,0.05),0,0.4),'oldwood':((0.3,0.2,0.1),0,0.8),'cloth':((0.3,0.05,0.05),0,0.8),'dark':((0.08,0.08,0.1),0.5,0.4),'red':((0.8,0.08,0.06),0,0.6),'gem':((0.1,0.8,0.5),0,0.1),'ec':((0.3,0.8,1),0,0.2),'iron':((0.2,0.2,0.22),1,0.5),'bronze':((0.55,0.38,0.16),1,0.35),'string':((0.9,0.9,0.85),0,0.8),'jade':((0.2,0.7,0.45),0,0.2),'rope':((0.6,0.5,0.3),0,0.9),'yellow':((1,0.8,0.1),0,0.6),'straw':((0.85,0.72,0.42),0,0.8),'silk':((0.95,0.88,0.6),0,0.7),'ink':((0.05,0.05,0.05),0,0.6),'yellowsilk':((1,0.82,0.2),0,0.6),'ivory':((0.96,0.94,0.88),0,0.4),'bamboo':((0.55,0.6,0.25),0,0.6),'reed':((0.7,0.65,0.45),0,0.8),'plume':((0.95,0.93,0.88),0,0.9),'glow':((0.6,0.95,1),0,0.2)}
for n,m in MATS.items():
 if n in COL:
  c,mt,r=COL[n];bs=m.node_tree.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=(*c,1);bs.inputs['Metallic'].default_value=mt;bs.inputs['Roughness'].default_value=r;m.diffuse_color=(*c,1)
print('TRIS',{k:tris([o]) for k,o in objs.items()})
export(os.path.join(OUT,'thanbinh.glb'))
