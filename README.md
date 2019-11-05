# export-attachments-named-from-field

NW October 2019

ArcGIS Script Tool to export Survey123 attachments with meaningful filenames

ArcGIS does not natively provide a way to bulk export attachments from Survey123 field data. This tool expands on the
simple script created by Esri (https://support.esri.com/en/technical-article/000011912) by allowing the user to specify
an attribute field from which to derive filenames of exported attachments.

This is very useful if, for example, you have collected many photos of different plants and wish to save each
photo as a jpg using the species name (a number is appended to filenames to prevent duplication).

Works in ArcMap 10x or ArcGIS Pro.

Two files are included in this repository: the .py containing the script logic and a .tbx containing the tool
file configuration to be loaded within the ArcGIS UI.


