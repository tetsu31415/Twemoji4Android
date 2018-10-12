#!/usr/bin/python
#
# Copyright 2013 Google, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# November 21, 2014
# Modified by tetsu31415

import glob, sys
from fontTools import ttx
from fontTools.ttLib.tables import otTables
from png import PNG

from nototools import add_emoji_gsub


def glyph_name(codes):
	return "_".join (["%04X" % int (code,16) for code in codes])


def add_ligature (font, codes):
		if 'GSUB' not in font:
			ligature_subst = otTables.LigatureSubst()
			ligature_subst.ligatures = {}

			lookup = otTables.Lookup()
			lookup.LookupType = 4
			lookup.LookupFlag = 0
			lookup.SubTableCount = 1
			lookup.SubTable = [ligature_subst]

			font['GSUB'] = add_emoji_gsub.create_simple_gsub([lookup])
		else:
			lookup = font['GSUB'].table.LookupList.Lookup[0]
			assert lookup.LookupType == 4
			assert lookup.LookupFlag == 0

		ligatures = lookup.SubTable[0].ligatures

		lig = otTables.Ligature()
		lig.CompCount = len(codes)
		lig.Component = [glyph_name([code]) for code in codes[1:]]
		lig.LigGlyph = glyph_name(codes)

		first = "%04X" % int(codes[0],16)
		try:
			ligatures[first].append(lig)
		except KeyError:
			ligatures[first] = [lig]



if len (sys.argv) < 4:
        print >>sys.stderr, """
Usage:

add_glyphs.py font.ttx out-font.ttx strike-prefix...

This will search for files that have strike-prefix followed by one or more
hex numbers (separated by underscore if more than one), and end in ".png".
For example, if strike-prefix is "icons/u", then files with names like
"icons/u1F4A9.png" or "icons/u1F1EF_1F1F5.png" will be loaded.  The script
then adds cmap, htmx, and potentially GSUB entries for the Unicode
characters found.  The advance width will be chosen based on image aspect
ratio.  If Unicode values outside the BMP are desired, the existing cmap
table should be of the appropriate (format 12) type.  Only the first cmap
table and the first GSUB lookup (if existing) are modified.
"""
        sys.exit (1)

in_file = sys.argv[1]
out_file = sys.argv[2]
img_prefix = sys.argv[3]
del sys.argv

font = ttx.TTFont()
font.importXML (in_file)

img_files = {}
glb = "%s*.png" % img_prefix
print "Looking for images matching '%s'." % glb
for img_file in glob.glob (glb):
        u = img_file[len (img_prefix):-4].upper()
        img_files[u] = img_file
if not img_files:
        raise Exception ("No image files found in '%s'." % glb)

ascent = font['hhea'].ascent
descent = -font['hhea'].descent

g = font['GlyphOrder'].glyphOrder
c = font['cmap'].tables[0].cmap
h = font['hmtx'].metrics

# Sort the characters by length, then codepoint, to keep the order stable
# and avoid adding empty glyphs for multi-character glyphs if any piece is
# also included.
img_pairs = img_files.items ()
img_pairs.sort (key=lambda pair: (len (pair[0]), pair[0]), reverse=True)

for code in [0x23,0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38,0x39,0x20e3]:
	g.append("%04X" % code)

for (u, filename) in img_pairs:
	codes = u.split("-")
	n = glyph_name (codes)
	print "Adding glyph for %s" % n
	g.append (n)
	for code in codes:
		code = int(code,16)
		if code not in c:
			name = glyph_name (["%04X" % code])
			c[code] = name
			if len (codes) > 1:
				h[name] = [0, 0]
	(img_width, img_height) = PNG (filename).get_size ()
	advance = int (round ((float (ascent+descent) * img_width / img_height)))
	h[n] = [advance, 0]
	if len (codes) > 1:
		add_ligature (font, codes)

font.saveXML (out_file)
