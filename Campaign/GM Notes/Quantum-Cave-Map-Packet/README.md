# Quantum Cave: 11 x 14 chipboard kit

This revision produces **32 finished tabletop pieces**, assembled from **32 backing cuts and 59 printed cardstock panels**. It uses your 11 x 14-inch chipboard with a 12 x 24-inch Cricut Explore 4 mat. Each grid square is one inch and represents five feet.

Start with **Setup-and-Navigation.pdf**, then use **Backing-and-Panel-Guide.pdf** while building. The latter gives one page per finished piece, with a diagram of its printed panels, the imported dimensions and any required rotation. These guides can stay open digitally while you work.

## Working folders

**Chipboard/** contains one Basic Cut SVG per finished piece. Each is oriented to fit within 10.7 x 13.7 inches, leaving a small allowance within your stock. Check the imported dimensions in the guide and select a 12 x 24 mat. Position your chipboard to cover the design's displayed placement on the mat.

**Cardstock/** contains transparent PNG panels for Print Then Cut. Import as Flat Graphic, preserve the white floor and transparent outside, and set the stated dimensions. Each panel fits within a conservative 6.4 x 8.8-inch rectangle for Letter paper. Some PNGs are rotated for printing; their guide entries say when to turn the cut panel clockwise for assembly. Print through Design Space to generate its registration marks. Small panels can share a printing mat/page where Design Space permits.

For a small piece with one cardstock panel, you can duplicate the imported PNG, change the duplicate to Basic Cut, and use it for the backing. Preserve its dimensions and rotate to fit the chipboard if needed. The matching SVG retains the exact vector contour. For large pieces, the whole backing SVG and multiple cardstock PNGs serve different stages of the build.

**Connector-Test/** contains eight sample SVGs and eight matching PNGs. The tab is 1.900 x 1.500 inches; the socket is 1.500 x 1.500 inches. Four pairs compare socket clearances of 0, 0.005, 0.010 and 0.015 inch. Test the complete glued construction before cutting the full set. The main kit uses zero additional clearance; a looser preferred sample indicates a needed contour adjustment. Material thickness, density, blade and adhesive affect the physical result.

## Assembly

Cut the backing, then print and cut its named cardstock panels. Arrange panels using their R/C identifiers: row 1 is the top and column 1 is the left of the assembly diagram. Match the artwork and grid along seams, glue panels flush together and let the piece dry flat. Label the backing's underside with its room or passage name. The printed panels stay permanently attached during play.

The guide diagrams show each piece in map orientation. Some backing SVGs are rotated clockwise 90 degrees to fit the chipboard; turn the finished backing to match its diagram before gluing. Panel diagrams label the actual cropped artwork shapes, so unequal panel widths are intentional.

## Finished-piece inventory

| Component | Pieces |
| --- | ---: |
| Entrance Hall | 4 |
| Entrance-to-junction passage | 1 |
| Nest Junction | 1 |
| Feeding Hollow | 2 |
| Lift Cavern | 1 |
| West branch | 2 |
| East branch | 2 |
| Low tunnel | 2 |
| Upper Gallery | 3 |
| Anomaly Grotto | 2 |
| Q1 entrance-state strips | 3 |
| Q2 slab and empty-dock inserts | 3 |
| Q3 occupied and empty berth inserts | 2 |
| Ship hull and ramp | 2 |
| Anomaly and maintenance case | 2 |
| **Total** | **32** |

The ship hull is a single **10 x 11.8-inch backing**, with four permanently attached printed panels. Its separate ramp meets the port hull edge. This retains the approximately 50 x 60-foot exterior scale. A future interior map can establish the party's living and working spaces.

All room dimensions, routes and quantum mechanics are preserved. The complete mouth strip swaps between Bright-Side, Dark-Side and Underground. Q2 moves between two matching docks. Q3 exchanges occupied and empty inserts between Gallery and Deep. Ship, case and anomaly remain separate objects. The three families have matching cut contours; this revision's broader connectors are intended to be used together as a complete set.

## PDFs and maps

- **Quantum-Cave-GM-Packet.pdf:** overview, state comparisons on pages 2–4, assembly plan on page 5, setup/navigation, inventory, twelve complete states beginning on page 10, and two event examples.
- **Backing-and-Panel-Guide.pdf:** 32 construction diagrams with backing and PNG dimensions.
- **Quantum-Cave-Player-Tiles-Letter.pdf:** 59 ordinary hand-trim printing pages with outlines and calibration bars. Use Actual Size / 100%. For Cricut Print Then Cut, use the PNGs through Design Space.
- **Quantum-Cave-Players.pdf:** complete unkeyed states and event examples. Reveal individual physical pieces during exploration; whole-map pages show the full layout.
- **Connector-Test-Sheet.pdf:** ordinary printing companion to the test files.
- **maps/** and **previews/**: editable vector maps, individual PDFs and PNG previews.
- **manifest.json:** backing sizes, panel sizes and their relationships, including printing-page numbers and orientation.

The 59 PNG panels are construction components. Design Space may pack multiple small panels onto a printed page. The hand-trim PDF puts each panel on its own page for straightforward dimensions and selection.

## Checks and source

Checks verify coverage and overlap of the fixed sections, full cardstock coverage of every backing, stock bounds, print-panel bounds, matching Q1/Q2/Q3 outlines, lower-cave connectivity and the two important blocked sightlines. The ship, assembly plan, setup guide and print-sheet samples were visually inspected. Physical cutting, fit and Design Space import remain to be tested on your equipment.

Rebuild with `python source/build_kit.py` using Shapely, CairoSVG, Pillow, ReportLab and pypdf. The generator writes its results to `source/validation.json`.

Official Cricut references:

- [Explore 4 mats and tools](https://help.cricut.com/hc/en-us/articles/28450364213143-Cricut-Explore-4-Quick-Start-Guide)
- [Print Then Cut size limits](https://help.cricut.com/hc/en-us/articles/360009429814-How-large-can-I-Print-Then-Cut)
- [Uploading images](https://help.cricut.com/hc/en-us/articles/360009556313-How-to-upload-images-into-Design-Space)
- [Print Then Cut workflow](https://help.cricut.com/hc/en-us/articles/360009387274-How-to-Print-Then-Cut-in-Design-Space)
