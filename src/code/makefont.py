#!/usr/bin/env python
# -*- coding: utf-8 -*-
# make a font loosely based on the DECwriter 7×7 dot matrix printer
# scruss - 2017-02
# (this is meant for Python 2.x, btw)

import json
import codecs
import fontforge
import math
import psMat

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Please - if you change anything in this code
#  or the related decwriter.json data, you must
#  change the fnt_name value. A unique name is
#  about the only way people and computers can
#  tell fonts apart.
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

fnt_name = 'FIXME_mnicmp'

# dot radius: for round dots, 50 is about right, 30 is light.
# square dots are a bit heavier than round
# star and diamond dots are a bit lighter than round
r = 50

# italic angle: 0.0 for none; 12.08° looks nice
# italic=0.0
italic=0.0

# bold?
bold=False

# dot shape: Square, Diamond or Star.
#  Anything else gets you plain old Round
shape='Round'

# not much to change after here
#  unless you want to break stuff
#################################

# coordinates of centres of dots:
#  eg lower left dot is at (340, 250)
xvals = ( 340,    393,    447,    500,    553,    607,    660 )
yvals = ( 750,    667,    583,    500,    417,    333,    250 )

# matrix translations:
# italic 1: shift LL corner to origin
mat_origin=psMat.translate(-xvals[0], -yvals[6])
# italic 2: skew by italic angle
mat_skew=psMat.skew(math.pi * italic / 180.0) # it likes radians
# italic 3: restore from origin to LL corner
mat_restore=psMat.translate(xvals[0], yvals[6])
# bold: double-strike shift is half point diameter
mat_bold=psMat.translate(r,0)

# a 'magic' value for approximating a circle with Bézier segments
magic = 4.0 / 3.0 * (math.sqrt(2) - 1)
# diamonds are just circles with relaxed control points
if (shape is "Diamond"):
    magic = magic / 2.0
# don't be tempted to make magic too large or you end up
#  with blocky yet frilly fonts that look disturbingly intestinal.

# parameters for stars
star=(3.0+math.sqrt(5))/2.0
inner=r/star
# segment angle (72°), radians
seg=math.pi * (360.0/5.0)/180.0

# read dot structure from JSON file
# resulting structure is a hash/dictionary of dot bitmap arrays
#  against unicode character:
#
#  chars = {
#           ...
#           u'A': [u'...#...',
#                  u'..#.#..',
#                  u'.#...#.',
#                  u'#.....#',
#                  u'#.#.#.#',
#                  u'#.....#',
#                  u'#.....#'],
#           ...
#          }
#
# Everything that's a '#' counts as a dot; everything else is ignored
# If you want to be true to the DECwriter way, you can't have adjacent
#  dots printed, but that's not enforced by this decoder

with open('decwriter.json') as data_file:
    chars = json.load(data_file)

font = fontforge.font(em=1000, encoding='UnicodeFull', ascent=800,
                      descent=200, design_size=12.0, is_quadratic=False,
                      fontname=fnt_name)
# helps with glyph naming (usually)
fontforge.loadNamelist('glyphlist.txt')

# try to make a glyph for every char in json
for uch in chars:
    glyph = font.createChar(ord(uch))
    pts=[]
    print '*** ', ord(uch), ': '
    yline = 0
    # go through glyph bitmap, placing dots where we find #s
    for li in chars[uch]:
        cy = yvals[yline]
        # only encode to prevent Python 2 from grousing about utf-8
        a_li = li.encode('ascii')
        xcol = 0
        for b in list(a_li):
            cx = xvals[xcol]
            if b == '#':
                # we have a pixel at cx, cy, so add it to the list
                pts.append(fontforge.point(cx,cy,False))
            xcol = xcol + 1
        yline = yline + 1

    # get the glyph's layer to draw on
    lyr = glyph.layers[glyph.activeLayer]
    # now transform the points and place contours in layer
    for p in pts:
        # italicize!
        if (italic > 0.0):
            p.transform(mat_origin)
            p.transform(mat_skew)
            p.transform(mat_restore)
        cx=p.x
        cy=p.y
        c = fontforge.contour()
        # draw a printer dot at (cx, cy) using chosen shape
        if (shape is "Square"):
            #
            # Draw a dot by drawing a square of side 2r
            #
            # move to start position
            c.moveTo(cx + r, cy + r)
            # draw the outline
            c.lineTo(cx + r, cy - r)
            c.lineTo(cx - r, cy - r)
            c.lineTo(cx - r, cy + r)
            c.lineTo(cx + r, cy + r)
        elif (shape is "Star"):
            #
            # Draw a 5 pointed star!
            #
            # move to start position (vertical; 90°)
            c.moveTo(cx, cy + r)
            for k in range(5):
                angle=math.pi/2 + (k+1)*seg
                inangle=angle-seg/2.0
                c.lineTo(cx + inner * math.cos(inangle),
                         cy + inner * math.sin(inangle))
                c.lineTo(cx + r * math.cos(angle),
                         cy + r * math.sin(angle))
            # I drew this anticlockwise, so fix it (ahem)
            c.reverseDirection()
        else:
            # Draw a printer dot by approximating a circle
            #  (default; also draws diamonds if magic is low)
            # move to start position
            c.moveTo(cx + r, cy)
            # cubic sector 1: from 0° to 270°, clockwise
            c.cubicTo((cx + r, cy - magic * r),
                      (cx + magic * r, cy - r),
                      (cx, cy - r))
            # cubic sector 2: from 270° to 180°, clockwise
            c.cubicTo((cx - magic * r, cy - r),
                      (cx - r, cy - magic * r),
                      (cx - r, cy))
            # cubic sector 3: from 180° to 90°, clockwise
            c.cubicTo((cx - r, cy + magic * r),
                      (cx - magic * r, cy + r),
                      (cx, cy + r))
            # cubic sector 4: from 90° to 0°, clockwise
            c.cubicTo((cx + magic * r, cy + r),
                      (cx + r, cy + magic * r),
                      (cx + r, cy))
        # ensure path is closed (important!)
        c.closed = True
        lyr += c
        
    # do double-strike effect on glyph if bold
    if (bold is True):
        new_lyr=lyr.dup()
        new_lyr.transform(mat_bold)
        lyr += new_lyr
    # update the glyph layers with our drawing
    glyph.layers[glyph.activeLayer] = lyr
    # some auto cleanups on each glyph to avoid manual work later
    # fix overlapping paths
    glyph.removeOverlap()
    # seems you have to set this too if you deliberately overlap
    glyph.unlinkRmOvrlpSave=True
    # add curve extrema (it's a font convention)
    glyph.addExtrema()
    # round all coordinates to integers
    glyph.round()
    # add PS hints, because we can
    glyph.autoHint()


# poor old space, always left to the end ...
space=font.createChar(ord(' '))
space.left_side_bearing = 90
space.right_side_bearing = 90
space.width = 600

# one last blat through all the glyphs to set monospace parameters
for g in font.glyphs():
    g.left_side_bearing = 90
    g.right_side_bearing = 90
    g.width = 600
    
# these need to restated for some reason,
#  and even then they don't always stick in FontForge
font.encoding = 'UnicodeFull'
font.fontname = fnt_name
font.design_size=12.0
# italic angle is negative for $reasons_i_dont_understand
font.italicangle=-italic

# save it and exit
font.save(fnt_name + '.sfd')
