import json, re, base64, sys
import numpy as np, pyfqmr
from glbx import GLB

def weld(P, F, tol=1e-6):
    key = np.round(P / tol).astype(np.int64)
    uniq, inv = np.unique(key, axis=0, return_inverse=True)
    inv = inv.reshape(-1)
    newP = np.zeros((len(uniq), 3)); cnt = np.zeros(len(uniq))
    np.add.at(newP, inv, P); np.add.at(cnt, inv, 1); newP /= cnt[:, None]
    F2 = inv[F]
    ok = (F2[:,0]!=F2[:,1]) & (F2[:,1]!=F2[:,2]) & (F2[:,0]!=F2[:,2])
    return newP, F2[ok]

def simplify(P, F, target):
    if len(F) <= target: return P, F
    s = pyfqmr.Simplify(); s.setMesh(P.astype(np.float64), F.astype(np.int32))
    s.simplify_mesh(target_count=int(target), aggressiveness=7, preserve_border=True, verbose=0)
    v, f, n = s.getMesh()
    return np.asarray(v, dtype=np.float64), np.asarray(f, dtype=np.int64)

def build(spec_list, glbs, out_path, meta, budget):
    parts = []
    all_names = {}
    for gpath in glbs:
        g = glbs[gpath]
        for i, n in g.mesh_nodes(): all_names.setdefault(n['name'], []).append((gpath, i))
    used = set()
    raw = []
    for sp in spec_list:
        Ps = []; Fs = []; off = 0
        for pat in sp['names']:
            hits = [nm for nm in all_names if (nm == pat or (pat.startswith('re:') and re.search(pat[3:], nm)))]
            if not hits: print('  !! no match', pat, file=sys.stderr)
            for nm in hits:
                if nm in used and not sp.get('allow_dup'): continue
                used.add(nm)
                for gpath, i in all_names[nm]:
                    for P, F, _ in glbs[gpath].node_world_geom(i):
                        Ps.append(P); Fs.append(F + off); off += len(P)
        if not Ps: continue
        P = np.vstack(Ps); F = np.vstack(Fs)
        P, F = weld(P, F)
        raw.append((sp, P, F))
    total = sum(len(F) for _, _, F in raw)
    scale_all = budget / total
    out = []
    lo = np.min([P.min(0) for _, P, _ in raw], axis=0); hi = np.max([P.max(0) for _, P, _ in raw], axis=0)
    center = (lo + hi) / 2; ext = (hi - lo).max() / 2
    for sp, P, F in raw:
        tgt = max(sp.get('min', 150), int(len(F) * scale_all * sp.get('w', 1.0)))
        P2, F2 = simplify(P, F, tgt)
        Q = np.clip(np.round((P2 - center) / ext * 32767), -32767, 32767).astype('<i2')
        idx = F2.astype('<u2' if len(P2) < 65536 else '<u4')
        out.append({'k': sp['k'], 'n': sp['n'], 'c': sp['c'], 'r': sp.get('r', 0.6),
                    'v': base64.b64encode(Q.tobytes()).decode(), 'i': base64.b64encode(idx.tobytes()).decode(),
                    'iw': idx.dtype.itemsize, 'nv': int(len(P2)), 'nt': int(len(F2))})
        print(f"  {sp['k']:12s} {len(F):7d} -> {len(F2):6d} tris")
    doc = dict(meta); doc['ext'] = float(ext); doc['parts'] = out
    s = json.dumps(doc, ensure_ascii=False, separators=(',', ':'))
    open(out_path, 'w').write(s)
    print(out_path, 'tris', sum(p['nt'] for p in out), 'size KB', len(s)//1024)

if __name__ == '__main__':
    which = sys.argv[1]
    specs = json.load(open('specs.json'))[which]
    glbs = {f: GLB(f + '.glb') for f in specs['glbs']}
    build(specs['parts'], glbs, 'm_' + which + '.json', specs['meta'], specs['budget'])
