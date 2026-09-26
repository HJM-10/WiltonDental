"""Create an original stylised tooth mesh as glTF 2.0. No third-party model rights.

Revolved rounded-square crown with four cusps and three curved tapered roots.
Illustrative artwork only, not patient anatomy or a clinical teaching model.
"""
from pathlib import Path
import math, struct, json
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
verts=[]; faces=[]
N=64
def surface(rings):
    start=len(verts)
    for ring in rings: verts.extend(ring)
    for r in range(len(rings)-1):
        for j in range(N):
            a=start+r*N+j;b=start+r*N+(j+1)%N;c=b+N;d=a+N
            faces.extend([[a,c,b],[a,d,c]])
def catmull(points,steps=7):
    result=[];p=[points[0]]+points+[points[-1]]
    for i in range(1,len(p)-2):
        a,b,c,d=map(np.array,p[i-1:i+3])
        for t in np.linspace(0,1,steps,endpoint=False):
            result.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t))
    return result+[np.array(points[-1])]
crown=[]
for rad,y in catmull([(0,-.26),(.37,-.25),(.6,-.12),(.76,.13),(.83,.47),(.81,.74),(.69,.91),(.48,.91),(.25,.79),(0,.76)]):
    ring=[]
    for a in np.linspace(0,math.tau,N,endpoint=False):
        # Rounded-square perimeter and restrained cusps around the chewing surface.
        shape=(abs(math.cos(a))**3+abs(math.sin(a))**3)**(-1/3)
        cusp=.095*(1-math.cos(4*a))*max(0,(y-.45)/.5)*min(1,rad/.45)
        ring.append((rad*shape*math.cos(a),y+cusp,rad*shape*math.sin(a)*.87))
    crown.append(ring)
surface(crown)
for x,z,length,bend in [(-.37,.2,1.55,-.2),(.37,.2,1.42,.22),(0,-.34,1.32,.05)]:
    rings=[]
    for t in np.linspace(0,1,43):
        y=-.05-t*length
        r=.32*(1-t)**.62+.008
        if t==1:r=0
        cx=x+bend*math.sin(t*1.8);cz=z*(1+.4*t)
        rings.append([(cx+r*math.cos(a),y,cz+r*.87*math.sin(a)) for a in np.linspace(0,math.tau,N,endpoint=False)])
    surface(rings)
v=np.asarray(verts,dtype='<f4'); f=np.asarray(faces,dtype='<u4')
# Normals use area-weighted adjacent faces; orient outward independently per surface.
n=np.zeros_like(v)
for tri in f:
    a,b,c=v[tri];normal=np.cross(b-a,c-a)
    for i in tri:n[i]+=normal
n/=np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-8)
# Crown runs bottom-to-top, roots top-to-bottom; orient surface normals consistently.
crown_count=len(crown)*N
if np.mean(np.sum(n[:crown_count,[0,2]]*v[:crown_count,[0,2]],axis=1))<0:
    n[:crown_count]*=-1
    mask=np.all(f<crown_count,axis=1);f[mask]=f[mask][:,[0,2,1]]
for root_index,(x,z,_,_) in enumerate([(-.37,.2,1.55,-.2),(.37,.2,1.42,.22),(0,-.34,1.32,.05)]):
    lo=crown_count+root_index*43*N;hi=lo+43*N
    vec=v[lo:hi,[0,2]]-np.array([x,z])
    if np.mean(np.sum(n[lo:hi,[0,2]]*vec,axis=1))<0:
        n[lo:hi]*=-1;mask=np.all((f>=lo)&(f<hi),axis=1);f[mask]=f[mask][:,[0,2,1]]
blocks=[v.tobytes(),n.astype('<f4').tobytes(),f.tobytes()];binary=b''.join(blocks)
g={'asset':{'version':'2.0','generator':'Wilton Dental original illustrative mesh'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'mesh':0,'name':'Illustrative ceramic tooth'}],'meshes':[{'primitives':[{'attributes':{'POSITION':0,'NORMAL':1},'indices':2,'material':0}]}],'materials':[{'name':'Porcelain','pbrMetallicRoughness':{'baseColorFactor':[.94,.96,.96,1],'metallicFactor':.05,'roughnessFactor':.29},'doubleSided':False}],'buffers':[{'byteLength':len(binary)}],'bufferViews':[{'buffer':0,'byteOffset':sum(map(len,blocks[:i])),'byteLength':len(b),'target':34963 if i==2 else 34962} for i,b in enumerate(blocks)],'accessors':[{'bufferView':0,'componentType':5126,'count':len(v),'type':'VEC3','min':v.min(0).tolist(),'max':v.max(0).tolist()},{'bufferView':1,'componentType':5126,'count':len(n),'type':'VEC3'},{'bufferView':2,'componentType':5125,'count':f.size,'type':'SCALAR'}]}
j=json.dumps(g,separators=(',',':')).encode();j+=b' '*((-len(j))%4)
data=struct.pack('<4sII',b'glTF',2,12+8+len(j)+8+len(binary))+struct.pack('<I4s',len(j),b'JSON')+j+struct.pack('<I4s',len(binary),b'BIN\x00')+binary
(ROOT/'dist/assets/tooth.glb').write_bytes(data)
im=Image.open(ROOT/'dist/assets/tooth-sculpture.png');im.thumbnail((680,740));im.save(ROOT/'dist/assets/tooth-poster.webp','WEBP',quality=82)
print(f'Tooth: {len(v)} vertices, {len(f)} triangles, {len(data):,} bytes')
