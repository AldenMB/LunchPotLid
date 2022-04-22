import cadquery as cq
import numpy as np
from types import SimpleNamespace as ns

INCH = 25.4

measured = ns(
    inside_diameter = 4 * INCH,
    outside_diameter = 4.5 * INCH,
    height = 0.9 * INCH,
    indent = ns(
        diameter = (3+2/3) * INCH,
        depth = 0.3 * INCH
    ),
    fillet = 0.1 * INCH,
    lip_thickness = 5.5,
    gasket = ns(
        width = 4,
        depth = 0.1 * INCH
    ),
    nub = ns(
        radius = 1/3 * INCH,
        inset = 0.25 * INCH
    ),
    channel = ns(
        depth = 0.1 * INCH,
        fillet = 1
    ),
)


lid = cq.Workplane('XY').cylinder(measured.height, measured.inside_diameter/2)
lid = (lid.faces('>Z').workplane()
    .circle(measured.outside_diameter/2)
    .extrude(-measured.lip_thickness)
)
lid = (lid.faces('>Z').workplane()
    .moveTo(measured.outside_diameter/2+measured.nub.inset-measured.nub.radius, 0)
    .circle(measured.nub.radius)
    .extrude(-measured.lip_thickness)
)
lid = lid.faces('>Z').workplane().hole(measured.indent.diameter, measured.indent.depth)
lid = lid.fillet(measured.fillet)

channel = (cq.Workplane('YZ')
    .moveTo(0.5*INCH, -measured.height/2)
    .radiusArc([0.5*INCH, -measured.height/2+7/2], -7/4)
    .line(-1.5*INCH, 0.25*INCH)
    .radiusArc([-INCH, -measured.height/2+0.25*INCH+7], 7/4)
    .line(1.5*INCH, -0.1*INCH)
    .tangentArcPoint([INCH, -measured.height/2])
    .close()
)
channel = channel.extrude(-measured.inside_diameter)
channel = channel.cut(
    cq.Workplane('XY')
    .cylinder(2*measured.height, measured.inside_diameter/2 - measured.channel.depth)
)
c = channel
for angle in [120, -120]:
    channel = channel.union(c.rotate([0,0,0], [0,0,1], angle))


#show_object(channel, name='channel', options={'color':'red', 'alpha':0.1})

lid = lid.cut(channel)

# done last to ensure it doesn't get filleted
lid = (lid.faces('<Z').workplane()
    .circle(measured.inside_diameter/2)
    .circle(measured.inside_diameter/2+measured.gasket.width)
    .cutBlind(-measured.height+measured.lip_thickness-measured.gasket.depth)
)

show_object(lid, name='lid', options={'color':'orange', 'alpha':0.1})

cq.exporters.export(lid, 'lunchpot.stl')
