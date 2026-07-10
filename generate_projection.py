import math, os
s=25.0; L=50.0; ap=s*math.sqrt(3)/2
# initial hex in base plane, hinge edge v1-v2 on HP, perpendicular to VP
verts0=[(0,-s/2,0),(0,s/2,0),(ap,s,0),(2*ap,s/2,0),(2*ap,-s/2,0),(ap,-s,0)]
th=math.radians(60)
def rot(p):
    x,y,z=p; return (x*math.cos(th), y, x*math.sin(th))
base=[rot(p) for p in verts0]
center=rot((ap,0,0))
axis=(-math.sin(th),0,math.cos(th))
apex=(center[0]+L*axis[0],0,center[2]+L*axis[2])
pts=base+[apex]
edges=[(0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(0,6),(1,6),(2,6),(3,6),(4,6),(5,6)]
faces=[[0,1,2,3,4,5],[0,1,6],[1,2,6],[2,3,6],[3,4,6],[4,5,6],[5,0,6]]
# orient normals outward using centroid
solid_cent=(sum(p[0] for p in pts)/7,sum(p[1] for p in pts)/7,sum(p[2] for p in pts)/7)
def sub(a,b): return (a[0]-b[0],a[1]-b[1],a[2]-b[2])
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b): return sum(a[i]*b[i] for i in range(3))
def normal(face):
    a,b,c=[pts[i] for i in face[:3]]; n=cross(sub(b,a),sub(c,a)); fc=tuple(sum(pts[i][j] for i in face)/len(face) for j in range(3))
    if dot(n, sub(solid_cent,fc))>0: n=tuple(-v for v in n)
    return n
face_norm=[normal(f) for f in faces]
edge_faces={e:[] for e in edges}
for fi,f in enumerate(faces):
    cyc=list(zip(f,f[1:]+f[:1]))
    for a,b in cyc:
        key=(a,b) if (a,b) in edge_faces else (b,a)
        if key in edge_faces: edge_faces[key].append(fi)
def vis_edges(view):
    visible=[]; hidden=[]
    for e,fs in edge_faces.items():
        isvis=any(dot(face_norm[fi],view)<-1e-9 for fi in fs)
        (visible if isvis else hidden).append(e)
    return visible,hidden
fv_vis,fv_hid=vis_edges((0,-1,0)); tv_vis,tv_hid=vis_edges((0,0,-1))
# offsets drawing coords: FV at (120,90), TV below XY y negative (first angle)
def fv(p): return (120+p[0], 90+p[2])
def tv(p): return (120+p[0], 30-p[1])
# DXF writer
ents=[]
def line(a,b,layer): ents.append(f"0\nLINE\n8\n{layer}\n10\n{a[0]:.6f}\n20\n{a[1]:.6f}\n30\n0\n11\n{b[0]:.6f}\n21\n{b[1]:.6f}\n31\n0\n")
def text(p,h,t,layer='Dimensions'): ents.append(f"0\nTEXT\n8\n{layer}\n10\n{p[0]:.6f}\n20\n{p[1]:.6f}\n30\n0\n40\n{h}\n1\n{t}\n")
# XY and projectors
line((40,90),(170,90),'Construction Lines')
text((42,93),3,'X-Y','Construction Lines')
for p in pts: line(fv(p),tv(p),'Construction Lines')
for e in fv_hid: line(fv(pts[e[0]]),fv(pts[e[1]]),'Hidden Lines')
for e in fv_vis: line(fv(pts[e[0]]),fv(pts[e[1]]),'Object Lines')
for e in tv_hid: line(tv(pts[e[0]]),tv(pts[e[1]]),'Hidden Lines')
for e in tv_vis: line(tv(pts[e[0]]),tv(pts[e[1]]),'Object Lines')
line(fv(center),fv(apex),'Centre Lines'); line(tv(center),tv(apex),'Centre Lines')
# labels
for i,p in enumerate(pts):
    lab=('a b c d e f o'.split()[i] if i<6 else 'O')
    text((fv(p)[0]+1,fv(p)[1]+1),2.5, lab+"'", 'Dimensions')
    text((tv(p)[0]+1,tv(p)[1]+1),2.5, lab, 'Dimensions')
text((90,125),4,'FINAL FRONT VIEW','Dimensions'); text((90,-5),4,'FINAL TOP VIEW','Dimensions')
# dimensions simplified
line(tv(pts[0]),tv(pts[1]),'Dimensions'); text((tv(pts[0])[0]+4,tv(pts[0])[1]-4),3,'Base side = 25 mm','Dimensions')
line(fv(center),fv(apex),'Dimensions'); text(((fv(center)[0]+fv(apex)[0])/2, (fv(center)[1]+fv(apex)[1])/2+4),3,'Axis = 50 mm','Dimensions')
# 30 deg indicator at center in FV
c=fv(center); line(c,(c[0]+28,c[1]),'Dimensions'); line(c,(c[0]-28*math.cos(math.radians(30)),c[1]+28*math.sin(math.radians(30))),'Dimensions'); text((c[0]-20,c[1]+8),3,'30° to H.P.','Dimensions')
header='0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n4\n0\nENDSEC\n0\nSECTION\n2\nTABLES\n0\nTABLE\n2\nLTYPE\n70\n3\n0\nLTYPE\n2\nCONTINUOUS\n70\n0\n3\nSolid\n72\n65\n73\n0\n40\n0\n0\nLTYPE\n2\nHIDDEN\n70\n0\n3\nHidden\n72\n65\n73\n2\n40\n6\n49\n3\n74\n0\n49\n-3\n74\n0\n0\nLTYPE\n2\nCENTER\n70\n0\n3\nCenter\n72\n65\n73\n4\n40\n8\n49\n5\n74\n0\n49\n-1\n74\n0\n49\n1\n74\n0\n49\n-1\n74\n0\n0\nENDTAB\n0\nTABLE\n2\nLAYER\n70\n5\n'
layers=[('Object Lines',7,'CONTINUOUS',35),('Hidden Lines',1,'HIDDEN',18),('Construction Lines',8,'CONTINUOUS',9),('Centre Lines',3,'CENTER',13),('Dimensions',5,'CONTINUOUS',13)]
for name,color,lt,lw in layers: header+=f'0\nLAYER\n2\n{name}\n70\n0\n62\n{color}\n6\n{lt}\n370\n{lw}\n'
header+='0\nENDTAB\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n'
dxf=header+''.join(ents)+'0\nENDSEC\n0\nEOF\n'
open('hexagonal_pyramid_projection.dxf','w').write(dxf)
# LSP and SCR use DXF creation/open basic lines
open('hexagonal_pyramid_projection.lsp','w').write('; Recreates the hexagonal pyramid projection drawing by opening the supplied DXF geometry.\n(command "_.OPEN" "hexagonal_pyramid_projection.dxf")\n')
open('hexagonal_pyramid_projection.scr','w').write('_.OPEN\nhexagonal_pyramid_projection.dxf\n')
# verification
import json
ver={
 'base_side': math.dist(pts[0],pts[1]), 'axis_length': math.dist(center,apex),
 'axis_angle_hp_deg': math.degrees(math.asin(abs(axis[2]))), 'axis_parallel_vp': abs(axis[1])<1e-9,
 'center': center, 'apex': apex, 'vertices': pts, 'fv_visible': fv_vis, 'fv_hidden': fv_hid, 'tv_visible': tv_vis, 'tv_hidden': tv_hid}
open('verification.json','w').write(json.dumps(ver,indent=2))
print(json.dumps(ver,indent=2))

# Replace the small DXF-opening helper scripts with standalone AutoCAD LSP/SCR
# command streams that recreate the generated layers, linework, labels and dimensions.
raw=''.join(ents).strip().splitlines()
parsed=[]; i=0
while i < len(raw):
    if raw[i] == '0':
        typ=raw[i+1]; i += 2; d={'TYPE': typ}
        while i < len(raw) and raw[i] != '0':
            if i + 1 < len(raw): d[raw[i]] = raw[i+1]
            i += 2
        parsed.append(d)
    else:
        i += 1
layer_cmds=[('Object Lines',7,'Continuous','0.35'),('Hidden Lines',1,'Hidden','0.18'),('Construction Lines',8,'Continuous','0.09'),('Centre Lines',3,'Center','0.13'),('Dimensions',5,'Continuous','0.13')]
lsp=['(defun c:HEX_PYRAMID_PROJECTION (/ )','  (command "_.UNITS" 2 3 1 0 0 "N")']
for name,color,lt,lw in layer_cmds:
    lsp.append(f'  (command "_.-LAYER" "M" "{name}" "C" "{color}" "" "LT" "{lt}" "" "LW" "{lw}" "" "")')
for d in parsed:
    if d['TYPE']=='LINE':
        lsp.append(f'  (command "_.-LAYER" "S" "{d["8"]}" "")')
        lsp.append(f'  (command "_.LINE" (list {d["10"]} {d["20"]} 0) (list {d["11"]} {d["21"]} 0) "")')
    elif d['TYPE']=='TEXT':
        txt=d['1'].replace('"','\\"')
        lsp.append(f'  (command "_.-LAYER" "S" "{d["8"]}" "")')
        lsp.append(f'  (command "_.TEXT" (list {d["10"]} {d["20"]} 0) {d["40"]} 0 "{txt}")')
lsp += ['  (princ)',')','(c:HEX_PYRAMID_PROJECTION)']
open('hexagonal_pyramid_projection.lsp','w').write('\n'.join(lsp)+'\n')
scr=['_.UNITS','2','3','1','0','0','N']
for name,color,lt,lw in layer_cmds:
    scr += ['_.-LAYER','M',name,'C',str(color),'','LT',lt,'','LW',lw,'','']
for d in parsed:
    if d['TYPE']=='LINE':
        scr += ['_.-LAYER','S',d['8'],'','_.LINE',f'{d["10"]},{d["20"]},0',f'{d["11"]},{d["21"]},0','']
    elif d['TYPE']=='TEXT':
        scr += ['_.-LAYER','S',d['8'],'','_.TEXT',f'{d["10"]},{d["20"]},0',d['40'],'0',d['1']]
open('hexagonal_pyramid_projection.scr','w').write('\n'.join(scr)+'\n')
