# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 15:52:40 2021

@author: Jonny
"""

from enum import Enum

class SosiObjId(Enum):
    UKJENT = 0
    PUNKT = 1
    KURVE = 2
    FLATE = 3

# pntlst: sequential list of points
# return list of point indices defining edges
def points_to_edglist(pntlst):
    edglst = []
    for i in range(1, len(pntlst)):
        edglst.append((i - 1, i))
    return edglst


def intary_to_trilist(ints, ilen):
    trilist = []
    for i in range(0, ilen):
        trilist.append((ints[3 * i], ints[3 * i + 1], ints[3 * i + 2]))
    return trilist