# sosi_files_importer for Blender
Importer for SOSI files (containing 3D model data) used for geographical information in Norway. SOSI stands for Systematic Organization of Spatial Information. This format was first standardized around 1990 by *Statens Kartverk*, and is still in active use in Norway.

This is an addon for Blender to allow imports of SOSI files (with extension .sos). This addon is intended to handle the data normally contained in so-called 
"digital maps" available from Norwegian municipal og governmental services.

The add-on was originally written in C++ for Sketchup under 64-bit Windows10. For Blender the appropriate C++ code is compiled into a DLL and called from Python. Thus, this addon is only usable within the Windows environment.

The *scripts/sosi_files_importer/* directory contains the sources for the Python code necessary to interface with the WinDLL. The DLL itself is placed in the sub directory *bin/x64/*.

Currently, this addon has only been tested with Blender 3.0 and Windows10.

![Example import](/images/ImportExample_0.png)

## Installation

While certainly possible, it is not recommended to install the addon using the sources directly. Instead, please use the packaged contents in the *Release page*. The packaged zip-file can be directly installed from the *Install...* button in the *Blender Preferences* dialog.

## Usage

Initially, the importer has to be enabled via the *Edit/preferences* dialog. It can be found as *Import-Export: SosiImporter*.

![Demo import 0](/images/Importing_0.png)

Run the importer from the *File/Import/Import SOSI Data* menu item.

![Demo import 1](/images/Importing_1.png)

The importer will then open a file selection dialog expecting a .txt file with a Reference coordinate specification. This coordinate is provided to map the SOSI file 3D data to a region near the Blender coordinate origin. Remember that SOSI data can be located thousands of kilometers away from the origin, a situation Blender - as well as other 3D applications - is not meant to handle. Please observe that Blender has a Clip-end setting to cut off geometry which is located further from the origin than specified by this setting.

Thereafter the user is asked for one or more SOSI files. Multiple files can be selected in the dialog.

The appropriate SOSI files are then parsed, one by one. For every selected file a dialog will open and show all SOSI element tags present. The user can choose to include/exclude any tags appropriate for the particular import. Default is inclusion of all element tags.

It is a good idea to open the Blender System Console before doing any imports, as the console will display importing details while processing. Any problems occurring while importing should be indicated in the console window.

## Example .sos file

In order to verify that an addon installation is working properly, the sources also include an example .sos file together with an appropriate reference coordinate file. The .sos file contains only rudimentory data, but is a perfectly valid SOSI file.

The example files can be found in the test_data directory:

```
test_data
|    SomeBorders.sos
|    SomeBorders_ref.txt
|  
└─── 
```

The result in Blender after import should look like this:

![TestFile import](/images/SomeBorders.png)

## File Format

The documentation for the SOSI format could certainly be better, but some documentation can be found via the link https://www.kartverket.no/geodataarbeid/standardisering/sosi-standarder2.

The format for the Reference file is pretty straight-forward. It simply takes two lines, one starting with E (for Easting) and one starting with N (for Northing). The float values after the letters are the corresponding coordinates values. The SOSI file data will be translated such that the Blender model origin will correspond to these coordinates.

```
E579843.71
N6635218.06
```

SOSI file ordered from public sources will come with UTM coordinates, which uses the notation Easting and Northing. It is beyond the scope of this document to further dive into this matter. https://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system gives a good insight into the UTM system.
