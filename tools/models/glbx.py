import json,struct,math
import numpy as np, DracoPy
from glbinfo import load

def quat_to_mat(q):
    x,y,z,w=q
    return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
def node_local(n):
    if 'matrix' in n: return np.array(n['matrix']).reshape(4,4).T
    M=np.eye(4)
    s=np.array(n.get('scale',[1,1,1])); r=quat_to_mat(n.get('rotation',[0,0,0,1])); t=np.array(n.get('translation',[0,0,0]))
    M[:3,:3]=r*s; M[:3,3]=t; return M

class GLB:
    def __init__(self,path):
        self.js,self.bin=load(path)
        js=self.js
        self.parent={}
        for i,n in enumerate(js['nodes']):
            for c in n.get('children',[]): self.parent[c]=i
        self.world={}
        self._cache={}
    def wmat(self,i):
        if i in self.world: return self.world[i]
        M=node_local(self.js['nodes'][i])
        if i in self.parent: M=self.wmat(self.parent[i])@M
        self.world[i]=M; return M
    def mesh_geom(self,mi):
        if mi in self._cache: return self._cache[mi]
        js=self.js; out=[]
        for p in js['meshes'][mi]['primitives']:
            ext=p.get('extensions',{}).get('KHR_draco_mesh_compression')
            bv=js['bufferViews'][ext['bufferView']]
            data=self.bin[bv.get('byteOffset',0):bv.get('byteOffset',0)+bv['byteLength']]
            m=DracoPy.decode(data)
            pts=np.array(m.points,dtype=np.float64).reshape(-1,3); faces=np.array(m.faces,dtype=np.int64).reshape(-1,3)
            out.append((pts,faces,p.get('material')))
        self._cache[mi]=out; return out
    def node_world_geom(self,ni):
        n=self.js['nodes'][ni]; M=self.wmat(ni); res=[]
        for pts,faces,mat in self.mesh_geom(n['mesh']):
            P=(np.c_[pts,np.ones(len(pts))]@M.T)[:,:3]
            f=faces.copy()
            if np.linalg.det(M[:3,:3])<0: f=f[:,[0,2,1]]
            res.append((P,f,mat))
        return res
    def mesh_nodes(self):
        return [(i,n) for i,n in enumerate(self.js['nodes']) if 'mesh' in n]
