import json,struct,sys
def load(path):
    b=open(path,'rb').read()
    magic,ver,length=struct.unpack('<4sII',b[:12])
    off=12; chunks=[]
    while off<len(b):
        ln,typ=struct.unpack('<I4s',b[off:off+8]); chunks.append((typ,b[off+8:off+8+ln])); off+=8+ln
    js=json.loads(chunks[0][1]); binc=chunks[1][1] if len(chunks)>1 else b''
    return js,binc
if __name__=='__main__':
    js,binc=load(sys.argv[1])
    print('extensionsUsed',js.get('extensionsUsed'),'extensionsRequired',js.get('extensionsRequired'))
    print('nodes',len(js.get('nodes',[])),'meshes',len(js.get('meshes',[])),'accessors',len(js.get('accessors',[])),'materials',len(js.get('materials',[])))
    acc=js['accessors']
    tv=0; tt=0
    for m in js['meshes']:
        for p in m['primitives']:
            tv+=acc[p['attributes']['POSITION']]['count']
            if 'indices' in p: tt+=acc[p['indices']]['count']//3
    print('total verts',tv,'tris',tt)
    # sample node names + extras
    for n in js['nodes'][:int(sys.argv[2]) if len(sys.argv)>2 else 15]:
        print(repr(n.get('name')), n.get('mesh'), json.dumps(n.get('extras',{}),ensure_ascii=False)[:160], 'children' if n.get('children') else '')
    print('attrs sample', js['meshes'][0]['primitives'][0]['attributes'], acc[js['meshes'][0]['primitives'][0]['attributes']['POSITION']].get('componentType'))
