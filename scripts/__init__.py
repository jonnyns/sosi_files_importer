# -*- coding: utf-8 -*-
# Copyright (c) 2021 Jonny Normann Skålvik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# The Software is provided “as is”, without warranty of any kind, express or
# implied, including but not limited to the warranties of merchantability,
# fitness for a particular purpose and noninfringement. In no event shall
# the authors or copyright holders be liable for any claim, damages or other
# liability, whether in an action of contract, tort or otherwise, arising from,
# out of or in connection with the software or the use or other dealings in the
# Software.
#
# This file is part of SosiImporter, an addon to import SOSI files containing
# 3D model data.
# SOSI is a geospatial vector data format predominantly used for exchange of
# geographical information in Norway.
# This addon is intended to handle the data normally contained in so-called 
# "digital maps" available from Norwegian municipal og governmental services.
# The add-on was originally written in C++ for Sketchup under 64-bit Windows 10.
# For Blender the C++ code is compiled into a DLL and called from python.

# Info for add-on install
bl_info = {
    "name": "SosiImporter",
    "author": "Jonny Normann Skålvik",
    "version": (0, 9, 0),
    "blender": (2, 93, 0),
    "location": "File > Import > SosiImporter",
    "description": "Import objects from SOSI files (.sos)",
    "warning": "",
    "wiki_url": "",
    "category": "Import-Export",
}

import os

# Determine if the code is running from within Belnder
env_blender = True
try:
    import bpy
    env_blender = os.path.basename(bpy.app.binary_path or '').lower().startswith('blender')
except ModuleNotFoundError:
    env_blender = False   
print('INFO: Blender environment:', env_blender)

#print(__file__)
#print(os.path.abspath(__file__))
#print(os.path.dirname(os.path.abspath(__file__)))

# To support reload properly, try to access a package var, 
# if it's there, reload everything
#if "bpy" in locals():
#	import imp
#	imp.reload(blender_temporary)
#else:
#	from . import blender_temporary as bldtmp

from . import sosi_importer as sosimp	
#from . import blender_temporary as bldtmp

def main(context):
    #print("Ooopppsssss2")
    #bldtmp.my_fnc()
    sosimp.do_imports()


class ImportSOSIData(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "import_files.sosi_data"
    bl_label = "Import SOSI Data"

    def execute(self, context):
        main(context)
        return {'FINISHED'}

    
def menu_func_import(self, context):
    self.layout.operator(ImportSOSIData.bl_idname)


def register():
    bpy.utils.register_class(ImportSOSIData)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportSOSIData)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.import_files.sosi_data()

