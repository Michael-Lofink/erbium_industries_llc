from pathlib import Path
import base64, io, json, re, shutil, math, html
import xml.etree.ElementTree as ET
import cairosvg
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Frame, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT.parent/'quantum-cave-map-v3'
VAULT=Path('/home/michaellofink/Documents/Erbium Industries LLC')
INK='#24596b'; GOLD='#b16436'; LIGHT='#e6eff0'; PURPLE='#75528d'
for p in ['Maps','Cricut/Artwork','Cricut/Cuts']: (ROOT/p).mkdir(parents=True,exist_ok=True)
font=Path('/usr/share/fonts/open-sans/OpenSans-Regular.ttf')
bold=font.with_name('OpenSans-Bold.ttf')
pdfmetrics.registerFont(TTFont('DejaVu',str(font)))
pdfmetrics.registerFont(TTFont('DejaVu-Bold',str(bold)))
pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVu-Bold',italic='DejaVu',boldItalic='DejaVu-Bold')

def text(x,y,s,size=12,color=INK,anchor='start',weight='normal'):
    s=s.replace('↔','/').replace('→','>')
    return f'<text x="{x}" y="{y}" font-family="DejaVu Sans,sans-serif" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{html.escape(s)}</text>'
def svg(body,w,h,vb=None):
    return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}in" height="{h}in" viewBox="{vb or f"0 0 {w*100} {h*100}"}">{body}</svg>'
def render(name,raw,width=2200,pdf=True):
    p=ROOT/'Maps'/name
    p.with_suffix('.svg').write_text(raw)
    cairosvg.svg2png(bytestring=raw.encode(),write_to=str(p.with_suffix('.png')),output_width=width)
    if pdf:cairosvg.svg2pdf(bytestring=raw.encode(),write_to=str(p.with_suffix('.pdf')))

# Existing map geometry and art are retained; only GM overlays are added.
raw=(OLD/'maps/GM-05-D-L-G.svg').read_text()
raw=raw.replace('Each feature changes independently after its final observer releases it. Rust dashed circles: 10-ft vent bursts.',
                'Q1-Q3: observation cycles. J / H1 / H2: movable cover; see placement sheet. Rust circles: vent bursts.')
raw=raw.replace('Ship/case shown at home states. Track carried objects separately; the appendix includes the ship escape state.',
                'Start: Dark-Side / Lower / Gallery. Ship at Underground. OutCry IV needs settlement components.')
positions={'J':[(29.5,31.5),(33.5,31.5)],'H1':[(10.5,37.5),(10.5,40.5)],'H2':[(15.5,39.5),(10.5,43.5)]}
colors={'J':PURPLE,'H1':GOLD,'H2':'#237c78'}
overlay='<g transform="translate(-1,8)">'
for k,pts in positions.items():
    for letter,(x,y) in zip('AB',pts):
        overlay+=f'<rect x="{x-.5}" y="{y-.5}" width="1" height="1" rx=".12" fill="white" fill-opacity=".9" stroke="{colors[k]}" stroke-width=".11"/>'
        overlay+=text(x,y+.12,k+letter,.34,colors[k],'middle','bold')
overlay+='</g>'
raw=raw.replace('</svg>',overlay+'</svg>')
render('Quantum-Cave-Navigation',raw,2800)

# Separate close-up plate for placing one-square additions on the built map.
root=ET.fromstring(raw); ns={'s':'http://www.w3.org/2000/svg'}
lower=next(g for g in root.findall('s:g',ns) if g.attrib.get('transform','').startswith('translate(-1,8)'))
lowcontent=''.join(ET.tostring(e,encoding='unicode') for e in list(lower))
def crop(x,y,w,h,X,Y,W,H):
    return f'<svg x="{X}" y="{Y}" width="{W}" height="{H}" viewBox="{x} {y} {w} {h}">{lowcontent}</svg>'
body='<rect width="1100" height="850" fill="white"/>'
body+=text(40,42,'QUANTUM COVER • PLACEMENT',24,weight='bold')
body+=text(40,68,'Same map geometry • north up • 5-foot squares • all stones start at A',12)
body+=crop(26,26,10,10,40,110,410,410)
body+='<rect x="40" y="110" width="220" height="22" fill="white"/>'
body+=text(40,125,'Stair ends 15 ft above floor',12)
body+=crop(2,35,16,12,490,110,570,427.5)
# Place markers again because original room group predates overlay.
for k,pts in positions.items():
    for letter,(x,y) in zip('AB',pts):
        if k=='J':X=40+(x-26)*41;Y=110+(y-26)*41;u=41
        else:X=490+(x-2)*35.625;Y=110+(y-35)*35.625;u=35.625
        body+=f'<rect x="{X-u/2}" y="{Y-u/2}" width="{u}" height="{u}" rx="4" fill="white" stroke="{colors[k]}" stroke-width="3"/>'
        body+=text(X,Y+5,k+letter,12,colors[k],'middle','bold')
body+=text(40,555,'J • Junction stone',19,weight='bold')+text(490,555,'H1 / H2 • Feeding Hollow',19,weight='bold')
lines=[
('J: white-striped stone beside the buttress.',40,590),
('White-striped H1 / split-topped H2.',490,590),
('At round start, each unstabilized stone moves A ↔ B.',40,640),
('Fix Your Gaze: 1 action; holds one stone through the next round-start shift.',40,668),
('Occupied destination or a creature standing on the stone: it stays this round.',40,696),
('Each stone occupies one square and grants standard cover across its position.',40,724),
('Existing printed buttresses, nests and vents remain fixed.',40,752),
('Cut 3 stone tiles. The 6 small position markers are optional paper pieces.',40,792)]
for s,x,y in lines:body+=text(x,y,s,15)
render('Quantum-Cover-Placement',svg(body,11,8.5),2400)

# Rendered companion to the guide's editable Mermaid flowchart.
body='<rect width="700" height="650" fill="white"/><defs><marker id="arrow" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto-start-reverse"><path d="M0 0L6 3L0 6" fill="none" stroke="#24596b"/></marker></defs>'
nodes={'1':(350,50,'1  Entrance Hall / Q1'),'2':(350,155,'2  Nest Junction'),'3':(135,270,'3  Feeding Hollow'),'4':(565,270,'4  Lift Cavern / Q2'),'5':(350,390,'5  Upper Gallery'),'T':(350,490,'Q3  Traveling Room'),'6':(350,590,'6  Anomaly Grotto')}
def edge(d,dash=False):return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="2" marker-start="url(#arrow)" marker-end="url(#arrow)"'+(' stroke-dasharray="6 5"' if dash else '')+'/>'
body+=edge('M350 78 L350 127')+text(365,108,'Two bends',12)
body+=edge('M270 183 L135 242')+text(157,207,'West passage',12)
body+=edge('M430 183 L565 242')+text(466,207,'East passage',12)
body+=edge('M238 270 L462 270')+text(350,257,'Low tunnel: 4-ft ceiling',12,anchor='middle')
body+=edge('M565 298 L565 340 L430 362')+text(563,331,'Lift / climb 20 ft',12,anchor='end')
body+=edge('M350 183 L350 230 L285 230 L285 332 L310 362')
body+=text(288,316,'Stairs: 15-ft gap',11)
body+=edge('M350 418 L350 462',True)+text(365,445,'Gallery berth',12)
body+=edge('M350 518 L350 562',True)+text(365,545,'Deep berth',12)
for k,(x,y,s) in nodes.items():
    body+=f'<rect x="{x-103}" y="{y-27}" width="206" height="54" rx="7" fill="{LIGHT}" stroke="{INK}" stroke-width="1.5"/>'+text(x,y+5,s,14,anchor='middle',weight='bold')
render('Quantum-Cave-Flowchart',svg(body,7,6.5),1500)

# Existing state plates preserve the original assembly and all Q1-Q3 states.
for name in ['GM-Plate-Q1','GM-Plate-Q2','GM-Plate-Q3']:
    shutil.copy2(OLD/'previews'/f'{name}.png',ROOT/'Maps'/f'{name}.png')
    shutil.copy2(OLD/'maps'/f'{name}.pdf',ROOT/'Maps'/f'{name}.pdf')

# Flat tokens: the supplied creature portrait is placed in a circular layout.
portrait=VAULT/'Resources/creaturePortrait_Electrovore.webp'
im=Image.open(portrait)
buf=io.BytesIO(); im.save(buf,format='PNG')
data=base64.b64encode(buf.getvalue()).decode()
iw,ih=im.size
tokens=[]
def circlecut(w=1):return f'<circle cx="50" cy="50" r="50" fill="black"/>'
def stonecut():return '<rect x="0" y="0" width="100" height="100" rx="8" fill="black"/>'
def save_token(name,body,cut,w=1,h=1):
    art=svg(body,w,h,'0 0 100 100')
    cairosvg.svg2png(bytestring=art.encode(),write_to=str(ROOT/'Cricut/Artwork'/f'{name}.png'),output_width=round(w*600),output_height=round(h*600))
    (ROOT/'Cricut/Cuts'/f'{name}.svg').write_text(svg(cut,w,h,'0 0 100 100'))
    tokens.append({'name':name,'width_in':w,'height_in':h,'body':body,'cut':cut})

for n,col in enumerate([INK,GOLD,PURPLE,'#397f5d'],1):
    # The full source remains embedded; this portrait window makes the head legible at 1 inch.
    body='<defs><clipPath id="rim"><circle cx="50" cy="50" r="47"/></clipPath></defs>'
    body+=f'<circle cx="50" cy="50" r="50" fill="{col}"/><circle cx="50" cy="50" r="46" fill="#e5e0d2"/>'
    body+='<g clip-path="url(#rim)">'
    body+=f'<svg x="5" y="4" width="90" height="87" viewBox="0 {ih*.43} {iw*.86} {ih*.51}" preserveAspectRatio="xMidYMid slice"><image x="0" y="0" width="{iw}" height="{ih}" xlink:href="data:image/png;base64,{data}"/></svg></g>'
    body+=f'<circle cx="72" cy="72" r="14" fill="{col}" stroke="white" stroke-width="2"/>'+text(72,78,str(n),19,'white','middle','bold')
    save_token(f'Electrovore-{n}-1in',body,circlecut())

for key in ['J','H1','H2']:
    col=colors[key]
    body=f'<rect width="100" height="100" rx="8" fill="{INK}"/><rect x="3" y="3" width="94" height="94" rx="6" fill="#e7ece9"/>'
    body+='<path d="M13 24L29 9L69 12L88 33L86 73L66 90L23 85L9 59Z" fill="#b8c4c2" stroke="#24596b" stroke-width="2"/>'
    body+='<path d="M29 9L36 36L13 24M36 36L66 29L69 12M66 29L70 66L86 73M70 66L42 75L23 85M42 75L36 36M9 59L42 75" fill="none" stroke="#718e94" stroke-width="1.5"/>'
    if key=='H2':body+='<path d="M52 13L42 38L60 49L47 69L58 88" fill="none" stroke="#24596b" stroke-width="5"/>'
    else:body+='<path d="M12 57L36 46L61 51L87 36" fill="none" stroke="white" stroke-width="7"/>'
    body+=f'<rect x="32" y="70" width="36" height="24" rx="5" fill="{col}"/>'+text(50,88,key,16,'white','middle','bold')
    save_token(f'{key}-Stone-1in',body,stonecut())

for key in ['J','H1','H2']:
    for letter in 'AB':
        col=colors[key]
        body=f'<circle cx="50" cy="50" r="50" fill="{col}"/><circle cx="50" cy="50" r="43" fill="white"/>'
        body+=text(50,43,key,28,col,'middle','bold')+text(50,77,letter,32,col,'middle','bold')
        save_token(f'{key}-{letter}-Marker-half-inch',body,circlecut(),.5,.5)

# One arranged transparent Print Then Cut sheet with matching Basic Cut silhouettes.
# Tight bounds: 4.75 x 3.5 inches. Numbered creatures, stones, optional markers.
layout=[(0,0),(1.25,0),(2.5,0),(3.75,0),(0,1.25),(1.25,1.25),(2.5,1.25),
        (0,3),(0.75,3),(1.5,3),(2.25,3),(3,3),(3.75,3)]
artbody='';cutbody=''
for i,(t,(x,y)) in enumerate(zip(tokens,layout)):
    b=t['body'].replace('id="rim"',f'id="rim{i}"').replace('url(#rim)',f'url(#rim{i})')
    artbody+=f'<g transform="translate({x*100},{y*100}) scale({t["width_in"]})">{b}</g>'
    cutbody+=f'<g transform="translate({x*100},{y*100}) scale({t["width_in"]})">{t["cut"]}</g>'
sheet=svg(artbody,4.75,3.5)
cairosvg.svg2png(bytestring=sheet.encode(),write_to=str(ROOT/'Cricut/All-Pieces-Print-Then-Cut.png'),output_width=2850,output_height=2100)
(ROOT/'Cricut/All-Pieces-Basic-Cut.svg').write_text(svg(cutbody,4.75,3.5))
(ROOT/'Cricut/Required-Seven-Backings.svg').write_text(svg(''.join(f'<g transform="translate({x*100},{y*100})">{t["cut"]}</g>' for t,(x,y) in zip(tokens[:7],layout[:7])),4.75,2.25))
(ROOT/'source/token-manifest.json').write_text(json.dumps([{k:v for k,v in t.items() if k not in ['body','cut']} for t in tokens],indent=2))

# Letter sheet for hand cutting / print scale checks.
c=canvas.Canvas(str(ROOT/'Cricut/Manual-Cut-Letter.pdf'),pagesize=(612,792))
c.setTitle('Quantum Cave: Add-on Pieces at Actual Size')
c.setAuthor('Erbium Industries LLC campaign')
c.setFillColor(HexColor(INK));c.setFont('DejaVu-Bold',17);c.drawString(40,744,'QUANTUM CAVE • ADD-ON PIECES')
c.setFont('DejaVu',10);c.drawString(40,723,'Actual size / 100% • 1 inch = 5 feet • Letter paper')
for t,(x,y) in zip(tokens,layout):
    c.drawImage(str(ROOT/'Cricut/Artwork'/f'{t["name"]}.png'),55+x*72,630-y*72-t['height_in']*72,width=t['width_in']*72,height=t['height_in']*72,mask='auto')
c.setFont('DejaVu',11)
for y,s in [(654,'Electrovores 1–4: 1-inch bases'),(554,'J, H1, H2: 1-inch terrain pieces'),(428,'Optional A/B markers: ½-inch paper circles'),(326,'Seven backed pieces; six optional position markers.'),(306,'For Cricut Print Then Cut, upload the transparent PNG in Design Space.'),(286,'This PDF supports ordinary printing and hand cutting.')]:c.drawString(40,y,s)
c.rect(40,173,72,72);c.drawString(126,205,'Check: this square must measure exactly 1 inch.')
c.setFont('DejaVu',8);c.drawString(40,65,'Creature portrait: supplied campaign resource / Paizo. Personal tabletop use.')
c.save()

# Four-page landscape quick-reference PDF.
W,H=792,612
c=canvas.Canvas(str(ROOT/'Quantum-Cave-Table-Reference.pdf'),pagesize=(W,H))
c.setTitle('Quantum Cave: Session 4 GM Table Reference')
c.setAuthor('Erbium Industries LLC campaign')
style=ParagraphStyle('body',fontName='DejaVu',fontSize=9.2,leading=13,spaceAfter=7,textColor=HexColor(INK))
small=ParagraphStyle('small',parent=style,fontSize=8.3,leading=11.5,spaceAfter=6)
head=ParagraphStyle('head',parent=style,fontName='DejaVu-Bold',fontSize=13,leading=17,spaceBefore=9,spaceAfter=6)
def top(title,num):
    c.setFillColor(HexColor(INK));c.setFont('DejaVu-Bold',19);c.drawString(30,H-35,title)
    c.setFont('DejaVu',8);c.drawString(30,16,'QUANTUM CAVE • SESSION 4 • GM REFERENCE');c.drawRightString(W-30,16,str(num))
def paras(items,x,y,w,h,st=style):
    fs=[]
    for item in items:
        if isinstance(item,tuple):fs.append(Paragraph(html.escape(item[1]),head))
        else:fs.append(Paragraph(item.replace('↔',' / ').replace('→',' &gt; ').replace('◆','(1 action)'),st))
    frame=Frame(x,y,w,h,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
    frame.addFromList(fs,c)
    if fs:raise RuntimeError(f'PDF overflow: {len(fs)} paragraphs at {x},{y}')

top('Quantum Cave: navigation',1)
c.drawImage(str(ROOT/'Maps/Quantum-Cave-Navigation.png'),28,50,width=736,height=501,preserveAspectRatio=True,anchor='c',mask='auto')
c.setFont('DejaVu',9);c.drawString(30,35,'Start: Dark-Side / Lower / Gallery. Ship: Underground. J, H1 and H2 start at A.')
c.showPage()

top('Connections and quantum states',2)
c.drawImage(str(ROOT/'Maps/Quantum-Cave-Flowchart.png'),22,156,width=380,height=385,preserveAspectRatio=True,mask='auto')
paras([
('h','Live tracker'),
'<b>Q1:</b> Dark-Side → Underground → Bright-Side → Dark-Side. Current: __________',
'<b>Q2:</b> Lower ↔ Upper. Current: __________',
'<b>Q3:</b> Gallery ↔ Deep. Current: __________',
'<b>Ship:</b> home Underground. <b>Case:</b> home Upper.',
'<b>Stones:</b> J ____ H1 ____ H2 ____; each starts A.',
('h','Observation'),
'Seeing a recognizable part holds Q1–Q3. Final observation ends: advance one state. Each new shift needs fresh observation and release. Deliberately close eyes or look away; ordinary blinking maintains the hold.',
'Darkvision and autonomous visual sensors count. Watched current photos and clear live feeds count. Photos become stale after a shift. One feature per observer in encounters.',
'Passengers entirely inside Q1/Q3 or supported by Q2 travel. A boundary-straddler, tether or unsafe occupied destination blocks the shift.',
('h','Exterior timing'),
'Leaving Dark-Side unobserved sends it Underground; natural Bright-Side resurfacing takes 1d4+1 days. Deliberate interior cycles remain immediate in this revision.'
],420,74,342,475,small)
paras(['<b>To the anomaly:</b> 1 → 2 → 4 → 5 → Q3 → 6. Area 3 links 2 and 4.',
       '<b>After the vision:</b> return in Q3 at Gallery. Descend the west stairs and rope to 2, or use Q2; then return through the two-bend passage to 1.',
       '<b>Q3 recovery:</b> watch its silver seam on a berth’s camera slate, then look away. The empty room changes berth when its final observer releases it.'],30,38,365,115,small)
c.showPage()

top('Room reference',3)
roomcards=[
('1  Entrance Hall • 120 × 80 ft',
'<b>North:</b> exterior. <b>South:</b> two bends to 2. White mineral boundary encloses quantum floor, walls, ceiling and opening. Landing-gear marks and boarding step identify the berth.',
'<b>Dark / Bright:</b> surface opening, empty berth at home. <b>Underground:</b> solid rock beyond opening; OutCry IV in berth, ramp down. First release from Dark sends Q1 Underground.'),
('2  Nest Junction • 40 ft across',
'<b>North:</b> 1. <b>West:</b> north entrance of 3. <b>East:</b> northeast entrance of 4. <b>Overhead:</b> gallery stair ends 15 ft up.',
'Fixed buttress and exhausted vent crust. Salvage cable follows east passage. <b>J</b> moves between A/B beside the buttress. Rope on the stairs gives a direct gallery route.'),
('3  Feeding Hollow • 70 × 50 ft',
'<b>North:</b> 2. <b>East:</b> low tunnel to 4, 5 ft wide / 4 ft high. <b>West:</b> three nests. Fixed printed buttresses. <b>V1:</b> upper western vent. <b>V2:</b> lower western vent.',
'One visible electrovore feeds beside V1. Further creatures can shelter in nest recesses. Eastern route skirts the vent bursts. <b>H1 / H2:</b> shifting one-square cover; start A.'),
('4  Lift Cavern • 50 × 40 ft',
'<b>Northeast:</b> 2. <b>West:</b> low tunnel to 3. <b>North:</b> fixed cliff, gallery ledge 20 ft up. <b>Q2:</b> 15-ft-square spiral slab.',
'Lower ↔ Upper. Board entirely, release slab, then watch again to hold at arrival. Yellow case appears at Upper. Fixed cliff permits climbing.'),
('5  Upper Gallery / Q3',
'<b>South:</b> lift dock. <b>West:</b> stairs descend 5 ft, then 15-ft gap to 2. <b>East:</b> sight-blocking dogleg to Q3. <b>V3:</b> vent near stairs.',
'Q3: 15-ft room in 20-ft berth; east-facing door. Entire room and curtain move Gallery ↔ Deep. Enter, close curtain, close eyes, then look again on arrival. Both berths have recovery slates.'),
('6  Anomaly Grotto • 60 × 50 ft',
'<b>West:</b> Q3 berth. <b>Center:</b> faceted anomaly over depression. Floor and walls fixed.',
'Contact: whole-team vision; Parted the Fabric and assigned abilities. Return inside Q3 at Gallery. Future Deep trips reach the empty replacement grotto, with recovery slate.')]
for i,(title,a,b) in enumerate(roomcards):
    col=i//3;row=i%3;x=30+col*381;y=380-row*169
    c.setStrokeColor(HexColor('#c5d5d9'));c.line(x,y+163,x+351,y+163)
    paras([('h',title),a,b],x,y,351,158,small)
c.showPage()

top('Encounter, repairs and departure',4)
paras([
('h','Moving stones: J / H1 / H2'),
'Each occupies one square, blocks movement through it and grants standard cover across its position. Outside combat, release of observation changes A ↔ B.',
'<b>Combat:</b> at round start, each unstabilized stone changes to its other position. Occupied destination or a creature standing on the stone: it stays for that round.',
'<b>Fix Your Gaze ◆:</b> choose a visible stone. Hold it through the next round-start shift while maintaining line of sight. Other actions are available. Losing sight releases it; the hold ends after the shift.',
('h','Electrovores'),
'Small; use one-inch numbered tokens. Darkvision observes quantum features. Electricsense detects electrical activity imprecisely. Immune to electricity; fly 20 ft. Feed beside vents, investigate powered gear, retreat toward nests after feeding or injury. Use the creature note for the selected version’s statistics.',
('h','Chuckle Vents'),
'V1/V2 in Feeding Hollow; V3 near gallery stairs. Junction crust is exhausted. Warning: trembling dust, comm interference, blue sparks.',
'Trigger: step on crust within 5 ft, break or disturb it. <b>10-ft burst; DC 17 basic Reflex; 2d6 electricity.</b> Recharges in 10 minutes.',
'<b>Survival DC 14, trained:</b> observe safely for 1 minute to find a lull for crossing. <b>Crafting DC 17, trained:</b> 2 actions adjacent, tools and conductive scrap; discharge for 10 minutes. Failure leaves it active; critical failure triggers it. Remote crust-breaking also triggers it.'
],30,43,351,505,small)
paras([
('h','State-bound objects'),
'<b>Case home: Upper. Ship home: Underground.</b> Watch the object while releasing the host’s stone to carry it with the shift. Interior views and valid images count.',
'Release the object away from home while it remains on the host: it returns home with occupants; host stays. Carry the case fully off Q2 or fly the ship fully beyond Q1 to end the binding.',
('h','OutCry IV inspection'),
'Stripped equipment mounts and disconnected services reveal cannibalization. Essential systems now keep Fresh-Breath habitable. Full repair depends on recovering settlement components.',
'Cable, case fittings and wreck salvage support partial repairs. Drift Eikon escape also needs a survivable hull and passenger support. Repair jobs and DCs remain to be set.',
'<b>Back for parts:</b> Underground → Bright-Side → Dark-Side through separate observation cycles.',
('h','Launch sequence'),
'1. Repair and board in Underground. Watch the ship’s interior.<br/>2. Disconnect tethers, close ramp and cover exterior views. Release every observer and valid image of Q1.<br/>3. Underground → Bright-Side; watched ship travels with it.<br/>4. Hold ship and hall while uncovering cockpit views. Launch fully across Q1’s boundary.',
('h','Cave music'),
'Explore: <b>The Uncertainty Principle</b>.<br/>Fight: <b>Robot Getaway</b>.<br/>Reveal: <b>The Nomai</b>.<br/>Vision: <b>The Ash Twin Project</b>.'
],411,43,351,505,small)
c.save()
print('Generated maps, 13 token images/cut files, Letter sheet and four-page table reference.')
