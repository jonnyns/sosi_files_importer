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

import numpy as np
import math
import logging
from . import sosi_log_helper as sologhlp
from . import sosi_settings as soset

# -----------------------------------------------------------------------------

def coords2D(v):
    return v[0], v[1]

# -----------------------------------------------------------------------------

def coords3D(v):
    return v[0], v[1], v[2]

# -----------------------------------------------------------------------------

def printArray(a):
    for row in range(len(a)):
        for col in range (len(a[row])):
            print("{:8.3f}".format(a[row][col]), end = " ")
        print()
        
# -----------------------------------------------------------------------------
        
def rads_2_degrees(angls):
    degs = []
    for a in angls:
        degs.append(math.degrees(a))
    return degs

# -----------------------------------------------------------------------------

def arc_circle_center_2D(p1, p2, p3):
    """
    For the 2D case: p1, p2, p3 are three points on the arc of a circle.
    Return the x and y coordinates for the center of the circle.
    """
    #print(p1, p2, p3)
    x1, y1 = coords2D(p1)
    x2, y2 = coords2D(p2)
    x3, y3 = coords2D(p3)
    
    n = (-x2 * x2 * y1 + x3 * x3 * y1 + x1 * x1 * y2 - x3 * x3 * y2 \
        + y1 * y1 * y2 - y1 * y2 * y2 - x1 * x1 * y3 + x2 * x2 * y3 \
        - y1 * y1 * y3 + y2 * y2 * y3 + y1 * y3 * y3 - y2 * y3 * y3)
    d = 2 * (x2 * y1 - x3 * y1 - x1 * y2 + x3 * y2 + x1 * y3 - x2 * y3)
    if (d == 0.0):
        return None
    x = -(n/d)
    n = -x1 * x1 * x2 + x1 * x2 * x2 + x1 * x1 * x3 - x2 * x2 * x3 \
        - x1 * x3 * x3 + x2 * x3 * x3 - x2 * y1 * y1 + x3 * y1 * y1 \
        + x1 * y2 * y2 - x3 * y2 * y2 - x1 * y3 * y3 + x2 * y3 * y3
    y = -(n/d)
    return (x, y)

# -----------------------------------------------------------------------------

def rotate_pts_3D(mtx, pts):
    """
    Rotate the 3D points in the pts list according to the 3x3 
    rotation matrix mtx.
    Return the list of rotated points.
    """
    tpts = []
    for pt in pts:
        p = mtx @ np.asarray(pt)
        tpts.append(p)
    return tpts

# -----------------------------------------------------------------------------

def transform_pts_3D(mtx, pts):
    """
    Transform the 3D points in the pts list according to the 4x4
    transformation matrix mtx.
    Return the list of transformed points.
    """
    tpts = []
    for pt in pts:
        if len(pt) < 4:
            pt = (*pt, 1.0)
        p = mtx @ np.asarray(pt)
        pp = (p[0], p[1], p[2])
        tpts.append(pp)
    return tpts

# -----------------------------------------------------------------------------

def get_rotation_matrix(axis, theta):
    """
    Find the rotation matrix associated with counterclockwise rotation
    about the given axis by theta radians.
    Credit: http://stackoverflow.com/users/190597/unutbu

    Args:
        axis (list): rotation axis of the form [x, y, z]
        theta (float): rotational angle in radians

    Returns:
        array. Rotation matrix.
    """

    axis = np.asarray(axis)
    theta = np.asarray(theta)
    axis = axis/math.sqrt(np.dot(axis, axis))
    a = math.cos(theta/2.0)
    b, c, d = -axis*math.sin(theta/2.0)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])

# -----------------------------------------------------------------------------

def get_translation_matrix(t):
    tm = [[1, 0, 0, t[0]], [0, 1, 0, t[1]], [0, 0, 1, t[2]], [0, 0, 0, 1]]
    return np.asarray(tm)

# -----------------------------------------------------------------------------

def angles_interpolate(angls, angls_diff, num_splits):
    angls_between = []
    for i in range(len(angls)-1):
        angl_step = angls_diff[i]/num_splits
        a = angls[i]
        angls_between.append(a)
        for j in range(1, num_splits):
            a += angl_step
            angls_between.append(a)
    angls_between.append(angls[-1])    
    return angls_between

# -----------------------------------------------------------------------------

# Angle between two vectors [radians]
def angle_vector_3D(v1, v2, acute):
    """
    # v1 is first vector
    # v2 is second vector
    """
    angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    if (acute == True):
        return angle
    else:
        return 2 * np.pi - angle

# -----------------------------------------------------------------------------

def angle_vector_2D(v1, v2):
    """
    Return angle between two 2D vectors (i.e. use only x and y coordinate values)
    Angle (from v1 to v2, positive angle of rotation) is in the range -pi < x < pi.
    """
    dot = v1[0] * v2[0] + v1[1] * v2[1] # dot product
    det = v1[0] * v2[1] - v1[1] * v2[0] # determinant
    angl = math.atan2(det, dot)
    return angl
        
# -----------------------------------------------------------------------------
        
def angles_circle_abs_2D(circle_pts, num=0):
    """
    Assuming circle_pts contains 2D coordinates for a circle with center origin (0., 0.)
    compute angle for all coordinates in range 0 <= angl < 2 * pi
    """
    if (num == 0):
        num = len(circle_pts)
    angls = []
    for i in range(0, num):
        pt = circle_pts[i]
        radius = math.sqrt(pt[0]**2 + pt[1]**2)
        if (radius == 0.0):
            angl = None
        else:
            angl = math.asin(pt[1]/radius)
            #print(pt[0],  pt[1], radius, angl, math.degrees(angl))
            if (pt[0] < 0.):
                    angl = math.pi - angl
            else:
                if ((pt[1] < 0.)):
                    angl = 2 * math.pi + angl
            #print(math.degrees(angl))
        angls.append(angl)
    return angls

# -----------------------------------------------------------------------------

def angles_circle_diff_2D(circle_pts):
    """
    Assuming circle_pts contains 2D coordinates for pts on a circle as well as the circle center 
    The circle center is the very last of the coordinates
    Compute angles between successive arc pts
    """
    a = []
    for i in range(1, len(circle_pts) - 1):
        vb = circle_pts[i] - circle_pts[-1]
        va = circle_pts[i-1] - circle_pts[-1]
        a.append(angle_vector_2D(va, vb))
    return a

# -----------------------------------------------------------------------------

def angle_num_splits(angl):
    num_splits = (angl * soset.SOSI_ARC_SEGMENTS) / (2 * math.pi)
    print(math.degrees(angl), num_splits)
    return num_splits

# -----------------------------------------------------------------------------

def is_arc_pos_or_neg(angls):
    #print(math.degrees(angls[0]), math.degrees(angls[1]), math.degrees(angls[2]))
    for i in range(len(angls)):  
        #print(i)
        idx_nxt = i + 1
        if (idx_nxt >= len(angls)):
            idx_nxt = 0
        if (angls[i] > angls[i-1]) and (angls[i] < angls[idx_nxt]):
            return 1
        elif (angls[i] < angls[i-1]) and (angls[i] > angls[idx_nxt]):
            return -1
    
# -----------------------------------------------------------------------------

def arc_pts_interpolate_2D(cirpts_hor, num_splits):
    """
    cirpts_hor contains 2D coordinates for pts on a circle (i.e. arcs) as well as the circle center.
    The circle center is the very last of the coordinates.
    num_splits is the number of segments required for each arc.
    Return the coordinates for every point on the circle (including those in cirpts_hor)
    """
    cirpts_hor = np.asarray(cirpts_hor) # To support vector operations
    radius = math.sqrt((cirpts_hor[0][0] - cirpts_hor[-1][0])**2 + (cirpts_hor[0][1] - cirpts_hor[-1][1])**2)
    angls = angles_circle_abs_2D(cirpts_hor, len(cirpts_hor)-1)
    #print(math.degrees(angls[0]), math.degrees(angls[1]), math.degrees(angls[2]))
    angls_diff = angles_circle_diff_2D(cirpts_hor)
    #print(rads_2_degrees(angls_diff))
    
    if num_splits == 0: # calculate number of splits
        angl_less = angls_diff[0]
        if abs(angls_diff[0]) > abs(angls_diff[1]):
            angl_less = angls_diff[1] # lesser value
        num_splits = math.ceil(abs(angle_num_splits(angl_less)))
        print(num_splits)
    angls_interpolated = angles_interpolate(angls, angls_diff, num_splits)
    #print(rads_2_degrees(angls_interpolated))

    coords = []    
    for a in angls_interpolated:
        coord = (math.cos(a) * radius, math.sin(a) * radius, cirpts_hor[0][2])
        coords.append(coord)
        #print(math.degrees(a), coord)
    return coords

# -----------------------------------------------------------------------------

def arc_pts_segments_3D(arc_pts, num_splits):
    """
    arc_pts contains 3 3D-coordinates assumed to lie on a circle (i.e. two arcs).
    Each arc will be split into num_splits segments.
    Return the 3D coordinates for all segment points (including the original coordinates)
    as curve points.                                           .
    """
    arr = np.asarray(arc_pts) # To support vector operations
    v1 = arr[0] - arr[1]
    v2 = arr[2] - arr[1]
    logging.debug(' Arc vectors:\n %s %s', v1, v2)
    vn = np.cross(v1, v2) # Normal to vector plane
    logging.debug(' Normal vector:\n %s',  sologhlp.formatArray(vn))
    vz = np.array([0.0, 0.0, 1.0])
    # Rotation vector
    vr = np.cross(vn, vz) # Between normal and z vector
    logging.debug(' Rotation vector:\n%s', sologhlp.formatArray(vr))
    # rotation angle
    a = angle_vector_3D(vn, vz, True)
    logging.debug(' Rotation angle:\n%s', math.degrees(a))
    
    if (a != 0.0) and (a != math.pi):
        rot_mtx = get_rotation_matrix(vr, a)
        logging.debug(' Rotation matrix:\n%s', rot_mtx)
        logging.debug(' Arc pts pre:\n%s', sologhlp.formatArray(arc_pts))
        arc_pts_horz = rotate_pts_3D(rot_mtx, arc_pts)
        logging.debug(' Arc pts post:\n%s', sologhlp.formatArray(arc_pts_horz))
    else:
        arc_pts_horz = arc_pts
        #ctr2D = get_arc_center_2D(arc_pts_horz[0], arc_pts_horz[1], arc_pts_horz[2])
        
    ctr2D = arc_circle_center_2D(arc_pts_horz[0], arc_pts_horz[1], arc_pts_horz[2])
    ctr3D = [ctr2D[0], ctr2D[1], arc_pts_horz[2][2]] # Use z-value for one of the points
    logging.debug(' Circle center:\n%s', ctr3D)
    # Append the center point to the list
    cir_pts_hor = [arc_pts_horz[0], arc_pts_horz[1], arc_pts_horz[2], np.array(ctr3D)]
    logging.debug(' Circle points:\n%s', sologhlp.formatArray(cir_pts_hor))
    
    # Translation to origo
    trans_mtx1 = get_translation_matrix([-ctr3D[0], -ctr3D[1], 0]) # Translate circle center to origo
    cir_pts_hor_origo = transform_pts_3D(trans_mtx1, cir_pts_hor)
    logging.debug(' Circle points around origo:\n%s', sologhlp.formatArray(cir_pts_hor_origo))
    
    # Interpolate into arc segment points
    #num_splits = 8
    arc_pts_horz_origo = arc_pts_interpolate_2D(cir_pts_hor_origo, num_splits)
    logging.debug(' Circle points around origo:\n%s', sologhlp.formatArray(arc_pts_horz_origo))
    
    # Translation back
    trans_mtx2 = get_translation_matrix([ctr3D[0], ctr3D[1], 0]) # Circle center back
    arc_pts_horz = transform_pts_3D(trans_mtx2, arc_pts_horz_origo)
    #printArray(arc_pts_horz)
    # Rotate back to original position
    if (a != 0.0) and (a != math.pi):
        arc_pts_nonhorz = []
        for ap in arc_pts_horz:
            arc_pts_nonhorz.append(np.transpose(rot_mtx) @ ap)
    else:
        arc_pts_nonhorz = arc_pts_horz
    return arc_pts_nonhorz