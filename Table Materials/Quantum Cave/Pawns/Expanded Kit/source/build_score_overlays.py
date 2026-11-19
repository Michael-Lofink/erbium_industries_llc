"""Build score-only SVGs for the existing expanded pawn sheets.

Coordinates match build_pawns.py: 0.35-inch feet, 0.08-inch spine,
0.9-inch bodies, and 1.1-inch column spacing. Artwork includes base labels
below the bodies; overlay bounds cover the fold lines only.
"""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SHEETS = (
    ('Electrovore-Pawns-1-4', 4, 165),
    ('Electrovore-Pawns-5-8', 4, 165),
    ('Quantum-Stone-Pawns', 3, 120),
)


def build():
    dest = ROOT / 'Score-Overlays'
    dest.mkdir(exist_ok=True)
    for name, count, face_height in SHEETS:
        width = (count - 1) * 110 + 90
        height = 2 * face_height + 8
        paths = []
        for col in range(count):
            x = col * 110
            for y in (0, face_height, face_height + 8, height):
                paths.append(f'M {x} {y} H {x + 90}')
        svg = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width/100:g}in" '
            f'height="{height/100:g}in" viewBox="0 0 {width} {height}">\n'
            '  <desc>Set operation to Score. Align left edges with matching PNG; '
            'place overlay top 0.35 inches below PNG top. Attach to PNG.</desc>\n'
            f'  <path id="Fold-lines" d="{" ".join(paths)}" '
            'fill="none" stroke="#000000" stroke-width="0.1"/>\n'
            '</svg>\n'
        )
        ET.fromstring(svg)
        (dest / f'{name}-Score.svg').write_text(svg)


if __name__ == '__main__':
    build()
