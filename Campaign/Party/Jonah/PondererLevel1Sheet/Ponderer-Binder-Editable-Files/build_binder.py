"""Build Ponderer's printable reference and editable, self-contained HTML.
Run with Python 3, reportlab and pymupdf. Content lives in binder-content.json.
"""
from pathlib import Path
import json, re, html, shutil, io, base64
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
ROOT=Path(__file__).resolve().parent
CONTENT=json.loads((ROOT/'binder-content.json').read_text())
PAGES,GM_PAGES,SECTIONS=CONTENT['pages'],CONTENT['gm_pages'],CONTENT['sections']
FONT_ROOT=Path('/usr/share/fonts/open-sans')
for name, fn in [('Body','OpenSans-Regular.ttf'),('Bold','OpenSans-Bold.ttf'),('Italic','OpenSans-Italic.ttf')]:
    local=ROOT/'fonts'/fn
    p=local if local.exists() else FONT_ROOT/fn
    pdfmetrics.registerFont(TTFont(name,str(p)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='Bold')
symbol_path=ROOT/'fonts'/'NotoSansMath-Regular.ttf'
if not symbol_path.exists():symbol_path=Path('/usr/share/fonts/google-noto/NotoSansMath-Regular.ttf')
pdfmetrics.registerFont(TTFont('Symbols',str(symbol_path)))
IDS={p['id'] for p in PAGES+GM_PAGES}
LINK_IDS=set()
ID_RE=re.compile(r'(?<![A-Za-z0-9])('+ '|'.join(sorted(IDS,key=len,reverse=True)) + r')(?![A-Za-z0-9])')
W,H=612,792
X,RIGHT=82,572
CW=RIGHT-X
INK=HexColor('#18222c'); GRAY=HexColor('#50606c'); PALE=HexColor('#f2f5f7')
styles={
 'body':ParagraphStyle('body',fontName='Body',fontSize=14,leading=18.5,textColor=INK,spaceAfter=4),
 'small':ParagraphStyle('small',fontName='Body',fontSize=11,leading=14,textColor=GRAY),
 'cost':ParagraphStyle('cost',fontName='Bold',fontSize=13,leading=17,textColor=INK),
 'head':ParagraphStyle('head',fontName='Bold',fontSize=17,leading=21,textColor=INK),
 'title':ParagraphStyle('title',fontName='Bold',fontSize=25,leading=30,textColor=INK),
 'cell':ParagraphStyle('cell',fontName='Body',fontSize=14,leading=18,textColor=INK),
}

# The one-action polygons and reaction path are from Tarn's Detonate Mine SVG.
# The open free-action paths are from GibSession2Handouts.json.
REACTION='M31 28 L11 47 L1 64 L23 46 L52 34 L82 29 L118 31 L148 40 L169 52 L187 70 L197 94 L196 113 L189 129 L173 147 L155 159 L134 166 L146 117 L40 182 L159 207 L137 177 L178 169 L211 155 L240 131 L253 108 L256 82 L245 52 L220 27 L184 9 L147 1 L106 1 L63 11 Z'
def glyph_svg(kind):
    if kind=='R':
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 257 208" aria-label="reaction"><path fill="currentColor" d="{REACTION}"/></svg>'
    if kind=='F':
        return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" aria-label="free action"><g fill="none" stroke="currentColor" stroke-width="11" stroke-linejoin="miter"><path d="M50 5 L95 50 L50 95 L5 50 Z"/><path d="M5 50 L27.5 27.5 L50 50 L27.5 72.5 Z"/></g></svg>'
    n=int(kind)
    polygons=['12,36 25,23 38,36 25,49','48,0 31,17 49,36 31,54 48,72 84,36']
    for i in range(1,n):
        a=48+46*i
        polygons.append(f'{a},4 {a-15},19 {a+1},36 {a-15},53 {a},68 {a+32},36')
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s 72" aria-label="%s actions"><g fill="currentColor">%s</g></svg>' % (84+46*(n-1),n,''.join(f'<polygon points="{p}"/>' for p in polygons))

def path_draw(c,coords,fill=1,stroke=0):
    p=c.beginPath(); tokens=re.findall(r'[MLZ]|-?\d+(?:\.\d+)?',coords); i=0
    while i<len(tokens):
        cmd=tokens[i]; i+=1
        if cmd=='Z':p.close()
        else:
            x,y=float(tokens[i]),float(tokens[i+1]); i+=2
            (p.moveTo if cmd=='M' else p.lineTo)(x,y)
    c.drawPath(p,fill=fill,stroke=stroke)

def glyph(c,kind,x,y,h=18):
    if kind not in ['1','2','3','R','F']:return 0
    svg=glyph_svg(kind); vw,vh=map(float,re.search(r'viewBox="0 0 (\S+) (\S+)"',svg).groups())
    c.saveState(); c.translate(x,y); c.scale(h/vh,-h/vh); c.setFillColor(INK); c.setStrokeColor(INK)
    if kind=='R': path_draw(c,REACTION)
    elif kind=='F':
        c.setLineWidth(11)
        path_draw(c,'M50 5 L95 50 L50 95 L5 50 Z',0,1)
        path_draw(c,'M5 50 L27.5 27.5 L50 50 L27.5 72.5 Z',0,1)
    else:
        for raw in re.findall(r'points="([^"]+)"',svg):
            pts=[tuple(map(float,p.split(','))) for p in raw.split()]
            path_draw(c,'M'+' L'.join(f'{a} {b}' for a,b in pts)+' Z')
    c.restoreState();return vw*h/vh

def clean(s):
    s=s.replace('’',"'").replace('“','"').replace('”','"')
    s=ID_RE.sub(lambda m:'<link href="#'+m[0]+'">'+m[0]+'</link>' if m[0] in LINK_IDS else m[0],s)
    return re.sub('[→□]',lambda m:'<font name="Symbols">'+m[0]+'</font>',s)
def para(c,text,y,style='body',x=X,w=CW):
    p=Paragraph(clean(text),styles[style]); _,h=p.wrap(w,1000)
    p.drawOn(c,x,y-h);return y-h-3

def table(c,rows,y,widths=None,header=False,compact=False):
    widths=[CW/len(rows[0])]*len(rows[0]) if widths is None else [CW*w/sum(widths) for w in widths]
    data=[[Paragraph(clean(str(v)),styles['cell']) for v in row] for row in rows]
    t=Table(data,colWidths=widths,hAlign='LEFT')
    ts=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-1),.5,HexColor('#d4dce1'))]
    if header:ts+=[('BACKGROUND',(0,0),(-1,0),PALE)]
    if compact:ts+=[('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]
    t.setStyle(TableStyle(ts));_,h=t.wrap(CW,1000);t.drawOn(c,X,y-h);return y-h-10

def action(c,b,y,color):
    y-=1
    c.setStrokeColor(color);c.setLineWidth(1);c.line(X,y,RIGHT,y);y-=6
    y=para(c,b['title'],y,'head')
    cost=b.get('cost',''); g=b.get('glyph')
    if cost:
        gw=glyph(c,g,X,y+1) if g else 0
        y=para(c,cost,y,'cost',x=X+gw+8 if g else X,w=CW-gw-8 if g else CW)-2
    if b.get('before'):y=para(c,'<b>Requirements:</b> '+b['before'],y)
    if b.get('choices'):
        y=para(c,'<b>Choose one:</b>',y)
        for s in b['choices']:y=para(c,s,y,x=X+14,w=CW-14)
    for i,s in enumerate(b.get('steps',[]),1):
        c.setFillColor(color);c.circle(X+9,y-9,8,fill=1,stroke=0)
        c.setFillColor(white);c.setFont('Bold',10);c.drawCentredString(X+9,y-12,str(i))
        y=para(c,s,y,x=X+25,w=CW-25)
    if b.get('results'):
        for s in b['results']:y=para(c,s,y)
    if b.get('outcomes'):y=table(c,b['outcomes'],y,[1,3])
    if b.get('note'):y=para(c,b['note'],y)
    return y-2

def diagram(c,name,y,color):
    if name=='decisions':
        bx=X; bw=215; rx=X+275; rw=215; bh=78
        questions=[('Need help or safety now?','First Aid / medpatch: P5<br/>Move / Take Cover: B3'),('Want a team bonus?','Help attacks: Get ’Em! P1<br/>Learn / defend: P2'),('Have a useful target in range?','Strike: B1–B2<br/>Bon Mot / Demoralize: P3')]
        def box(x,top,w,txt):
            c.setFillColor(PALE);c.setStrokeColor(color);c.setLineWidth(1)
            c.roundRect(x,top-bh,w,bh,7,fill=1,stroke=1)
            para(c,txt,top-13,'cell',x+12,w-24)
        def arrow(x1,y1,x2,y2):
            c.setStrokeColor(color);c.line(x1,y1,x2,y2)
            if y1==y2:
                c.line(x2-5,y2+4,x2,y2);c.line(x2-5,y2-4,x2,y2)
            else:
                c.line(x2-4,y2+5,x2,y2);c.line(x2+4,y2+5,x2,y2)
        for question,result in questions:
            box(bx,y,bw,question);box(rx,y,rw,result)
            arrow(bx+bw+4,y-43,rx-4,y-43)
            c.setFillColor(INK);c.setFont('Bold',11);c.drawCentredString(bx+bw+30,y-34,'YES')
            arrow(bx+bw/2,y-bh-3,bx+bw/2,y-bh-33)
            c.setFont('Bold',11);c.drawString(bx+bw/2+8,y-bh-22,'NO')
            y-=bh+38
        box(bx,y,CW,'Move closer: B3 • Seek: G2<br/>Or Delay before taking actions: O3')
        return y-bh-15
    if name=='turns':
        examples=[('Attack and support', [('Get ’Em!','2','Strike included'),('Take Cover','1','if cover is available')]),('Move into range', [('Stride','1','up to my Speed'),('Get ’Em!','2','Strike included')]),('Set up a Will save', [('Bon Mot','1','within 30 feet'),('Get ’Em!','1','within 60 feet'),('Stride','1','or another 1-action option')]),('Pistol was put away', [('Draw pistol','1','free hand needed'),('Get ’Em!','2','loaded pistol needed')])]
        for title,steps in examples:
            y=para(c,title,y,'head'); bh=79; n=len(steps); gap=15; bw=(CW-gap*(n-1))/n
            for i,(label,g,detail) in enumerate(steps):
                x=X+i*(bw+gap);c.setFillColor(PALE);c.setStrokeColor(HexColor('#bac7d0'));c.roundRect(x,y-bh,bw,bh,5,fill=1,stroke=1)
                glyph(c,g,x+10,y-9,16)
                para(c,label,y-31,'cell',x+9,bw-18)
                para(c,detail,y-56,'small',x+9,bw-18)
                if i<n-1:
                    c.setStrokeColor(color);c.line(x+bw+2,y-42,x+bw+gap-3,y-42)
                    c.line(x+bw+gap-6,y-39,x+bw+gap-3,y-42);c.line(x+bw+gap-6,y-45,x+bw+gap-3,y-42)
            y-=bh+12
        return y
    if name=='cover':
        # Simple top-down diagram: cover depends on the attack's direction.
        top=y;size=36;cols=10;rows=3;x0=X+48
        c.setStrokeColor(HexColor('#d5dde2'));c.setLineWidth(.5)
        for k in range(cols+1):c.line(x0+k*size,y-rows*size,x0+k*size,y)
        for k in range(rows+1):c.line(x0,y-k*size,x0+cols*size,y-k*size)
        c.setFillColor(color);c.circle(x0+1.5*size,y-1.5*size,11,fill=1,stroke=0)
        c.setFillColor(INK);c.circle(x0+8.5*size,y-1.5*size,11,fill=1,stroke=0)
        c.setFillColor(HexColor('#7c8993'));c.rect(x0+4.5*size,y-2.5*size,10,2*size,fill=1,stroke=0)
        c.setFont('Bold',11);c.setFillColor(white);c.drawCentredString(x0+1.5*size,y-1.5*size-4,'P');c.drawCentredString(x0+8.5*size,y-1.5*size-4,'E')
        y-=rows*size+9
        return para(c,'P = Ponderer. E = enemy. The barrier can give cover along this attack line. The GM decides how much.',y,'small')-4
    if name=='magazine':
        y=para(c,'LOADED — ready to fire',y,'head')
        for k in range(10):
            x=X+29+(k%5)*94; yy=y-28-(k//5)*60
            c.setStrokeColor(color);c.setLineWidth(1.2);c.circle(x,yy,27,stroke=1,fill=0)
            c.setFillColor(GRAY);c.setFont('Body',11);c.drawCentredString(x,yy-4,str(k+1))
        y-=126
        y=para(c,'SPENT — return tokens here after firing',y,'head')
        c.setFillColor(PALE);c.setStrokeColor(color)
        c.roundRect(X,y-118,CW,118,7,fill=1,stroke=1)
        return y-130
    if name=='carbine_battery':
        y=para(c,'CHARGED — each pair powers one shot',y,'head')
        for k in range(5):
            x=X+49+k*97
            c.setStrokeColor(color);c.setFillColor(PALE)
            c.roundRect(x-37,y-145,74,143,7,fill=1,stroke=1)
            c.setFillColor(INK);c.setFont('Bold',10)
            c.drawCentredString(x,y-15,f'PAIR {k+1}')
            for off in [49,110]:
                c.setStrokeColor(color);c.setFillColor(white)
                c.circle(x,y-off,27,fill=1,stroke=1)
        y-=157
        y=para(c,'SPENT — used or empty charge spaces',y,'head')
        c.setFillColor(PALE);c.setStrokeColor(color)
        c.roundRect(X,y-118,CW,118,7,fill=1,stroke=1)
        return y-130
    if name=='carbine_tokens':
        for k in range(10):
            x=X+41+(k%5)*94;yy=y-30-(k//5)*66
            c.setStrokeColor(color);c.setLineWidth(1);c.circle(x,yy,27,fill=0,stroke=1)
            c.setFillColor(INK);c.setFont('Bold',9)
            c.drawCentredString(x,yy+5,'FED-12')
            c.drawCentredString(x,yy-9,'CHARGE')
        return y-141
    if name=='assets':
        gap=12;bw=(CW-2*gap)/3;h=128
        for i in range(3):
            x=X+i*(bw+gap)
            c.setStrokeColor(color);c.setFillColor(PALE)
            c.roundRect(x,y-h,bw,h,6,fill=1,stroke=1)
            c.setFillColor(INK);c.setFont('Bold',12)
            c.drawCentredString(x+bw/2,y-16,f'ASSET {i+1}')
            c.circle(x+bw/2,y-51,27,fill=0,stroke=1)
            c.setFont('Body',11);c.drawString(x+9,y-96,'Name:')
            c.line(x+45,y-97,x+bw-9,y-97);c.line(x+9,y-117,x+bw-9,y-117)
        return y-h-13
    if name=='turn_tracker':
        def slot(cx,cy,label=None):
            c.setStrokeColor(color);c.setLineWidth(1.2);c.circle(cx,cy,27,stroke=1,fill=0)
            if label:
                c.setFillColor(GRAY);c.setFont('Body',10);c.drawCentredString(cx,cy-4,label)
        def row(title,left,right,n=1):
            nonlocal y
            y=para(c,title,y,'head');h=93;mid=X+CW/2;gap=12
            for xx,lab in [(X,left),(mid+gap/2,right)]:
                ww=CW/2-gap/2
                c.setFillColor(PALE);c.setStrokeColor(color);c.roundRect(xx,y-h,ww,h,5,fill=1,stroke=1)
                c.setFillColor(INK);c.setFont('Bold',11);c.drawCentredString(xx+ww/2,y-16,lab)
                for k in range(n):slot(xx+ww/2+(k-(n-1)/2)*68,y-57)
            y-=h+12
        row('Actions','AVAILABLE','USED',3)
        # Compact reaction/directive rows keep all turn controls on one mat.
        for title,l,r in [('Reaction','READY','USED'),('Directive','AVAILABLE','ISSUED')]:
            y=para(c,title,y,'head')
            for xx,lab in [(X,l),(X+255,r)]:
                c.setFillColor(PALE);c.setStrokeColor(color);c.roundRect(xx,y-62,235,62,5,fill=1,stroke=1)
                c.setFillColor(INK);c.setFont('Bold',11);c.drawString(xx+12,y-35,lab)
                slot(xx+192,y-31)
            y-=73
        y=para(c,'NEXT ATTACK — shared by all attacks',y,'head')
        for i,lab in enumerate(['FIRST','SECOND','THIRD+']):
            cx=X+78+i*166
            c.setFillColor(INK);c.setFont('Bold',11);c.drawCentredString(cx,y-12,lab)
            slot(cx,y-47)
            if i<2:
                c.setStrokeColor(color);c.line(cx+36,y-47,cx+122,y-47)
                c.line(cx+116,y-43,cx+122,y-47);c.line(cx+116,y-51,cx+122,y-47)
        return y-82
    if name=='effects':
        h=468;leftw=100;gap=14;rx=X+leftw+gap;rw=CW-leftw-gap
        c.setFillColor(PALE);c.setStrokeColor(color);c.roundRect(X,y-h,leftw,h,6,fill=1,stroke=1)
        c.setFillColor(INK);c.setFont('Bold',11);c.drawCentredString(X+leftw/2,y-18,'PARKED')
        for i in range(7):
            c.setStrokeColor(color);c.circle(X+leftw/2,y-55-i*62,27,fill=0,stroke=1)
        def panel(title,top,height):
            c.setFillColor(PALE);c.setStrokeColor(color);c.roundRect(rx,top-height,rw,height,6,fill=1,stroke=1)
            para(c,title,top-10,'head',rx+12,rw-24)
        def circle(cx,cy,label):
            c.setStrokeColor(color);c.circle(cx,cy,27,fill=0,stroke=1)
            c.setFillColor(GRAY);c.setFont('Bold',8.5)
            parts=label.split(' ')
            c.drawCentredString(cx,cy+3,parts[0]);c.drawCentredString(cx,cy-9,' '.join(parts[1:]))
        def target(top,label='Target'):
            c.setFillColor(INK);c.setFont('Body',13);c.drawString(rx+12,top,label+':')
            c.line(rx+(123 if label=='Affected person' else 68),top-2,rx+rw-12,top-2)
        panel('Get ’Em!',y,160);target(y-46)
        circle(rx+53,y-89,'+1 ATTACK');circle(rx+239,y-89,'DAMAGE')
        para(c,'To hit',y-122,'small',rx+30,135)
        para(c,'Later Strikes: see P1',y-122,'small',rx+194,160)
        yy=y-174
        panel('Digital Assessment!',yy,128);target(yy-46)
        circle(rx+53,yy-89,'+1 AC')
        para(c,'Against this target’s attacks',yy-70,'body',rx+100,rw-112)
        yy=y-316
        panel('Bon Mot',yy,152)
        circle(rx+45,yy-79,'BON MOT')
        tx=rx+85
        c.setFillColor(INK);c.setFont('Bold',10)
        c.drawString(tx,yy-43,'Affected person');c.drawString(tx+128,yy-43,'Penalty');c.drawString(tx+206,yy-43,'Ends at')
        for k in range(3):
            by=yy-66-k*24
            c.setStrokeColor(color);c.setLineWidth(.6)
            c.line(tx,by,tx+118,by);c.line(tx+128,by,tx+192,by);c.line(tx+206,by,rx+rw-12,by)
        para(c,'Clear each effect when it ends (P3). Park token when all end.',yy-129,'small',rx+12,rw-24)
        return y-h-12
    if name=='air':
        y=para(c,'Air minutes remaining',y,'head')
        for row,label in enumerate(['Tens','Ones']):
            yy=y-row*45;c.setFont('Bold',14);c.setFillColor(INK);c.drawString(X,yy-21,label)
            for k in range(10):
                x=X+68+k*41;c.setStrokeColor(color);c.roundRect(x,yy-34,33,32,3,fill=0,stroke=1)
                c.setFont('Body',15);c.drawCentredString(x+16.5,yy-24,str(k))
        return y-94
    if name=='tokens':
        groups=[('Turn tokens → C8',['ACTION','ACTION','ACTION','REACTION','DIRECTIVE','NEXT ATTACK']),('Ammunition → C3',['BULLET']*10),('Effects → C9 / assets → Y1',['+1 ATTACK','DAMAGE','+1 AC','BON MOT','SIZED UP 1','SIZED UP 2','SIZED UP 3'])]
        for label,labels in groups:
            y=para(c,label,y,'head')
            for i,lab in enumerate(labels):
                x=X+41+(i%5)*94;yy=y-30-(i//5)*64
                c.setStrokeColor(color);c.setLineWidth(.7);c.circle(x,yy,27,fill=0,stroke=1)
                c.setFont('Bold',8.5);c.setFillColor(INK)
                words=lab.split(' ')
                if len(lab)>9 and len(words)>1:
                    c.drawCentredString(x,yy+3,' '.join(words[:-1]));c.drawCentredString(x,yy-9,words[-1])
                else:c.drawCentredString(x,yy-3,lab)
                if lab in ['ACTION','REACTION']:glyph(c,'1' if lab=='ACTION' else 'R',x-9,yy+18,14)
            y-=((len(labels)+4)//5)*64+6
        return y
    raise ValueError(name)

def diagram_svg(name,color):
    import pymupdf as fitz
    global LINK_IDS
    old_ids=LINK_IDS;LINK_IDS=set()
    buffer=io.BytesIO();dc=canvas.Canvas(buffer,pagesize=(W,H))
    end=diagram(dc,name,H,HexColor(color));dc.showPage();dc.save()
    LINK_IDS=old_ids
    doc=fitz.open(stream=buffer.getvalue(),filetype='pdf')
    doc[0].set_cropbox(fitz.Rect(X,0,RIGHT,H-end))
    svg=doc[0].get_svg_image(text_as_path=True)
    for id in set(re.findall(r'id="([^"]+)"',svg)):
        svg=svg.replace('id="'+id+'"','id="'+name+'-'+id+'"').replace('href="#'+id+'"','href="#'+name+'-'+id+'"').replace('url(#'+id+')','url(#'+name+'-'+id+')')
    return svg.replace('<svg ','<svg class="diagram" role="img" aria-label="'+name+' diagram" ',1)

def render(pages,filename,gm=False):
    global LINK_IDS
    LINK_IDS={p['id'] for p in pages}
    c=canvas.Canvas(str(ROOT/filename),pagesize=(W,H),pageCompression=1)
    c.setTitle("Ponderer — GM setup" if gm else "Ponderer — Table Reference")
    c.setAuthor('Erbium Industries LLC campaign')
    metrics=[]
    for p in pages:
        sec=SECTIONS.get(p['section'],{'name':'GM setup','color':'#45546a','label':'GM'})
        col=HexColor(sec['color']);c.setFillColor(col);c.rect(X,H-52,CW,7,fill=1,stroke=0)
        c.setFillColor(INK);c.setFont('Bold',11);c.drawString(X,H-72,sec['name'].upper())
        c.drawRightString(RIGHT,H-72,p['id'])
        c.bookmarkPage(p['id']);c.addOutlineEntry(p['id']+'  '+p['title'],p['id'],0,False)
        y=para(c,p['title'],H-91,'title')-3
        if p.get('lead'):y=para(c,p['lead'],y)-6
        for b in p['blocks']:
            kind=b['type']
            if kind=='action':y=action(c,b,y,col)
            elif kind=='text':y=para(c,b['text'],y,b.get('style','body'))
            elif kind=='head':y=para(c,b['text'],y-5,'head')
            elif kind=='table':y=table(c,b['rows'],y,b.get('widths'),b.get('header',False),b.get('compact',False))
            elif kind=='diagram':y=diagram(c,b['name'],y,col)
            elif kind=='space':y-=b['height']
        if y<52:metrics.append({'id':p['id'],'bottom':round(y,1),'overflow':True})
        else:metrics.append({'id':p['id'],'bottom':round(y,1),'overflow':False})
        c.setStrokeColor(HexColor('#c6cfd5'));c.line(X,44,RIGHT,44)
        c.setFillColor(GRAY);c.setFont('Body',9)
        c.drawString(X,29,'PONDERER • TABLE REFERENCE' if not gm else 'GM COPY • NOT A PLAYER RULES PAGE')
        c.drawRightString(RIGHT,29,p.get('source','Campaign reference • 9 October 2026'))
        c.showPage()
    c.save();return metrics

def markup(pages,gm=False):
    embedded_fonts=''.join('@font-face{font-family:"Open Sans";font-style:'+style+';font-weight:'+weight+';src:url(data:font/ttf;base64,'+base64.b64encode((ROOT/'fonts'/fn).read_bytes()).decode('ascii')+') format("truetype");}' for fn,style,weight in [('OpenSans-Regular.ttf','normal','400'),('OpenSans-Bold.ttf','normal','700'),('OpenSans-Italic.ttf','italic','400')])
    css='''@page {size:letter;margin:0} *{box-sizing:border-box} body{margin:0;background:#e8ecf0;color:#18222c;font-family:"Open Sans",Arial,sans-serif;font-size:14pt;line-height:1.4} .page{width:8.5in;min-height:11in;margin:16px auto;background:white;padding:.62in .56in .6in 1.14in;page-break-after:always;border-top:7px solid var(--color)} header{display:flex;justify-content:space-between;font-size:11pt;font-weight:700} h1{font-size:25pt;line-height:1.2;margin:14px 0} h2{font-size:17pt;margin:12px 0 6px} p{margin:6px 0 10px} .action{border-top:1px solid var(--color);padding-top:8px;margin-top:12px} .cost,footer{font-size:11pt;color:#50606c} .cost svg{height:18px;width:auto;vertical-align:middle;margin-right:8px} ol{padding-left:28px} li{margin:7px 0} table{border-collapse:collapse;width:100%;margin:10px 0} td{padding:7px;border-bottom:1px solid #d4dce1;vertical-align:top} footer{margin-top:16px;border-top:1px solid #ccd3da;padding-top:8px} .diagram{width:100%;height:auto} .print-note{max-width:8.5in;margin:20px auto;font-size:12pt} @media print{body{background:white}.page{margin:0}.print-note{display:none}}'''
    css+=' .cost{font-size:13pt;font-weight:700;color:#18222c} a{color:inherit;text-decoration:underline;text-underline-offset:2px} button{font:inherit;padding:6px 12px;margin:4px} [contenteditable="true"]{outline:2px dashed #087487} .toolbar{position:sticky;top:0;background:#e8ecf0;padding:8px;z-index:5} @media print{.toolbar{display:none}}'
    title='Ponderer GM setup' if gm else 'Ponderer table reference'
    out=['<!doctype html><html lang="en"><meta charset="utf-8"><title>'+title+' — editable source</title><style>'+embedded_fonts+css+'</style><body><div class="print-note toolbar"><button onclick="editText()" aria-pressed="false" id="edit-toggle">Edit text</button><button onclick="saveCopy()">Save edited HTML</button><p>For checked pagination and exact-size cutouts, print the companion PDF. Edits here change this HTML only. To rebuild the PDFs, edit binder-content.json and run build_binder.py.</p></div>']
    page_ids={p['id'] for p in pages}
    def linked(s):return ID_RE.sub(lambda m:'<a href="#'+m[0]+'">'+m[0]+'</a>' if m[0] in page_ids else m[0],s)
    for p in pages:
        sec=SECTIONS.get(p['section'],{'name':'GM setup','color':'#45546a'})
        out.append(f'<article class="page" id="{p["id"]}" style="--color:{sec["color"]}"><header><span>{sec["name"].upper()}</span><span>{p["id"]}</span></header><h1>{p["title"]}</h1>')
        if p.get('lead'):out.append('<p>'+linked(p['lead'])+'</p>')
        for b in p['blocks']:
            kind=b['type']
            if kind=='text':out.append('<p>'+linked(b['text'])+'</p>')
            elif kind=='head':out.append('<h2>'+b['text']+'</h2>')
            elif kind=='table':out.append('<table>'+''.join('<tr>'+''.join('<td>'+linked(str(t))+'</td>' for t in r)+'</tr>' for r in b['rows'])+'</table>')
            elif kind=='action':
                out.append('<section class="action"><h2>'+b['title']+'</h2><div class="cost">'+(glyph_svg(b['glyph']) if b.get('glyph') else '')+b.get('cost','')+'</div>')
                if b.get('before'):out.append('<p><b>Requirements:</b> '+linked(b['before'])+'</p>')
                if b.get('choices'):out.append('<p><b>Choose one:</b></p>'+''.join('<p>'+linked(s)+'</p>' for s in b['choices']))
                out.append('<ol>'+''.join('<li>'+linked(s)+'</li>' for s in b.get('steps',[]))+'</ol>')
                if b.get('results'):out.append(''.join('<p>'+linked(s)+'</p>' for s in b['results']))
                if b.get('outcomes'):out.append('<table>'+''.join('<tr>'+''.join('<td>'+linked(str(t))+'</td>' for t in r)+'</tr>' for r in b['outcomes'])+'</table>')
                if b.get('note'):out.append('<p>'+linked(b['note'])+'</p>')
                out.append('</section>')
            elif kind=='diagram':
                out.append(diagram_svg(b['name'],sec['color']))
        out.append('<footer>'+p.get('source','Campaign reference • 9 October 2026')+'</footer></article>')
    out.append('''<script>
function setEditing(active){document.querySelectorAll('.page').forEach(p=>{if(active){p.contentEditable='true';}else{p.removeAttribute('contenteditable');}});const button=document.getElementById('edit-toggle');button.textContent=active?'Finish editing':'Edit text';button.setAttribute('aria-pressed',String(active));}
function editText(){setEditing(!document.querySelector('.page').isContentEditable);}
function saveCopy(){setEditing(false);const data='<!doctype html>'+String.fromCharCode(10)+document.documentElement.outerHTML;const url=URL.createObjectURL(new Blob([data],{type:'text/html'}));const a=document.createElement('a');a.href=url;a.download=document.querySelector('#GM1')?'Ponderer-GM-Edited.html':'Ponderer-Edited.html';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
</script></body></html>''');return '\n'.join(out)

if __name__=='__main__':
    reports={}
    reports['binder']=render(PAGES,'Ponderer-Table-Reference.pdf')
    reports['gm']=render(GM_PAGES,'Ponderer-GM-Setup.pdf',True)
    import pymupdf as fitz
    with fitz.open(ROOT/'Ponderer-Table-Reference.pdf') as binder, fitz.open() as mats:
        for id in ['C3','C10','C8','C9','C4','Y1','C6','C11']:
            i=next(i for i,p in enumerate(PAGES) if p['id']==id)
            mats.insert_pdf(binder,from_page=i,to_page=i,links=False)
        mats.set_metadata({'title':'Ponderer — Table Mats and Cutouts'})
        mats.save(ROOT/'Ponderer-Table-Mats.pdf')
    with fitz.open(ROOT/'Ponderer-Table-Reference.pdf') as binder, fitz.open() as additions:
        for id in ['C10','C11']:
            i=next(i for i,p in enumerate(PAGES) if p['id']==id)
            additions.insert_pdf(binder,from_page=i,to_page=i,links=False)
        additions.set_metadata({'title':'Ponderer — FED-12 Battery Tracker and Tokens'})
        additions.save(ROOT/'Ponderer-FED-12-Tracker.pdf')
    (ROOT/'layout-check.json').write_text(json.dumps(reports,indent=2))
    (ROOT/'Ponderer-Editable.html').write_text(markup(PAGES))
    (ROOT/'Ponderer-GM-Setup.html').write_text(markup(GM_PAGES,True))
    assets=ROOT/'action-symbols';assets.mkdir(exist_ok=True)
    for kind,name in [('1','one-action'),('2','two-actions'),('3','three-actions'),('F','free-action'),('R','reaction')]:
        (assets/(name+'.svg')).write_text(glyph_svg(kind))
    print(json.dumps({'pages':len(PAGES),'gm_pages':len(GM_PAGES),'overflow':[x for xs in reports.values() for x in xs if x['overflow']]},indent=2))
