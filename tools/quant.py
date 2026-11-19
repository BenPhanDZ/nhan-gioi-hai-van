# Nén glTF nhúng: pháp tuyến float32 -> int8 chuẩn hoá (KHR_mesh_quantization), chỉ số uint32 -> uint16 khi được
import json,base64,struct,sys
def run(p):
 j=json.load(open(p));uri=j['buffers'][0]['uri'];raw=base64.b64decode(uri.split(',',1)[1])
 views=j['bufferViews'];acc=j['accessors']
 def data(a):
  v=views[a['bufferView']];o=v.get('byteOffset',0)+a.get('byteOffset',0);
  n={5126:4,5125:4,5123:2,5121:1,5122:2,5120:1}[a['componentType']]*{'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
  return raw[o:o+n*a['count']]
 normals=set();idxs=set()
 for m in j['meshes']:
  for pr in m['primitives']:
   if 'NORMAL' in pr['attributes']:normals.add(pr['attributes']['NORMAL'])
   if 'indices' in pr:idxs.add(pr['indices'])
 out=bytearray();newviews=[];vmap={}
 def addview(b,target=None,stride=None):
  while len(out)%4:out.append(0)
  v={'buffer':0,'byteOffset':len(out),'byteLength':len(b)}
  if target:v['target']=target
  if stride:v['byteStride']=stride
  out.extend(b);newviews.append(v);return len(newviews)-1
 def keep(vi):
  if vi not in vmap:
   v=views[vi];o=v.get('byteOffset',0);vmap[vi]=addview(raw[o:o+v['byteLength']],v.get('target'),v.get('byteStride'))
  return vmap[vi]
 for i,a in enumerate(acc):
  if 'bufferView' not in a:
   if 'sparse' in a:
    a['sparse']['indices']['bufferView']=keep(a['sparse']['indices']['bufferView']);a['sparse']['values']['bufferView']=keep(a['sparse']['values']['bufferView'])
   continue
  if i in normals and a['componentType']==5126 and not views[a['bufferView']].get('byteStride'):
   b=data(a);f=struct.unpack('<%df'%(a['count']*3),b);q=bytearray()
   for k in range(a['count']):
    x,y,z=f[k*3:k*3+3];q.extend(struct.pack('<bbbb',max(-127,min(127,round(x*127))),max(-127,min(127,round(y*127))),max(-127,min(127,round(z*127))),0))
   vi=addview(bytes(q),34962,4);a['componentType']=5120;a['normalized']=True;a['bufferView']=vi;a.pop('byteOffset',None);a.pop('min',None);a.pop('max',None)
  elif i in idxs and a['componentType']==5125 and a.get('max',[70000])[0]<65535:
   b=data(a);f=struct.unpack('<%dI'%a['count'],b);vi=addview(struct.pack('<%dH'%a['count'],*f),34963);a['componentType']=5123;a['bufferView']=vi;a.pop('byteOffset',None)
  else:
   a['bufferView']=keep(a['bufferView'])
 for im in j.get('images',[]):
  if 'bufferView' in im:im['bufferView']=keep(im['bufferView'])
 j['bufferViews']=newviews;j['buffers']=[{'byteLength':len(out),'uri':'data:application/octet-stream;base64,'+base64.b64encode(bytes(out)).decode()}]
 ext=set(j.get('extensionsUsed',[]));ext.add('KHR_mesh_quantization');j['extensionsUsed']=sorted(ext);req=set(j.get('extensionsRequired',[]));req.add('KHR_mesh_quantization');j['extensionsRequired']=sorted(req)
 json.dump(j,open(p,'w'),separators=(',',':'))
for p in sys.argv[1:]:
 import os;b=os.path.getsize(p);run(p);print(p,b,'->',os.path.getsize(p))
