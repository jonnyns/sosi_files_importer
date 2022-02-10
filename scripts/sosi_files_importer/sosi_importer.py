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

import bpy
import os
import sys
import numpy as np
import ctypes
from ctypes import wintypes
import logging
from . import sosi_settings as soset
from . import sosi_log_helper as sologhlp
from . import sosi_geom_helper as sogeohlp

# -----------------------------------------------------------------------------

RES_SOSI_GENERAL_ERROR	    = 0x0001
RES_SOSI_DIMENSION_MISMATCH = 0x0010
RES_SOSI_LOOP_UNCLOSED      = 0x0100

#C = bpy.context
#D = bpy.data

# Parent object for all SOSI elements
top_parent = None

# Determine if the code is running from within Blender
in_blender = True

try:
    import bpy
    in_blender = os.path.basename(bpy.app.binary_path or '').lower().startswith('blender')
except ModuleNotFoundError:
    in_blender = False   
#print('INFO: Blender environment:', in_blender)

if (in_blender == True):
    from . import sosi_datahelper as sodhlp    
    from . import blender_helper as bldhlp
else:
    import sosi_datahelper as sodhlp    
    import blender_helper as bldhlp
    
#import sosi_datahelper as sodhlp
#from . import sosi_datahelper as sodhlp
#from sosi_importer import sosi_datahelper as sodhlp # from directory sosi_importer

#import blender_helper as bldhlp
#from sosi_importer import blender_helper as bldhlp # from directory sosi_importer

c_int = ctypes.c_int
c_int32 = ctypes.c_int32
c_double = ctypes.c_double
c_void_p = ctypes.c_void_p
c_char_p = ctypes.c_char_p

# -----------------------------------------------------------------------------

def coord_array_to_list(ndims, ncoords, ary):
    coordList = []
    if (ndims == 2):
        for i in range(ncoords):
            coordList.append((ary[i * 2], ary[i * 2 + 1], 0.0))
    else: # ndims == 3
        for i in range(ncoords):
            coordList.append((ary[i * 3], ary[i * 3 + 1], ary[i * 3 + 2]))
    return coordList

# -----------------------------------------------------------------------------

def get_full_path(rel_path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    head_path, tail_path = os.path.split(dir_path)
    return os.path.join(head_path, rel_path)

# -----------------------------------------------------------------------------

def free_library(handle):
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    #kernel32.FreeLibrary.argtypes = [ctypes.wintypes.HMODULE]
    #kernel32.FreeLibrary.restype = ctypes.wintypes.BOOL
    kernel32.FreeLibrary.argtypes = [wintypes.HMODULE]
    kernel32.FreeLibrary.restype = wintypes.BOOL
    kernel32.FreeLibrary(handle)

# -----------------------------------------------------------------------------

# Function will be called per sosi object and return ptr to object name, ptr to coordinate array 
def my_cb_func(id, objrefnum, sosires, pobjname, ndims, ncoords, pcoord_ary, pfilename):
	
    #global has_parent
    global top_parent
    #print('PAR2 before:', top_parent)
    
    #if has_parent == False:
    if top_parent == None:
        #print('--->done')
        top_parent = bpy.data.objects.new("SOSI_Parent", None)
        top_parent.empty_display_size = 1
        #top_parent.empty_display_type = 'PLAIN_AXES'
        top_parent.empty_display_type = 'SPHERE'
        bpy.context.scene.collection.objects.link(top_parent)
        #has_parent = True
        #print('PAR3 after:', top_parent)
        logging.debug(' SOSI_Parent:', top_parent)
	
    objname = pobjname.decode('utf-8')  # Interpret the byte array as utf-8
    #print(objname)
    # NUMPY copy
    a = np.fromiter(pcoord_ary, dtype=np.double, count=ndims * ncoords)
    coord_list = coord_array_to_list(ndims, ncoords, a)
    #print("A", coord_list)
    #bpy.ops.object.mode_set(mode = 'OBJECT')
    filename = pfilename.decode('utf8')
    #print(filename) # pfilename is already utf8
    coll = bldhlp.Collection.get_or_create_linked_subcollection_by_name('SOSI', filename)
    
    if (sodhlp.SosiObjId(id) == sodhlp.SosiObjId.PUNKT):
        ob = bldhlp.Mesh.point_cloud(objname, coord_list)
        
        if bldhlp.get_mesh_obj_named(objname) != None:
            ob = bldhlp.mesh_obj_join_existing(objname, ob)
            #print('  Joined', ob.data)
            logging.debug('  Joined', ob.data)
        else:
            ob.parent = top_parent
            #bpy.context.collection.objects.link(ob)
            coll.objects.link(ob)
        #print('PUNKT {}: Res= 0x{:x} NoOfCoords= {}'.format(objrefnum, sosires, ncoords))
        logging.info('PUNKT {}: Res= 0x{:x} NoOfCoords= {}'.format(objrefnum, sosires, ncoords))
    elif (sodhlp.SosiObjId(id) == sodhlp.SosiObjId.KURVE):
        #print("A", coord_list)
        edg_list = sodhlp.points_to_edglist(coord_list)
        #print("B", edg_list)
        ob = bldhlp.Mesh.point_cloud(objname, coord_list, edg_list)
        
        if bldhlp.get_mesh_obj_named(objname) != None:
            ob = bldhlp.mesh_obj_join_existing(objname, ob)
            #print('  Joined', ob.data)
            logging.debug('  Joined', ob.data)
        else:
            ob.parent = top_parent
            #bpy.context.collection.objects.link(ob)
            coll.objects.link(ob)
        #print('KURVE {}: Res= 0x{:x} NoOfCoords= {}'.format(objrefnum, sosires, ncoords))
        logging.info('KURVE {}: Res= 0x{:x} NoOfCoords= {}'.format(objrefnum, sosires, ncoords))
    elif (sodhlp.SosiObjId(id) == sodhlp.SosiObjId.FLATE):
        #print("A", coord_list)
        edg_list = sodhlp.points_to_edglist(coord_list)
        ob = bldhlp.Mesh.point_cloud(objname, coord_list, edg_list)
        
        if bldhlp.get_mesh_obj_named(objname) != None:
            ob = bldhlp.mesh_obj_join_existing(objname, ob)
            #print('  Joined', ob.data)
            logging.debug('  Joined', ob.data)
        else:
            ob.parent = top_parent
            #ob = bldhlp.Mesh.point_cloud(filename, coord_list, edg_list)
            #bpy.context.collection.objects.link(ob)
            coll.objects.link(ob)
        #print ('FLATE {}: Res= 0x{:x} NoOfCoords= {}'.format(objrefnum, sosires, ncoords))
        logging.info('FLATE {}: Res= 0x{:x} NoOfCoords= {}'.format(objrefnum, sosires, ncoords))
        if (sosires & RES_SOSI_DIMENSION_MISMATCH):
            print('  WARNING: Dimension mismatch in FLATE elements, drawing might be strange.')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = ob
        ob.select_set(True)
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_mode(type="EDGE")
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.edge_face_add() # Make the ngon
        #bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY') # Triangulate
        bpy.ops.object.mode_set(mode = 'OBJECT')
    elif (sodhlp.SosiObjId(id) == sodhlp.SosiObjId.BUEP):
        num_segs = 8
        arc_seg_pts = sogeohlp.arc_pts_segments_3D(coord_list, num_segs)
        edg_list = sodhlp.points_to_edglist(arc_seg_pts)
        ob = bldhlp.Mesh.point_cloud(objname, arc_seg_pts, edg_list)
        
        if bldhlp.get_mesh_obj_named(objname) != None:
            ob = bldhlp.mesh_obj_join_existing(objname, ob)
            #print('  Joined', ob.data)
            logging.debug('  Joined', ob.data)
        else:
            ob.parent = top_parent
            #bpy.context.collection.objects.link(ob)
            coll.objects.link(ob)
        #print('BUEP {}: Res= 0x{:x} NoOfCoords= {}'.format(objrefnum, sosires, ncoords))
        logging.info('BUEP {}: Res= 0x{:x} NoOfCoords= {}'.format(objrefnum, sosires, ncoords))
        
    return 0

# -----------------------------------------------------------------------------

def do_imports():
    logger = sologhlp.get_logger(soset.ACT_LOG_LEVEL)
    global top_parent
    top_parent = None
    
    if soset.USE_DEBUG_DLL_PATH == True:
        dll_path = soset.DEBUG_DLL_PATH
    else:
        rel_path = soset.REL_DLL_PATH
        dll_path = get_full_path(rel_path)
    
    my_dll = ctypes.WinDLL(dll_path)
    
    #Prototype callback
    callback_type = ctypes.CFUNCTYPE(c_int, c_int, c_int, c_int, c_char_p, c_int, c_int, ctypes.POINTER(c_double), c_char_p)
    my_callback = callback_type(my_cb_func)  # Use a variable to avoid garbage collection
    
    # Prototype get_SosiInputObjects()
    my_dll.get_SosiInputObjects.argtypes = [ctypes.POINTER(c_double), ctypes.POINTER(c_double), ctypes.POINTER(c_double), ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_double]
    my_dll.get_SosiInputObjects.restype = c_int
    
    #Prototype process_SosiFiles()
    my_dll.process_SosiFiles.argtypes = [c_int, c_void_p]
    my_dll.process_SosiFiles.restype = c_int
    
    bldscale = 1.0  # bldhlp.LocalUnits.scene_unit_factor() # STRANGE??? Blender takes numbers as m always???
    #print("Blender scale factor:", bldscale)
    #bldhlp.setMyEnvironment()   # TEMPORARY to set my local environment
    
    peasting = (ctypes.c_double)()
    pnorthing = (ctypes.c_double)()
    punity = (ctypes.c_double)()
    clip_end = bldhlp.SceneSettings.get_clip_end()
    #unit_system = bpy.context.scene.unit_settings.system
    #unit_length = bpy.context.scene.unit_settings.length_unit
    #print(unit_system, unit_length)
    unit_system = bldhlp.UnitSettings.scene_unit_system_get()
    unit_length = bldhlp.UnitSettings.scene_unit_length_get()
    unit_scale = bldhlp.UnitSettings.scene_unit_scale_get()
    #print(unit_system, unit_length, unit_scale)
 
    nfiles = my_dll.get_SosiInputObjects(peasting, pnorthing, punity, bldscale, clip_end, unit_system, unit_length, unit_scale)
    # print(peasting, pnorthing, punity, nfiles)
    
    if (nfiles > 0):
        res = my_dll.process_SosiFiles(nfiles, my_callback)
    
    # Unload the lib so we can change and recompile the lib without restarting the Python environment
    lib_handle = my_dll._handle
    #del my_dll
    free_library(lib_handle)
    
    return nfiles
