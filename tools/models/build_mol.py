import json
BACKBONE={"P","OP1","OP2","OP3","O1P","O2P","O5'","C5'","C4'","O4'","C3'","O3'","C2'","C1'"}
def atoms(path):
    out=[]
    for line in open(path):
        if not line.startswith(('ATOM','HETATM')): continue
        alt=line[16]
        if alt not in (' ','A'): continue
        name=line[12:16].strip(); res=line[17:20].strip(); chain=line[21]
        x,y,z=float(line[30:38]),float(line[38:46]),float(line[46:54])
        el=(line[76:78].strip() or name[0]).upper()
        out.append(dict(name=name,res=res,chain=chain,x=x,y=y,z=z,el=el,het=line.startswith('HETATM')))
    return out
def pack(groups, meta, path, align=False):
    allp=[a for g in groups for a in g['atoms']]
    cx=sum(a['x'] for a in allp)/len(allp); cy=sum(a['y'] for a in allp)/len(allp); cz=sum(a['z'] for a in allp)/len(allp)
    if align:
        # Principal axis -> y (the helix stands upright), second axis -> x.
        import numpy as np
        P=np.array([[a['x']-cx,a['y']-cy,a['z']-cz] for a in allp])
        w,v=np.linalg.eigh(np.cov(P.T))
        R=np.stack([v[:,1],v[:,2],v[:,0]])
        if np.linalg.det(R)<0: R[2]*=-1
        for a in allp:
            q=R@np.array([a['x']-cx,a['y']-cy,a['z']-cz]); a['x'],a['y'],a['z']=float(q[0]),float(q[1]),float(q[2])
        cx=cy=cz=0.0
    ext=max(max(abs(a['x']-cx),abs(a['y']-cy),abs(a['z']-cz)) for a in allp)
    doc=dict(meta); doc['ext']=round(ext,2); doc['type']='mol'; doc['parts']=[]
    for g in groups:
        part={'k':g['k'],'n':g['n'],'c':g['c'],
          'a':[ [round(a['x']-cx,2),round(a['y']-cy,2),round(a['z']-cz,2),a['el']] for a in g['atoms']]}
        if g.get('s'): part['s']=g['s']
        doc['parts'].append(part)
        print(g['k'],len(g['atoms']))
    s=json.dumps(doc,ensure_ascii=False,separators=(',',':')); open(path,'w').write(s); print(path,len(s)//1024,'KB')
# DNA 1BNA
A=[a for a in atoms('1BNA.pdb') if a['res']!='HOH']
bb=[a for a in A if a['name'] in BACKBONE]
base={'DA':[], 'DT':[], 'DG':[], 'DC':[]}
for a in A:
    if a['name'] not in BACKBONE and a['res'] in base: base[a['res']].append(a)
pack([
 {'k':'squelette','n':'Squelette sucre-phosphate','c':'#A9BCD0','atoms':bb},
 {'k':'A','n':'Adénine (A)','c':'#E53935','atoms':base['DA']},
 {'k':'T','n':'Thymine (T)','c':'#1E88E5','atoms':base['DT']},
 {'k':'G','n':'Guanine (G)','c':'#43A047','atoms':base['DG']},
 {'k':'C','n':'Cytosine (C)','c':'#FDD835','atoms':base['DC']},
], {'id':'adn','titre':"L'ADN",'credit':"Structure réelle : PDB 1BNA (Drew et al., 1981), via RCSB PDB."}, 'm_adn.json', align=True)
# Hemoglobin 2HHB
H=[a for a in atoms('2HHB.pdb') if a['res'] not in ('HOH','PO4')]
prot={c:[a for a in H if not a['het'] and a['chain']==c] for c in 'ABCD'}
heme=[a for a in H if a['het'] and a['res']=='HEM']
pack([
 {'k':'a1','n':'Chaîne α (alpha)','c':'#E57373','atoms':prot['A']},
 {'k':'b1','n':'Chaîne β (bêta)','c':'#5C9CE6','atoms':prot['B']},
 {'k':'a2','n':'Chaîne α (alpha)','c':'#F0A0A0','atoms':prot['C']},
 {'k':'b2','n':'Chaîne β (bêta)','c':'#8DBDF2','atoms':prot['D']},
 {'k':'heme','n':'Groupe hème (avec son atome de fer)','c':'#FFB300','atoms':heme,'s':1.3},
], {'id':'hemoglobine','titre':"L'hémoglobine",'credit':"Structure réelle : PDB 2HHB (Fermi et al., 1984), via RCSB PDB."}, 'm_hemoglobine.json')
