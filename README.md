# sosi_files_importer for Blender
Importer for SOSI files (containing 3D model data) used for geographical information in Norway.

This is an addon for Blender to allow imports of SOSI files (with extension .sos). This addon is intended to handle the data normally contained in so-called 
"digital maps" available from Norwegian municipal og governmental services.

The add-on was originally written in C++ for Sketchup under 64-bit Windows10. For Blender the appropriate C++ code is compiled into a DLL and called from Python. Thus, this addon is only usable within the Windows environment.

The *scripts* directory contains the sources for the Python code necessary to interface with the WinDLL. The DLL itself is placed in the sub directory *bin\x64*.

It is not recommended to install the addon using the sources directly. Instead, please use the packaged contents in the *release page*. The packaged zip-file can be directly installed from the *Install...* button in the *Blender Preferences* dialog.

Currently, this addon has only been tested with Blender 3.0 and Windows10.

## Usage

Activate the importer from the *File/Import/Import SOSI Data* menu item.

The importer will then open a file selection dialog expecting a Reference coordinate specification.
