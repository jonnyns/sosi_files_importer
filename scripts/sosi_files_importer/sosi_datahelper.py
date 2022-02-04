# -*- coding: utf-8 -*-
"""
Copyright © 2022 Jonny Normann Skålvik

Permission is hereby granted, free of charge, to any person obtaining a copy 
of this software and associated documentation files (the “Software”), to deal 
in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in 
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.

This file is part of SosiImporter, an addon to import SOSI files containing
3D model data into Blender.
"""

from enum import Enum

# -----------------------------------------------------------------------------

class SosiObjId(Enum):
    UKJENT = 0
    PUNKT = 1
    KURVE = 2
    FLATE = 3
    BUEP = 4

# -----------------------------------------------------------------------------

# pntlst: sequential list of points
# return list of point indices defining edges
def points_to_edglist(pntlst):
    edglst = []
    for i in range(1, len(pntlst)):
        edglst.append((i - 1, i))
    return edglst

# -----------------------------------------------------------------------------

def intary_to_trilist(ints, ilen):
    trilist = []
    for i in range(0, ilen):
        trilist.append((ints[3 * i], ints[3 * i + 1], ints[3 * i + 2]))
    return trilist