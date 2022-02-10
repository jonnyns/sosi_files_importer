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

# Info for add-on install
bl_info = {
    "name": "SosiImporter",
    "author": "Jonny Normann Skålvik",
    "version": (1, 1, 0),
    "blender": (2, 93, 0),
    "location": "File > Import > SosiImporter",
    "description": "Import objects from SOSI files (.sos)",
    "warning": "",
    "wiki_url": "",
    "category": "Import-Export",
}

import os

# Determine if the code is running from within Blender
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

# -----------------------------------------------------------------------------

def main(context):
    sosimp.do_imports()

# -----------------------------------------------------------------------------

class ImportSOSIData(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "import_files.sosi_data"
    bl_label = "Import SOSI Data"

    def execute(self, context):
        main(context)
        return {'FINISHED'}

# -----------------------------------------------------------------------------
    
def menu_func_import(self, context):
    self.layout.operator(ImportSOSIData.bl_idname)

# -----------------------------------------------------------------------------

def register():
    bpy.utils.register_class(ImportSOSIData)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

# -----------------------------------------------------------------------------

def unregister():
    bpy.utils.unregister_class(ImportSOSIData)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.import_files.sosi_data()

