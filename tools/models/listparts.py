import sys,json
import numpy as np
from glbx import GLB
g=GLB(sys.argv[1]); out=[]
for i,n in g.mesh_nodes():
    geo=g.node_world_geom(i)
    tris=sum(len(f) for _,f,_ in geo); P=np.vstack([p for p,_,_ in geo])
    c=P.mean(0); mn=P.min(0); mx=P.max(0)
    out.append((n.get('name'),tris,[round(v,3) for v in c],[round(v,3) for v in (mx-mn)]))
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=0)
print(len(out),'parts; tris total',sum(o[1] for o in out))
