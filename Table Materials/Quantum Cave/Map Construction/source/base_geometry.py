from pathlib import Path
import math, json, io, zipfile, textwrap, re
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from shapely.geometry import Polygon, box, LineString, Point
from shapely.ops import unary_union
from shapely.affinity import translate
import cairosvg
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader, PdfWriter, Transformation

ROOT=Path(__file__).resolve().parents[1]
INK='#176c89'; GRID='#a8c7d1'; PAPER='#ffffff'
def poly(p): return Polygon(p)
def corridor(points,w=2): return LineString(points).buffer(w/2,cap_style=2,join_style=2)
def path(g):
    def ring(r): return 'M '+' L '.join(f'{x:.3f},{y:.3f}' for x,y in r.coords)+' Z'
    if g.is_empty:return ''
    if g.geom_type=='Polygon':return ring(g.exterior)+' '+' '.join(ring(r) for r in g.interiors)
    return ' '.join(path(a) for a in g.geoms)
def text(x,y,s,size=.65,color=INK,anchor='start',weight='normal'):
    return f'<text x="{x}" y="{y}" font-family="DejaVu Sans, sans-serif" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{escape(s)}</text>'
def line(x1,y1,x2,y2,color=INK,width=.09,dash=''):
    return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="{width}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def rect(x,y,w,h,fill='white',stroke=INK,sw=.09):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def circle(x,y,r,fill='white',stroke=INK,sw=.09):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def badge(x,y,s):return circle(x,y,.64)+text(x,y+.24,s,.72,anchor='middle',weight='bold')
def vent(x,y,spent=False):
    s=f'<path d="M{x-.65},{y-.3} Q{x},{y-.9} {x+.6},{y-.3} M{x-.5},{y+.15} L{x-.1},{y-.2} L{x+.15},{y+.3} L{x+.65},{y-.1}" stroke="{INK}" stroke-width=".1" fill="none"/>'
    if spent:s+=line(x-.6,y+.55,x+.6,y+.55,dash='.15 .12')
    return s
def stairs(x,y,w,h):
    s=''
    for i in range(int(h*3)+1):s+=line(x,y+i/3,x+w,y+i/3,width=.07)
    s+=line(x+w/2,y+.3,x+w/2,y+h-.4,width=.1)
    s+=f'<path d="M{x+w/2-.3},{y+h-.8} L{x+w/2},{y+h-.35} L{x+w/2+.3},{y+h-.8}" fill="none" stroke="{INK}" stroke-width=".1"/>'
    return s
def slab(x,y):
    s=rect(x,y,3,3)
    pts=[]
    for i in range(90):
        a=i*.14;r=.05+i*.009;pts.append((x+1.5+math.cos(a)*r,y+1.5+math.sin(a)*r))
    return s+f'<path d="{pathline(pts)}" fill="none" stroke="{INK}" stroke-width=".09"/>'
def pathline(pts):return 'M '+' L '.join(f'{x:.3f},{y:.3f}' for x,y in pts)
def chamber(x,y):
    s=rect(x,y,3,3)
    s+=line(x+3,y+1,x+3,y+2,'white',.16)
    s+=f'<path d="M{x+.25},{y+.25} H{x+2.75} V{y+.85} M{x+2.75},{y+2.15} V{y+2.75} H{x+.25} V{y+.25}" fill="none" stroke="{INK}" stroke-width=".04"/>'
    s+=f'<path d="M{x+2.7},{y+1} l-.12,.17 .24,.17 -.24,.17 .24,.17 -.24,.17 .12,.15" fill="none" stroke="{INK}" stroke-width=".08"/>'
    return s
def ship(x,y):
    hull=[(x+5,y),(x+8,y+3),(x+8,y+5),(x+10,y+8),(x+10,y+11),(x+7,y+10),(x+7,y+12),(x+3,y+12),(x+3,y+10),(x,y+11),(x,y+8),(x+2,y+5),(x+2,y+3)]
    s=f'<path d="{path(poly(hull))}" fill="white" stroke="{INK}" stroke-width=".14"/>'
    s+=f'<path d="M{x+3.1},{y+3.5} L{x+5},{y+1.5} L{x+6.9},{y+3.5} Z" fill="none" stroke="{INK}" stroke-width=".1"/>'
    s+=rect(x+3,y+5,4,4)+rect(x+3.3,y+10,1.2,1.5)+rect(x+5.5,y+10,1.2,1.5)
    s+=rect(x-2,y+8,4,1.5)+stairs(x-2,y+8,4,1.5)
    return s
def anomaly(x,y):
    s=''
    for dx,dy,r in [(0,0,.65),(-1,-.5,.38),(.9,-.8,.32),(.9,.8,.42),(-.8,.9,.28)]:
        s+=f'<path d="M{x+dx},{y+dy-r} L{x+dx+r},{y+dy} L{x+dx},{y+dy+r} L{x+dx-r},{y+dy} Z" fill="white" stroke="{INK}" stroke-width=".1"/>'
    return s

# Floor coordinates are measured in five-foot squares; north is up in every inset.
entrance=poly([(18,3),(20,2),(40,2),(42,4),(42,16),(40,18),(20,18),(18,16)])
mouth=box(24,0,36,4)
entryroute=corridor([(30,18),(30,21),(33,21),(33,27)])
junction=poly([(28,27),(34,27),(35,28),(35,34),(34,35),(28,35),(27,34),(27,28)])
hollow=poly([(5,22),(15,22),(17,24),(17,30),(15,32),(5,32),(3,30),(3,24)])
hollow=translate(hollow,yoff=14)
west=corridor([(27,32),(10,32),(10,36)])
east=corridor([(35,32),(51,32),(51,38)])
low=corridor([(17,39.5),(39.5,39.5),(39.5,41.5),(43,41.5)],1)
lift=poly([(44,26),(52,26),(53,27),(53,33),(52,34),(44,34),(43,33),(43,27)])
lift=translate(lift,yoff=12)
lower=unary_union([entrance,mouth,entryroute,junction,hollow,west,east,low,lift])
pillars=[box(30,30,32,32),poly([(13,40),(14,39),(15,40),(15,42),(14,43),(13,42)]),box(9,38,10,39)]
lower=lower.difference(unary_union(pillars))
gallery=unary_union([box(3,3,21,7),box(21,3,33,5),box(31,5,33,10),box(27,7,31,11),box(3,7,5,12)])
# Lift shaft is traversable only with slab present; shown as a separate feature.
upper=unary_union([gallery,box(17,7,20,10)])
deep=unary_union([box(2,6,6,10),poly([(6,5),(8,3),(16,3),(18,5),(18,11),(16,13),(8,13),(6,11)])])
GEOM={'lower':lower,'upper':upper,'deep':deep}

