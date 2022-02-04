# sosi_files_importer for Blender
Importer for SOSI files (containing 3D model data) used for geographical information in Norway.

This is an addon for Blender to allow imports of SOSI files (with extension .sos). This addon is intended to handle the data normally contained in so-called 
"digital maps" available from Norwegian municipal og governmental services.

The add-on was originally written in C++ for Sketchup under 64-bit Windows10. For Blender the appropriate C++ code is compiled into a DLL and called from Python. Thus, this addon is only usable within the Windows environment.

The *scripts* directory contains the sources for the Python code necessary to interface with the WinDLL. The DLL itself is placed in the sub directory *bin\x64*.

It is not recommended to install the addon using the sources directly. Instead, please use the packaged contents in the *release page*. The packaged zip-file can be directly installed from the *Install...* button in the *Blender Preferences* dialog.

Currently, this addon has only been tested with Blender 3.0 and Windows10.

![Example import](/images/ImportExample_0.png)

## Usage

Initially, the importer has to be enabled via the *Edit/preferences* dialog. It can be found as *Import-Export: SosiImporter*.

Run the importer from the *File/Import/Import SOSI Data* menu item.

![Demo import](/images/Importing_1.png)

The importer will then open a file selection dialog expecting a .txt file with a Reference coordinate specification. This coordinate is provided to map the SOSI file 3D data to a region near the Blender coordinate origin. Remember that SOSI data can be located thousands of kilometers away from the origin, a situation Blender - as well as other 3D applications - is not meant to handle.

Thereafter the user is asked for one or more SOSI files. Multiple files can be selected in the dialog.

The appropriate SOSI files are then parsed, one by one. For every selected file a dialog will open and show all SOSI element tags present. The user can choose to include/exclude any tags appropriate for the particular import. Default is inclusion of all element tags.

It is a good idea to open the Blender System Console before doing any imports, as the console will display importing details while processing. Any problems occurring while importing should be indicated in the console window.

## Example .sos file

In order to verify that an addon installation is working properly, an example .sos file is included together with an appropriate reference coordinate file. The .sos file contains only rudimentory data, but is a perfectly valid SOSI file.

The files can be found in the test_data directory:

'''
test_data
|    SomeBorders.sos
|    SomeBorders_ref.txt
|  
└─── 
'''
