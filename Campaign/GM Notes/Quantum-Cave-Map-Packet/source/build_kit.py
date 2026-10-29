"""Reproducible five-foot-grid atlas and interchangeable jigsaw tile kit."""
from pathlib import Path
exec(compile((Path(__file__).parent/'base_geometry.py').read_text(),str(Path(__file__).parent/'base_geometry.py'),'exec'))
import random, itertools, hashlib
from collections import defaultdict
from shapely import affinity
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
for d in ['maps','previews','tiles','source']: (ROOT/d).mkdir(exist_ok=True)
for pattern in ['*-art.svg','*-cut.svg','*-print.png']:
    for generated in (ROOT/'tiles').glob(pattern):generated.unlink()
INK='#24596b'; GRID='#bfd0d3'; ACCENT='#b16436'; MUTED='#68808a'
FONT='/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf'
if not Path(FONT).exists():FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
if Path(FONT).exists():pdfmetrics.registerFont(TTFont('DV',FONT))
RFONT='DV' if Path(FONT).exists() else 'Helvetica'

def label(x,y,s,size=.6,anchor='start',color=INK,back=True):
    width=len(s)*size*.58+.16
    left=x-(width/2 if anchor=='middle' else width if anchor=='end' else 0)
    return (rect(left-.06,y-size*.84,width,size*1.12,'white','none') if back else '')+text(x,y,s,size,color,anchor)
def dotbadge(x,y,s):
    return circle(x,y,.65,'white',INK,.09)+text(x,y+.23,s,.68,INK,'middle','bold')
def outlines(g,fill='white',stroke=INK,sw=.10):
    return f'<path d="{path(g)}" fill="{fill}" fill-rule="evenodd" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
def doc(body,w,h,vb=None,physical=False):
    unit='in' if physical else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}{unit}" height="{h}{unit}" viewBox="{vb or f"0 0 {w} {h}"}">{body}</svg>'
def emit(name,svg,preview=False,pdf=True):
    p=ROOT/'maps'/f'{name}.svg';p.write_text(svg)
    if pdf:cairosvg.svg2pdf(bytestring=svg.encode(),write_to=str(ROOT/'maps'/f'{name}.pdf'))
    if preview:cairosvg.svg2png(bytestring=svg.encode(),write_to=str(ROOT/'previews'/f'{name}.png'),output_width=2400)
    return p
def transformed(s,dx=0,dy=0,scale=1):return f'<g transform="translate({dx},{dy}) scale({scale})">{s}</g>'

def roughen(g,seed):
    # Add small inward breaks to long exposed rock edges; preserve room extrema.
    rng=random.Random(seed);pts=[];coords=list(g.exterior.coords)
    for a,b in zip(coords,coords[1:]):
        pts.append(a);dx=b[0]-a[0];dy=b[1]-a[1];L=math.hypot(dx,dy)
        if L<3:continue
        for i in range(1,int(L)):
            t=i/int(L);x=a[0]+t*dx;y=a[1]+t*dy
            # Inward vector from edge toward an interior reference point.
            p=g.representative_point();nx=p.x-x;ny=p.y-y;n=math.hypot(nx,ny)
            f=rng.choice([0,.06,.10,.15,.22]);pts.append((x+nx/n*f,y+ny/n*f))
    q=Polygon(pts)
    assert q.is_valid
    return q

# The approach directions and overall topology match the first map revision.
entrance=roughen(entrance,11);junction=roughen(junction,12);hollow=roughen(hollow,13);lift=roughen(lift,14)
ports=[box(29,17.5,31,18.5),box(32,26.5,34,28),box(26.5,31,28,33),box(34,31,35.5,33),box(9,35.5,11,36.5),box(16.5,39,17.5,40),box(50,37.5,52,38.5),box(42.5,41,43.5,42)]
lower=unary_union([entrance,mouth,entryroute,junction,hollow,west,east,low,lift]+ports).difference(unary_union(pillars))
grotto=roughen(poly([(6,5),(8,3),(16,3),(18,5),(18,11),(16,13),(8,13),(6,11)]),15)
deep=unary_union([box(2,6,6.4,10),grotto])
GEOM={'lower':lower,'upper':upper,'deep':deep}

def vent_art(x,y,spent=False):
    crust=poly([(x-.72,y+.2),(x-.55,y-.35),(x-.1,y-.63),(x+.5,y-.42),(x+.78,y+.06),(x+.45,y+.4),(x+.05,y+.18),(x-.25,y+.43)])
    s=outlines(crust,'#f1f4f2',INK,.065)
    s+=f'<path d="M{x-.48},{y+.12} l.3,-.3 .18,.38 .25,-.43 .25,.22" fill="none" stroke="{INK}" stroke-width=".09"/>'
    if not spent:
        for dx,dy in [(-.9,-.45),(.8,-.6),(.1,.7)]:s+=line(x+dx,y+dy,x+dx+.12,y+dy+.06,width=.045)
    return s
def nest_art(x,y,seed):
    rng=random.Random(seed);s=''
    for j in range(3):
        pts=[(x+math.cos(a)*(1.2-j*.14),y+math.sin(a)*(.68-j*.1)) for a in [i*math.pi/9 for i in range(19)]]
        s+=f'<path d="{pathline(pts)}" fill="none" stroke="{INK}" stroke-width=".045"/>'
    for j in range(9):
        dx=rng.uniform(-.7,.7);dy=rng.uniform(-.3,.3)
        s+=f'<path d="M{x+dx},{y+dy} q.2,-.15 .4,.1" stroke="{INK}" stroke-width=".035" fill="none"/>'
    return s
def slab_art(x,y):
    g=poly([(x+.04,y+.14),(x+.23,y+.03),(x+2.82,y+.03),(x+2.97,y+.18),(x+2.97,y+2.82),(x+2.8,y+2.97),(x+.15,y+2.97),(x+.03,y+2.8)])
    s=outlines(g,'#f8faf9',INK,.10)
    pts=[]
    for i in range(130):
        a=i*.12;r=.03+i*.007;pts.append((x+1.5+math.cos(a)*r,y+1.5+math.sin(a)*r))
    s+=f'<path d="{pathline(pts)}" fill="none" stroke="{INK}" stroke-width=".065"/>'
    for a,b in [((.2,.3),(.65,.5)),((2.7,.2),(2.45,.6)),((.3,2.7),(.65,2.5))]:s+=line(x+a[0],y+a[1],x+b[0],y+b[1],width=.045)
    return s
def case_art(x,y):
    s=rect(x,y,.85,.55,'#f6e5bc',INK,.06)+rect(x+.08,y+.07,.69,.41,'none',INK,.035)
    s+=rect(x+.29,y-.08,.27,.08,'none',INK,.04)
    for dx in [.16,.62]:s+=rect(x+dx,y+.19,.06,.17,INK,INK,.02)
    return s
def q3_art(x,y):
    s=rect(x,y,3,3,'#fdfdfb',INK,.14)
    for xg in [1,2]:s+=line(x+xg,y+.15,x+xg,y+2.85,GRID,.025)
    for yg in [1,2]:s+=line(x+.15,y+yg,x+2.85,y+yg,GRID,.025)
    s+=f'<path d="M{x+.23},{y+.23} H{x+2.77} V{y+.88} M{x+2.77},{y+2.12} V{y+2.77} H{x+.23} V{y+.23}" fill="none" stroke="{MUTED}" stroke-width=".06"/>'
    s+=line(x+3,y+1,x+3,y+2,'white',.2)
    s+=f'<path d="M{x+2.75},{y+1} q-.23,.08 0,.16 t0,.16 t0,.16 t0,.16 t0,.16 t0,.16" fill="none" stroke="{INK}" stroke-width=".055"/>'
    for dx,dy in [(.7,2.3),(1,2.1),(1.5,1.6)]:s+=f'<ellipse cx="{x+dx}" cy="{y+dy}" rx=".07" ry=".13" fill="{MUTED}" opacity=".65"/>'
    return s
def ship_art(x,y):
    hull=[(x+5,y),(x+7.9,y+2.9),(x+8.2,y+5.4),(x+10,y+8),(x+9.7,y+10.9),(x+7.3,y+10.1),(x+7.3,y+11.8),(x+2.7,y+11.8),(x+2.7,y+10.1),(x+.3,y+10.9),(x,y+8),(x+1.8,y+5.4),(x+2.1,y+2.9)]
    s=outlines(poly(hull),'#f7faf9',INK,.13)
    s+=outlines(poly([(x+5,y+.85),(x+7.1,y+3.2),(x+2.9,y+3.2)]),'#d7e7e9',INK,.055)
    s+=line(x+5,y+.85,x+5,y+3.2,width=.045)+rect(x+3,y+4.1,4,4.8,'none',INK,.065)
    for yy in [4.7,8.3]:s+=line(x+3.4,y+yy,x+6.6,y+yy,width=.04)
    for xx in [3.1,5.7]:
        s+=rect(x+xx,y+9.7,1.2,2,'white',INK,.07)
        for j in range(5):s+=line(x+xx+.1,y+10.65+j*.18,x+xx+1.1,y+10.65+j*.18,width=.04)
    for xx,flip in [(1,1),(9,-1)]:
        s+=f'<path d="M{x+xx},{y+8.2} l{flip*1.5},-1.5 v2.5 l{-flip*1.2},.55 Z" fill="none" stroke="{INK}" stroke-width=".06"/>'
    s+=rect(x-2,y+8,4,1.5,'#f6f7f4',INK,.08)
    for i in range(1,8):s+=line(x-2+i*.5,y+8,x-2+i*.5,y+9.5,width=.04)
    for xx,yy in [(2.2,3),(7.8,3),(2.2,11),(7.8,11)]:s+=rect(x+xx-.25,y+yy-.25,.5,.5,'#ecf0ee',INK,.055)
    return s
def anomaly_art(x,y):
    s=''
    facets=[(0,0,.62),(-1,-.3,.38),(.9,-.8,.38),(.95,.75,.4),(-.65,.9,.29),(0,-1.1,.2)]
    for dx,dy,r in facets:
        s+=outlines(poly([(x+dx,y+dy-r),(x+dx+r*.8,y+dy),(x+dx,y+dy+r),(x+dx-r*.8,y+dy)]),'#dceef1',INK,.06)
        s+=line(x+dx,y+dy-r,x+dx,y+dy+r,INK,.035)
    for a,b in [(1,0),(2,0),(3,0),(4,1)]:
        aa=facets[a];bb=facets[b];s+=line(x+aa[0],y+aa[1],x+bb[0],y+bb[1],MUTED,.025)
    return s

def hatch(g,seed):
    rng=random.Random(seed);s='';boundary=g.boundary
    # Draw rock strokes only beyond the floor, so the grid remains clear.
    rings=[g.exterior]+list(g.interiors)
    for ring in rings:
        ll=LineString(ring.coords)
        for i in range(int(ll.length/.6)):
            p=ll.interpolate(i*.6);pn=ll.interpolate(min(ll.length,i*.6+.05));dx=pn.x-p.x;dy=pn.y-p.y;n=math.hypot(dx,dy)
            if n<1e-8:continue
            nx=-dy/n;ny=dx/n
            if g.contains(Point(p.x+nx*.1,p.y+ny*.1)):nx=-nx;ny=-ny
            le=rng.uniform(.17,.4);s+=line(p.x+nx*.09,p.y+ny*.09,p.x+nx*le,p.y+ny*le,MUTED,.025)
    return s

def fixed(panel):
    s=''
    if panel=='lower':
        for x,y in [(27.2,6),(32.8,6),(27.2,14),(32.8,14)]:s+=rect(x-.35,y-.3,.7,.6,'none',MUTED,.035)
        s+=rect(21.2,11.7,1.35,.65,'none',INK,.06)
        for x in [21.45,21.8,22.15]:s+=line(x,11.7,x,12.35,width=.04)
        s+=line(29,18,31,18,ACCENT,.12)+vent_art(29,29,True)
        s+=f'<path d="M34,33.3 H50.2 V37.5 L44.2,39.5" fill="none" stroke="{INK}" stroke-width=".045"/>'
        s+=f'<path d="M34,33.15 H50.35 V37.6 L44.3,39.6" fill="none" stroke="{INK}" stroke-width=".025"/>'
        for j,y in enumerate([38,41,44]):s+=nest_art(5.1,y,j+30)
        s+=vent_art(7,39.5)+vent_art(7,43.5)
        # Dashed overhead stair projection in lower plan.
        s+=f'<path d="M28,27.2 h1 v1.3 h-1 Z" fill="none" stroke="{MUTED}" stroke-width=".06" stroke-dasharray=".15 .12"/>'
        for y in [27.5,27.8,28.1]:s+=line(28,y,29,y,MUTED,.035,'.12 .1')
        s+=rect(47,38,3,3,'none',INK,.045)
    elif panel=='upper':
        s+=stairs(3,7,2,4.4)+line(3,11.45,3.4,11.7)+line(3.4,11.7,4,11.4)+line(4,11.4,4.6,11.7)+line(4.6,11.7,5,11.45)
        s+=vent_art(7,4.8)
        for x in range(6,21):
            if x not in [17,18,19]:s+=line(x,7,x+.16,7.35,width=.04)
        s+=rect(27,7,4,4,'none',MUTED,.035)
        s+=rect(31.2,9.8,.5,.7,'white',INK,.055)+rect(31.28,9.88,.34,.36,'#dceef1',INK,.025)
    else:
        s+=f'<ellipse cx="12" cy="8" rx="2.1" ry="1.5" fill="none" stroke="{MUTED}" stroke-width=".04"/>'
        s+=f'<path d="M10,8.2 Q12,10.1 14,8.2" fill="none" stroke="{MUTED}" stroke-width=".025"/>'
        s+=rect(2,6,4,4,'none',MUTED,.035)+rect(6.2,9,.5,.7,'white',INK,.055)+rect(6.28,9.08,.34,.36,'#dceef1',INK,.025)
    return s

clip_seq=itertools.count()
def scene(panel,q1='B',q2='L',q3='G',gm=False,post=False,objects=True,ship_override=None,case_override=None):
    g=GEOM[panel];gid=f'clip{next(clip_seq)}';x0,y0,x1,y1=g.bounds
    s=f'<defs><clipPath id="{gid}">{outlines(g)}</clipPath></defs>'+hatch(g,19)+outlines(g)
    s+=f'<g clip-path="url(#{gid})">'
    for x in range(math.floor(x0),math.ceil(x1)+1):s+=line(x,y0,x,y1,GRID,.022)
    for y in range(math.floor(y0),math.ceil(y1)+1):s+=line(x0,y,x1,y,GRID,.022)
    s+='</g>'+fixed(panel)
    if panel=='lower':
        s+=mouth_art(q1)
        if q2=='L' and objects:s+=slab_art(47,38)
        if objects and (ship_override if ship_override is not None else q1=='U'):s+=ship_art(25,3)
        if objects and case_override=='lower':s+=case_art(48,39)
        if gm:
            for x,y,n in [(20.4,4.8,'1'),(33.6,29,'2'),(15.4,37.3,'3'),(51.4,44.4,'4')]:s+=dotbadge(x,y,n)
            s+=label(20.2,16.7,'Q1 / entire hall',.65)+label(20.2,17.55,'120 x 80 ft',.48)
            s+=label(29,19.2,'Fixed passage begins',.48,'end')+label(34.3,23.3,'Two sight-blocking bends',.46)
            s+=label(28.5,26.3,'S / stair ends +15 ft',.48,'middle')+label(48.5,37.3,'L / Q2 dock',.53,'middle')
            s+=label(27,38.3,'Low tunnel / 4-ft ceiling',.5,'middle')+label(36,34.5,'Salvage cable',.46)
            for x,y,n in [(7,39.5,'V1'),(7,43.5,'V2')]:s+=f'<circle cx="{x}" cy="{y}" r="2" fill="none" stroke="{ACCENT}" stroke-width=".05" stroke-dasharray=".16 .12"/>'+label(x+1,y-.7,n,.44)
    elif panel=='upper':
        if objects and q2=='H':
            s+=slab_art(17,7)
            if case_override is None or case_override=='upper':s+=case_art(18,8)
        else:
            s+=line(17,7,20,10,MUTED,.035)+line(17,10,20,7,MUTED,.035)
        if objects and q3=='G':s+=q3_art(27.5,7.5)
        if gm:
            s+=dotbadge(12,5,'5')+label(18.5,11.1,'L / +20 ft',.53,'middle')+label(2.5,13,'S / 5-ft stair descent, then 15-ft gap',.49)
            s+=label(29,12,'Q3 / Gallery berth',.51,'middle')+label(24,6.3,'Sight-blocking corner',.44)
            s+=f'<circle cx="7" cy="4.8" r="2" fill="none" stroke="{ACCENT}" stroke-width=".05" stroke-dasharray=".16 .12"/>'+label(8,4,'V3',.44)
    else:
        if objects and q3=='D':s+=q3_art(2.5,6.5)
        if objects and not post:s+=anomaly_art(12,8)
        if gm:s+=dotbadge(16,5,'6')+label(4,11.2,'Q3 / Deep berth',.51,'middle')+label(12,11.1,'Empty replacement grotto' if post else 'Anomaly',.48,'middle')
    return s

def mouth_art(state):
    fill={'B':'#fafbf5','D':'#dce5eb','U':'#e2e5e2'}[state]
    s=rect(24,0,12,2,fill,'none')
    if state=='U':
        for x in range(24,36):s+=line(x,0,x+1,2,MUTED,.035)
        s+=f'<path d="M24,2 l1,-.15 1,.15 1,-.07 1,.07 1,-.15 1,.15 1,-.08 1,.08 1,-.18 1,.18 1,-.1 1,.1" fill="none" stroke="{INK}" stroke-width=".15"/>'
    else:
        for x in range(24,37):s+=line(x,0,x,2,GRID,.022)
        s+=line(24,1,36,1,GRID,.022)
        for x,y in [(25.2,.6),(28.6,1.25),(33.2,.5)]:
            s+=f'<path d="M{x-.35},{y+.1} l.3,-.2 .4,.1 .1,.2" fill="none" stroke="{MUTED}" stroke-width=".04"/>'
        s+=line(24,0,24,2,width=.10)+line(36,0,36,2,width=.10)
    return s

STATES=list(itertools.product('BDU','LH','GD'))
Q1={'B':'BRIGHT-SIDE','D':'DARK-SIDE','U':'UNDERGROUND'};Q2={'L':'LOWER','H':'UPPER'};Q3={'G':'GALLERY','D':'DEEP'}
def master(state=('B','L','G'),gm=True,blue=False,post=False,escape_ship=False):
    a,b,c=state;col='white' if blue else INK
    s=rect(0,0,90,66,INK if blue else 'white','none')
    s+=text(2.5,2.8,'THE QUANTUM CAVE',1.45,col,weight='bold')
    st=f'{a}-{b}-{c}  /  {Q1[a]}  /  LIFT {Q2[b]}  /  ROOM AT {Q3[c]}'
    if post:st+='  /  AFTER CONTACT'
    s+=text(2.5,4.3,st,.64,col)
    s+=text(2.5,5.4,('GM STATE MAP' if gm else 'PLAYER STATE MAP')+'  |  1 SQUARE = 5 FEET  |  NORTH UP',.5,col)
    for panel,dx,dy in [('lower',-1,8),('upper',55,7),('deep',62,29)]:
        s+=transformed(scene(panel,a,b,c,gm,post,ship_override=True if escape_ship else None),dx,dy)
    for x,y,t in [(2,7.2,'LOWER CAVE / FLOOR +0 FT'),(57,7.2,'UPPER GALLERY / FLOOR +20 FT'),(57,27.3,'REMOTE GROTTO / SEPARATE SPACE')]:s+=text(x,y,t,.5,col)
    if gm:
        # Connection key sits in the free lower-right space.
        s+=text(58,46,'CONNECTIONS',.7,col,weight='bold')
        for i,t in enumerate(['L: area 4 north dock <-> area 5 south dock','S: area 5 west stairs <-> area 2 overhead','Q3: Gallery berth <-> Deep berth','One traveling room; two receiving berths.']):s+=text(58,47.4+i*1.1,t,.49,col)
        if escape_ship:s+=label(31,15.5,'SHIP HELD BY OBSERVATION',.47,'middle')
        lines=['1 Entrance Hall   2 Nest Junction   3 Feeding Hollow   4 Lift Cavern   5 Upper Gallery   6 Grotto',
        'Q1: Bright > Dark > Underground > Bright.   Q2: Lower <-> Upper.   Q3: Gallery <-> Deep.',
        'Each feature changes independently after its final observer releases it. Rust dashed circles: 10-ft vent bursts.',
        'Ship/case shown at home states. Track carried objects separately; the appendix includes the ship escape state.']
    else:lines=['Use individual tiles for gradual reveal. This complete map reveals the explored layout.', 'The separate plans share the same grid scale; their page positions are independent.']
    for i,t in enumerate(lines):s+=text(2.5,58+i*1.3,t,.55,col)
    s+=line(79,64,85,64,col,.1)
    for x in [79,81,83,85]:s+=line(x,63.7,x,64.3,col,.08)
    s+=text(82,65.2,'30 ft',.5,col,'middle')
    return doc(s,17,17*66/90,'0 0 90 66',True)

def crop_scene(panel,bounds,dx,dy,scale=1,**kw):
    x0,y0,x1,y1=bounds;cid=f'crop{next(clip_seq)}'
    content=scene(panel,**kw)
    return f'<defs><clipPath id="{cid}">{rect(x0,y0,x1-x0,y1-y0)}</clipPath></defs>'+f'<g transform="translate({dx},{dy}) scale({scale}) translate({-x0},{-y0})"><g clip-path="url(#{cid})">{content}</g></g>'
def plate(title,subtitle):return rect(0,0,96,61,'white','none')+text(3,3.3,title,1.5,weight='bold')+text(3,5,subtitle,.66)
def arrow(x1,y1,x2,y2):
    ang=math.atan2(y2-y1,x2-x1);r=.65
    return line(x1,y1,x2,y2,ACCENT,.13)+outlines(poly([(x2,y2),(x2-r*math.cos(ang-.45),y2-r*math.sin(ang-.45)),(x2-r*math.cos(ang+.45),y2-r*math.sin(ang+.45))]),ACCENT,ACCENT,.03)

# Side-by-side plates give the GM simultaneous views of every alternative.
s=plate('Q1 / ENTRANCE STATES','The whole hall changes state. Its southern passage and connection to area 2 remain fixed.')
for i,a in enumerate('BDU'):
    dx=3+i*31;s+=text(dx,8,Q1[a],.95,weight='bold')
    s+=crop_scene('lower',(17,-.5,43,20),dx,9,1,q1=a,q2='L',q3='G',gm=False)
    s+=label(dx+13,31,'A / same southern passage',.6,'middle')
    s+=text(dx,33,{'B':'Daylight / empty berth at home','D':'Night / empty berth at home','U':'Rock closure / ship at home'}[a],.6)
    s+=arrow(dx+13,31.7,dx+13,36)
s+=line(16,36,78,36,ACCENT,.12)+arrow(47,36,47,39)
s+=rect(29,39,36,6,'#f4f7f6',INK,.07)+text(47,41.2,'FIXED TWO-BEND PASSAGE',.85,anchor='middle',weight='bold')+text(47,43,'Leads to area 2 / Nest Junction in every state',.62,anchor='middle')
for j,t in enumerate(['Cycle: Bright-Side > Dark-Side > Underground > Bright-Side.',
 'The matching Q1 mouth inserts use identical jigsaw outlines in all three states.',
 'Keep the four hall sections in place; exchange the single mouth insert and move the ship overlay.',
 'Escape: keep observing the ship, release Q1, then move Underground > Bright-Side.']):s+=text(3,49+j*1.6,t,.67)
emit('GM-Plate-Q1',doc(s,17,17*61/96,'0 0 96 61',True),True)

s=plate('Q2 / LIFT POSITIONS','Only the 15-ft slab changes position. The cavern floor, cliff and upper gallery are fixed.')
for i,b in enumerate('LH'):
    dx=4+i*47;s+=text(dx,8,'SLAB '+Q2[b],1,weight='bold')
    s+=crop_scene('upper',(14,4,23,12),dx+6,10,1.6,q2=b,gm=False)
    s+=text(dx+24,15,'Upper dock',.7)+text(dx+24,16.5,'Gallery floor +20 ft',.6)
    s+=arrow(dx+13,24,dx+13,28)
    s+=crop_scene('lower',(42,37,54,47),dx+3,29,1.5,q2=b,gm=False)
    s+=text(dx+24,35,'Lower dock',.7)+text(dx+24,36.5,'Cavern floor +0 ft',.6)
    s+=text(dx,47,'Case at home: '+('Upper configuration' if b=='L' else 'On the slab'),.65)
for j,t in enumerate(['Move the single slab insert between the matching 3 x 3 docks; put the empty insert in its former dock.',
 'An upper empty dock shows a 20-ft drop. The lower empty dock is a shallow floor recess.',
 'The case can accompany an observed slab transition when watched separately; its token tracks that exception.',
 'Climb the fixed cliff as an alternate route. Creatures standing entirely on Q2 travel with the slab.']):s+=text(3,52+j*1.55,t,.65)
emit('GM-Plate-Q2',doc(s,17,17*61/96,'0 0 96 61',True),True)

s=plate('Q3 / TRAVELING ROOM','The room occupies one berth at a time. Its doorway faces east at both destinations.')
for row,c in enumerate('GD'):
    yy=10+row*20;s+=text(3,yy-2,'ROOM AT '+Q3[c],.9,weight='bold')
    s+=crop_scene('upper',(26,6,34,12),5,yy,1.6,q3=c,gm=False)
    s+=arrow(22,yy+5,39,yy+5)
    s+=crop_scene('deep',(1,2,19,14),42,yy,1.3,q3=c,gm=False)
    s+=text(70,yy+3,'Gallery berth: '+('occupied' if c=='G' else 'empty'),.62)
    s+=text(70,yy+4.5,'Deep berth: '+('occupied' if c=='D' else 'empty'),.62)
    s+=text(5,yy+11,'Connected to fixed area 5',.57)
for j,t in enumerate(['The 4 x 4 berth tiles share one cut shape. Swap occupied and empty inserts between them.',
 'The stone room itself remains 3 x 3 squares; the tile includes the fixed clearance around it.',
 'The viewing slate at each berth can establish observation of Q3 so an empty room can be called back.',
 'After the vision: return everyone and Q3 to Gallery. Remove the anomaly; Deep now reaches the replacement grotto.']):s+=text(3,53+j*1.5,t,.63)
emit('GM-Plate-Q3',doc(s,17,17*61/96,'0 0 96 61',True),True)

# Twelve independent combinations, plus the scripted post-contact and ship-escape examples.
gmfiles=[];pfiles=[]
for idx,state in enumerate(STATES,1):
    code='-'.join(state)
    emit(f'GM-{idx:02}-{code}',master(state,True),preview=idx==1)
    emit(f'Players-{idx:02}-{code}',master(state,False))
    gmfiles.append(ROOT/'maps'/f'GM-{idx:02}-{code}.pdf');pfiles.append(ROOT/'maps'/f'Players-{idx:02}-{code}.pdf')
emit('GM-After-Contact',master(('B','L','G'),True,post=True))
emit('Players-After-Contact',master(('B','L','G'),False,post=True))
emit('GM-Ship-Escape',master(('B','L','G'),True,escape_ship=True))
emit('Players-Ship-Escape',master(('B','L','G'),False,escape_ship=True))
emit('Quantum-Cave-GM-Blue',master(('B','L','G'),True,True),True)

# Physical sections use inch coordinates, one inch per five-foot square.
from shapely.ops import linemerge
from reportlab.lib.colors import HexColor
for d,pattern in [('Chipboard','*.svg'),('Cardstock','*.png')]:
    (ROOT/d).mkdir(exist_ok=True)
    for generated in (ROOT/d).glob(pattern):generated.unlink()

def components(g):
    if g.is_empty:return []
    if g.geom_type=='Polygon':return [g]
    return [p for p in g.geoms if p.geom_type=='Polygon']
def whole(g):return unary_union([Polygon(p.exterior) for p in components(g)])
def peg(x,y,axis='x',clearance=0):
    p=unary_union([box(x-.025,y-.12,x+.23,y+.12),Point(x+.20,y).buffer(.20,quad_segs=16)])
    if axis=='y':p=affinity.rotate(p,90,origin=(x,y))
    return p.buffer(clearance) if clearance else p
q1=box(24,0,36,2).union(peg(27,2,'y')).union(peg(33,2,'y'))
q2=box(0,0,3,3).union(peg(3,1.5))
q3=box(0,0,4,4).union(peg(4,2))
slots={'lower':[('Q1',q1),('Q2-L',affinity.translate(q2,47,38))],
       'upper':[('Q2-H',affinity.translate(q2,17,7)),('Q3-G',affinity.translate(q3,27,7))],
       'deep':[('Q3-D',affinity.translate(q3,2,6))]}
bodies={}
for panel,g in GEOM.items():
    # Pillars stay printed on the backing; rock between looping passages stays open.
    body=(g.union(unary_union(pillars)) if panel=='lower' else g).buffer(.18,join_style=2)
    for name,slot in slots[panel]:body=body.union(slot.buffer(.18,join_style=2))
    if panel=='lower':body=body.difference(box(-100,-100,100,2)).union(q1)
    bodies[panel]=body

# Ownership masks separate room reveals and keep every backing within 11 x 14 stock.
regions={
'lower':[
 ('Entrance-NW',box(-100,-100,30,10)),('Entrance-NE',box(30,-100,100,10)),
 ('Entrance-SW',box(-100,10,30,18.2)),('Entrance-SE',box(30,10,100,18.2)),
 ('Entrance-Passage',box(-100,18.2,100,27)),('Nest-Junction',box(26.5,27,35.5,35.2)),
 ('Feeding-West',box(-100,35.8,10,100)),('Feeding-East',box(10,35.8,17.2,100)),
 ('Lift-Cavern',box(42.8,37.8,100,100)),
 ('West-Passage-A',box(-100,27,18,35.8)),('West-Passage-B',box(18,27,26.5,35.8)),
 ('East-Passage-A',box(35.5,27,44,37.8)),('East-Passage-B',box(44,27,100,37.8)),
 ('Low-Tunnel-A',box(-100,35.2,30,100)),('Low-Tunnel-B',box(30,35.2,100,100))],
'upper':[('Gallery-West',box(-100,-100,13,100)),('Gallery-Middle',box(13,-100,23,100)),('Gallery-East',box(23,-100,100,100))],
'deep':[('Grotto-West',box(-100,-100,10,100)),('Grotto-East',box(10,-100,100,100))]}
pieces=[];joints=[]
for panel,body in bodies.items():
    fixedbody=body.difference(unary_union([g for n,g in slots[panel]]));remaining=fixedbody;parts=[]
    for name,mask in regions[panel]:
        g=remaining.intersection(mask).buffer(0)
        assert g.area>.1,name
        parts.append({'id':name,'panel':panel,'kind':'fixed','shape':g})
        remaining=remaining.difference(g)
    assert remaining.area<1e-7,(panel,'unassigned',remaining.area)
    for a in parts:
        for fragment in components(a['shape']):
            if fragment.area>=.8:continue
            choices=[(fragment.boundary.intersection(b['shape'].boundary).length,j)
                     for j,b in enumerate(parts) if b is not a]
            length,j=max(choices)
            assert length>1e-7,(a['id'],'isolated fragment')
            parts[j]['shape']=parts[j]['shape'].union(fragment)
            a['shape']=a['shape'].difference(fragment).buffer(0)
    # One broad tab per meaningful shared boundary. A few wide joints receive two.
    for i,a in enumerate(parts):
        for b in parts[i+1:]:
            common=a['shape'].boundary.intersection(b['shape'].boundary)
            ls=[common] if common.geom_type=='LineString' else [x for x in getattr(common,'geoms',[]) if x.geom_type=='LineString']
            if len(ls)>1:
                merged=linemerge(ls);ls=[merged] if merged.geom_type=='LineString' else list(merged.geoms)
            for edge in ls:
                if edge.length<1.1:continue
                x0,y0,x1,y1=edge.bounds
                if x1-x0<1e-6:axis='x'
                elif y1-y0<1e-6:axis='y'
                else:continue
                for f in ([.3,.7] if edge.length>7 else [.5]):
                    c=edge.interpolate(f,normalized=True);tab=peg(c.x,c.y,axis)
                    union=a['shape'].union(b['shape'])
                    if not union.buffer(1e-8).covers(tab):continue
                    forward=Point(c.x+.3,c.y) if axis=='x' else Point(c.x,c.y+.3)
                    owner,other=(a,b) if b['shape'].covers(forward) else (b,a)
                    owner['shape']=owner['shape'].union(tab);other['shape']=other['shape'].difference(tab)
                    joints.append([owner['id'],other['id'],c.x,c.y])
    assembled=unary_union([p['shape'] for p in parts]);assert assembled.symmetric_difference(fixedbody).area<1e-7
    for i,a in enumerate(parts):
        assert a['shape'].geom_type=='Polygon',a['id']
        for b in parts[i+1:]:assert a['shape'].intersection(b['shape']).area<1e-7
    pieces+=parts
for state in 'BDU':pieces.append({'id':'Q1-'+Q1[state].title(),'panel':'lower','kind':'mouth','state':state,'shape':q1,'family':'Q1'})
for name,kind in [('Slab','slab'),('Lower-Empty','lower-empty'),('Upper-Empty','upper-empty')]:pieces.append({'id':'Q2-'+name,'panel':None,'kind':kind,'shape':q2,'family':'Q2'})
for name,kind in [('Room','room'),('Empty','room-empty')]:pieces.append({'id':'Q3-'+name,'panel':None,'kind':kind,'shape':q3,'family':'Q3'})
hull=poly([(5,0),(7.9,2.9),(8.2,5.4),(10,8),(9.7,10.9),(7.3,10.1),(7.3,11.8),(2.7,11.8),(2.7,10.1),(.3,10.9),(0,8),(1.8,5.4),(2.1,2.9)])
# The ramp sits against the port hull edge. Shared contour defines its irregular end.
ramp=box(-2,8,2,9.5).difference(hull)
pieces += [{'id':'Ship-Hull','panel':None,'kind':'ship','shape':hull},
 {'id':'Ship-Ramp','panel':None,'kind':'ship','shape':ramp},
 {'id':'Anomaly','panel':None,'kind':'anomaly','shape':box(0,0,3,3)},
 {'id':'Maintenance-Case','panel':None,'kind':'case','shape':box(0,0,1.1,.85)}]
SCENES={p:scene(p,objects=False,post=True) for p in GEOM}
def artwork(p):
    k=p['kind']
    if k=='fixed':return SCENES[p['panel']]
    if k=='mouth':return mouth_art(p['state'])
    if k=='slab':return slab_art(0,0)
    if k in ['lower-empty','upper-empty']:
        s=rect(0,0,3,3,'#f0f4f3',INK,.04)
        for x in [1,2]:s+=line(x,0,x,3,GRID,.022)+line(0,x,3,x,GRID,.022)
        return s+(line(0,0,3,3,MUTED,.04)+line(0,3,3,0,MUTED,.04) if k=='upper-empty' else rect(.15,.15,2.7,2.7,'none',MUTED,.03))
    if k in ['room','room-empty']:
        s=rect(0,0,4,4,'white',INK,.035)
        for x in [1,2,3]:s+=line(x,0,x,4,GRID,.022)+line(0,x,4,x,GRID,.022)
        return s+(q3_art(.5,.5) if k=='room' else rect(.5,.5,3,3,'none',MUTED,.025))
    if k=='ship':return ship_art(0,0)
    if k=='anomaly':return anomaly_art(1.5,1.5)
    if k=='case':return case_art(.1,.18)
def size(g):
    x0,y0,x1,y1=g.bounds;return x1-x0,y1-y0

def art_svg(p,g):
    x0,y0,x1,y1=g.bounds;w,h=size(g)
    body=f'<defs><clipPath id="c">{outlines(g)}</clipPath></defs><g clip-path="url(#c)">'+outlines(g,'white','none',0)+artwork(p)+'</g>'
    return doc(body,w,h,f'{x0} {y0} {w} {h}',True)
manifest=[];panels=[]
for p in pieces:
    g=p['shape'];w,h=size(g);turn=w>10.7
    cutg=affinity.rotate(g,90,origin=(0,0)) if turn else g
    cw,ch=size(cutg)
    assert cw<=10.7 and ch<=13.7,(p['id'],cw,ch)
    x0,y0,x1,y1=cutg.bounds
    cutsvg=doc(outlines(cutg,'black','none',0),cw,ch,f'{x0} {y0} {cw} {ch}',True)
    (ROOT/'Chipboard'/f"{p['id']}.svg").write_text(cutsvg)
    # Split the printed skin independently of the backing. Conservative Letter rectangles.
    opts=[]
    for pw,ph in [(6.4,8.8),(8.8,6.4)]:
        nx=math.ceil(w/pw);ny=math.ceil(h/ph);opts.append((nx*ny,nx,ny))
    _,nx,ny=min(opts);x0,y0,x1,y1=g.bounds
    sub=[]
    for row in range(ny):
        for col in range(nx):
            cell=g.intersection(box(x0+col*w/nx,y0+row*h/ny,x0+(col+1)*w/nx,y0+(row+1)*h/ny)).buffer(0)
            if cell.area<1e-8:continue
            # One PNG can include several islands; keep their placement in the panel.
            ident=p['id']+f'-R{row+1}C{col+1}';a,b=size(cell);rotate=a>6.4+1e-6
            svg=art_svg(p,cell)
            imfile=ROOT/'Cardstock'/f'{ident}.png'
            cairosvg.svg2png(bytestring=svg.encode(),write_to=str(imfile),output_width=round(a*300),output_height=round(b*300))
            if rotate:
                im=Image.open(imfile);im.transpose(Image.Transpose.ROTATE_90).save(imfile)
            iw,ih=(b,a) if rotate else (a,b)
            assert iw<=6.40001 and ih<=8.80001,(ident,iw,ih)
            meta={'id':ident,'backing':p['id'],'width_inches':round(iw,6),'height_inches':round(ih,6),'rotation_ccw':90 if rotate else 0,'row':row+1,'column':col+1,'bounds':list(cell.bounds),'png':ident+'.png'}
            panels.append(meta);sub.append({'meta':meta,'shape':cell})
    p['panels']=sub
    manifest.append({'id':p['id'],'kind':p['kind'],'panel':p['panel'],'family':p.get('family'),'width_inches':round(cw,6),'height_inches':round(ch,6),'rotation_clockwise':90 if turn else 0,'map_width_inches':round(w,6),'map_height_inches':round(h,6),'panels':[x['meta']['id'] for x in sub],'cut_sha256':hashlib.sha256(cutsvg.encode()).hexdigest()})
for family in ['Q1','Q2','Q3']:assert len({m['cut_sha256'] for m in manifest if m['family']==family})==1

# Assembly map keeps IDs off the player artwork.
s=rect(0,0,90,66,'white','none')+text(3,3,'ASSEMBLY / 11 x 14 CHIPBOARD',1.3,weight='bold')+text(3,4.6,'32 finished pieces / 12 x 24 mat / one-inch squares / thin rust lines show backing joins',.62)
for panel,dx,dy in [('lower',-1,8),('upper',55,7),('deep',62,29)]:
    inner=SCENES[panel]
    for p in pieces:
        if p['kind']=='fixed' and p['panel']==panel:
            inner+=outlines(p['shape'],'none',ACCENT,.07);pt=p['shape'].representative_point()
            inner+=label(pt.x,pt.y,p['id'],.42,'middle')
    for name,g in slots[panel]:
        inner+=outlines(g,'#eef2ea',ACCENT,.1);pt=g.representative_point();inner+=label(pt.x,pt.y,name,.5,'middle')
    s+=transformed(inner,dx,dy)
for j,t in enumerate(['Q1: exchange the complete mouth strip. The entrance hall uses four permanent sections.',
 'Q2: move the slab between docks. Q3: exchange the occupied and empty berth inserts.',
 'Printed cardstock panels are permanently glued onto each named backing before play.',
 'Ship: one 10 x 11.8-inch hull plus a separate ramp. Anomaly and case remain movable tokens.']):s+=text(3,58+j*1.4,t,.58)
emit('GM-Assembly',doc(s,17,17*66/90,'0 0 90 66',True),True)

# Plain printing companion. Cricut users print PNGs through Design Space.
c=canvas.Canvas(str(ROOT/'Quantum-Cave-Player-Tiles-Letter.pdf'),pagesize=(612,792))
panel_shapes={sub['meta']['id']:sub['shape'] for p in pieces for sub in p['panels']}
for idx,m in enumerate(panels,1):
    c.setFont(RFONT,13);c.drawString(36,758,m['id']);c.setFont(RFONT,8)
    c.drawString(36,741,'Cardstock surface panel / glue onto '+m['backing'])
    c.drawString(36,727,'Hand-trim PDF: Actual Size / 100%. Cricut Print Then Cut: use the PNG through Design Space.')
    w=m['width_inches']*72;h=m['height_inches']*72
    c.drawImage(str(ROOT/'Cardstock'/m['png']),36,710-h,w,h,mask='auto')
    contour=panel_shapes[m['id']]
    if m['rotation_ccw']:contour=affinity.rotate(contour,-90,origin=(0,0))
    bx0,by0,bx1,by1=contour.bounds;pp=c.beginPath()
    for component in components(contour):
        for ring in [component.exterior]+list(component.interiors):
            coords=list(ring.coords);pp.moveTo(36+(coords[0][0]-bx0)*72,710-(coords[0][1]-by0)*72)
            for xx,yy in coords[1:]:pp.lineTo(36+(xx-bx0)*72,710-(yy-by0)*72)
            pp.close()
    c.setStrokeColorRGB(.6,.6,.6);c.setLineWidth(.25);c.drawPath(pp,stroke=1,fill=0)
    c.setFont(RFONT,8);c.drawString(36,52,f"Panel {idx}/{len(panels)} | PNG size {m['width_inches']:.3f} x {m['height_inches']:.3f} in")
    c.rect(36,28,72,8,stroke=1,fill=0);c.drawString(115,29,'One-inch calibration bar');c.showPage();m['pdf_page']=idx
c.save()

# Per-backing assembly sheets display cardstock seams and label the imported orientation.
c=canvas.Canvas(str(ROOT/'Backing-and-Panel-Guide.pdf'),pagesize=(612,792))
for p,m in zip(pieces,manifest):
    c.setFont(RFONT,16);c.drawString(36,755,p['id']);c.setFont(RFONT,9)
    c.drawString(36,735,f"Backing SVG: {m['width_inches']:.3f} x {m['height_inches']:.3f} in; {len(p['panels'])} cardstock panel(s).")
    c.drawString(36,720,'Diagram shows map orientation. R = row, C = column; north/top is the top of this diagram.')
    g=p['shape'];x0,y0,x1,y1=g.bounds;w,h=size(g);scale=min(510/w,485/h)
    # Render a reduced labeled construction diagram, retaining vector source in the kit.
    body=f'<defs><clipPath id="assembly">{outlines(g)}</clipPath></defs><g clip-path="url(#assembly)">'+outlines(g,'white','none',0)+artwork(p)+'</g>'+outlines(g,'none',ACCENT,.04)
    for sub in p['panels']:
        sh=sub['shape'];mm=sub['meta'];pt=sh.representative_point()
        body+=outlines(sh,'none',ACCENT,.045)+label(pt.x,pt.y,f"R{mm['row']}C{mm['column']}",.42,'middle')
    svg=doc(body,w,h,f'{x0} {y0} {w} {h}',True)
    png=cairosvg.svg2png(bytestring=svg.encode(),output_width=1200)
    c.drawImage(ImageReader(io.BytesIO(png)),36,695-h*scale,w*scale,h*scale,mask='auto')
    c.setFont(RFONT,8);yy=190
    for sub in p['panels']:
        mm=sub['meta'];rotate='; turn clockwise after cutting' if mm['rotation_ccw'] else ''
        c.drawString(36,yy,f"R{mm['row']}C{mm['column']}: {mm['width_inches']:.3f} x {mm['height_inches']:.3f} in{rotate}");yy-=13
    c.drawString(36,55,'Glue panels flush along the marked seams. Match grid lines; keep adhesive clear of tab edges.')
    c.drawString(36,42,'The finished backing is one tabletop piece. Printed seams remain permanently assembled.')
    c.showPage()
c.save()

# Fit coupons use the same broad connector as the complete kit.
testdir=ROOT/'Connector-Test';testdir.mkdir(exist_ok=True)
c=canvas.Canvas(str(ROOT/'Connector-Test-Sheet.pdf'),pagesize=(612,792));c.setFont(RFONT,17);c.drawString(36,755,'Connector fit test / complete laminated sample')
c.setFont(RFONT,9);c.drawString(36,735,'Test cardstock glued to your chipboard. Main-kit outlines use zero added clearance.')
for row,gap in enumerate([0,.005,.01,.015]):
    shapes=[box(0,0,1.5,1.5).union(peg(1.5,.75)),box(1.5,0,3,1.5).difference(peg(1.5,.75).buffer(gap))]
    for col,g in enumerate(shapes):
        name=f'{int(gap*1000):03}-'+('Tab' if col==0 else 'Socket');x0,y0,x1,y1=g.bounds;w,h=size(g)
        cut=doc(outlines(g,'black','none',0),w,h,f'{x0} {y0} {w} {h}',True)
        (testdir/f'{name}.svg').write_text(cut)
        art=doc(outlines(g,'white',INK,.015)+text((x0+x1)/2,.72,name,.13,INK,'middle'),w,h,f'{x0} {y0} {w} {h}',True)
        cairosvg.svg2png(bytestring=art.encode(),write_to=str(testdir/f'{name}.png'),output_width=round(w*300),output_height=450)
        c.drawImage(str(testdir/f'{name}.png'),45+col*200,580-row*145,w*72,h*72,mask='auto')
    c.drawString(45,565-row*145,f'Socket clearance: {gap:.3f} inch. Tab PNG/SVG: 1.900 x 1.500 in; socket: 1.500 x 1.500 in.')
c.save()

# Guide text uses measured wrapping and explicit page limits.
def write_page(c,title,paragraphs):
    c.setFont(RFONT,17);c.setFillColor(HexColor(INK));c.drawString(38,752,title);y=724
    for heading,body in paragraphs:
        c.setFont(RFONT,10.5);c.drawString(38,y,heading);y-=16;c.setFont(RFONT,9)
        linebuf=''
        for word in body.split():
            trial=(linebuf+' '+word).strip()
            if pdfmetrics.stringWidth(trial,RFONT,9)>536:c.drawString(38,y,linebuf);y-=12;linebuf=word
            else:linebuf=trial
        if linebuf:c.drawString(38,y,linebuf);y-=12
        y-=12
    assert y>35,(title,y);c.showPage()
c=canvas.Canvas(str(ROOT/'Setup-and-Navigation.pdf'),pagesize=(612,792))
write_page(c,'Build and play / 32 finished pieces',[
 ('Materials and scale','Use 11 x 14-inch chipboard on a 12 x 24-inch mat. Every backing fits a 10.7 x 13.7-inch envelope after its supplied rotation. One grid square measures one inch and represents five feet. Blade and material settings depend on the thickness and density of your chipboard.'),
 ('Cardstock / printing','Upload PNGs from Cardstock as Flat Graphic / Print Then Cut. Preserve white interior areas and the transparent exterior. Enter the dimensions in the panel guide or manifest; each PNG is at 300 pixels per inch. Use Letter paper and print through Design Space so it supplies the registration marks. Each panel fits within a conservative 6.4 x 8.8-inch rectangle.'),
 ('Chipboard / backing cuts','Upload the named SVG from Chipboard as Basic Cut. Check its dimensions against the guide, select a 12 x 24-inch mat and position the 11 x 14-inch stock to cover the cut. Some backing SVGs are rotated 90 degrees for the stock. Printed panels and the assembly diagrams use the map orientation.'),
 ('One-image option for small pieces','For a backing with one cardstock panel, you can duplicate its imported PNG and change the duplicate to Basic Cut. If its orientation differs from the backing SVG, rotate it to fit the stock. Keep both copies at the same physical scale. The separate SVG provides the exact designed contour. Large backings use one SVG and several printed panels.'),
 ('Glue and assemble','Use Backing-and-Panel-Guide.pdf to arrange the printed panels on each backing. R1C1 starts at the top left of the diagram. Match the grid across seams and glue each panel flush to its neighbor. Label the underside with the backing name and let it dry flat. Panels stay glued together during play.'),
 ('Connector fit','The fit-test folder contains four tab/socket pairs with socket clearances of 0, 0.005, 0.010 and 0.015 inch. Test the complete cardstock-and-chipboard construction. Main-kit contours use zero added clearance. If your preferred fit needs a larger socket, use that result to request a contour adjustment before cutting the full kit.'),
 ('Reveal and pack','Place a whole room or its named sections when discovered. Reveal corridors as the party follows them. Keep the three entrance-state strips together, Q2 inserts together, and Q3 inserts together. Store the hull flat with its ramp beside it. The complete player atlas reveals the full configuration when displayed.'),
 ('Ship','The hull is one backing measuring 10 x 11.8 inches, representing approximately 50 x 60 feet. Its separate ramp meets the port hull contour. The exterior supports boarding, repairs and extraction. A future interior map can establish cabins, shared living space, storage and machinery.')])
write_page(c,'Navigation and quantum states',[
 ('Fixed routes','Area 1 connects south through two bends to area 2. The junction branches west to area 3 and east to area 4; those branches enter their destination rooms from the north. The low tunnel joins area 3 east to area 4 west. It is five feet wide with a four-foot ceiling.'),
 ('Elevations','Matching L markers connect the lift docks, 20 feet apart vertically. Matching S markers connect the gallery stairs to their broken end over the junction: five feet of stair descent followed by a 15-foot gap. Insets have independent page positions and share north-up orientation.'),
 ('Q1 / entrance','The entire hall changes state: Bright-Side > Dark-Side > Underground > Bright-Side. Its fixed southern connection persists. Keep the four floor backings in place and exchange the single mouth strip. The ship belongs to the Underground state until preserved by observation during extraction.'),
 ('Q2 / lift','The three-square slab alternates between lower and upper docks. Move the slab insert and fill the vacated dock with the appropriate empty insert. The maintenance case belongs to the Upper state and is a separate token.'),
 ('Q3 / traveling room','The enclosed three-square room alternates between Gallery and Deep. Its four-square physical insert includes fixed berth clearance. Exchange the occupied and empty inserts. Berth slates can display a view of the room to establish observation for recovery.'),
 ('Observation','A recognizable observed part stabilizes the whole quantum feature. An ordinary blink preserves observation; deliberately looking away or closing eyes releases it. The final observer releasing a feature advances it once, followed by a fresh observation and release for another change. Tethers, occupied boundaries and blocked destinations constrain transitions.'),
 ('Separate objects','Keep observing the ship while releasing Q1 to carry it into Bright-Side. Likewise, watching the case preserves it when Q2 changes. Releasing either object away from its home state while it remains on its host returns that object and its occupants home. Carrying the case off the slab or flying the ship fully clear ends this constraint.'),
 ('Anomaly contact','The party receives the vision, Parted the Fabric and their GM-assigned abilities, then returns with Q3 to Gallery. Remove the anomaly token. Later Deep visits reach the empty replacement grotto. Retain the current Q1 and Q2 states; the after-contact atlas page uses B-L-G only as an example.')])
write_page(c,'State atlas index',[(f'{i:02} / {"-".join(st)}',f'{Q1[st[0]].title()}; lift {Q2[st[1]].lower()}; traveling room at {Q3[st[2]].lower()}.') for i,st in enumerate(STATES,1)])
for start in range(0,len(manifest),32):
    c.setFont(RFONT,16);c.drawString(38,752,'Backing inventory / dimensions as imported')
    c.setFont(RFONT,8);c.drawString(38,730,'Backing ID');c.drawString(280,730,'Width x height (inches)');c.drawString(460,730,'Cardstock panels');y=710
    for m in manifest[start:start+32]:
        c.drawString(38,y,m['id']);c.drawString(280,y,f"{m['width_inches']:.3f} x {m['height_inches']:.3f}");c.drawString(485,y,str(len(m['panels'])));y-=19
    c.showPage()
c.save()
gm=PdfWriter();gm.append(gmfiles[0])
for name in ['GM-Plate-Q1','GM-Plate-Q2','GM-Plate-Q3','GM-Assembly']:gm.append(ROOT/'maps'/f'{name}.pdf')
gm.append(ROOT/'Setup-and-Navigation.pdf');atlas_start=len(gm.pages)+1
for f in gmfiles:gm.append(f)
for name in ['GM-After-Contact','GM-Ship-Escape']:gm.append(ROOT/'maps'/f'{name}.pdf')
gm.write(ROOT/'Quantum-Cave-GM-Packet.pdf')
pl=PdfWriter()
for f in pfiles:pl.append(f)
for name in ['Players-After-Contact','Players-Ship-Escape']:pl.append(ROOT/'maps'/f'{name}.pdf')
pl.write(ROOT/'Quantum-Cave-Players.pdf')
assert len(pieces)==32,len(pieces)
assert lower.geom_type=='Polygon' and lower.is_valid
assert not lower.covers(LineString([(30,17),(33,28)]))
assert not upper.covers(LineString([(18.5,8.5),(29,9)]))
for panel,ss in slots.items():
    for name,g in ss:assert bodies[panel].covers(g),(panel,name)
for p in pieces:
    gg=unary_union([sub['shape'] for sub in p['panels']]);assert gg.symmetric_difference(p['shape']).area<1e-7,p['id']
(ROOT/'manifest.json').write_text(json.dumps({'backings':manifest,'cardstock_panels':panels},indent=2))
validation={'finished_pieces':len(pieces),'fixed_sections':sum(p['kind']=='fixed' for p in pieces),'printed_panels':len(panels),'state_maps':len(STATES),'gm_pages':len(gm.pages),'state_atlas_first_page':atlas_start,'stock_envelope_inches':[10.7,13.7],'cardstock_envelope_inches':[6.4,8.8],'fixed_coverage_exact':True,'fixed_overlap_area':0,'artwork_panel_coverage_exact':True,'matching_quantum_families':['Q1','Q2','Q3'],'physical_cut_test':'pending','joints':len(joints)}
(ROOT/'source'/'validation.json').write_text(json.dumps(validation,indent=2));print(json.dumps(validation))
