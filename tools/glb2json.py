import struct,json,base64,sys
def conv(src,dst):
 b=open(src,'rb').read();assert b[:4]==b'glTF'
 l=struct.unpack('<I',b[12:16])[0];j=json.loads(b[20:20+l]);o=20+l
 bl=struct.unpack('<I',b[o:o+4])[0];bin_=b[o+8:o+8+bl]
 j['buffers']=[{'byteLength':len(bin_),'uri':'data:application/octet-stream;base64,'+base64.b64encode(bin_).decode()}]
 json.dump(j,open(dst,'w'),separators=(',',':'))
for a in sys.argv[1:]:conv(a,a.replace('.glb','.json'))
