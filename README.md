# qgis-anuga-gui-plugin
Graphical interface for generating mesh for AnuGA model

This is a simple plugin to generate mesh for AnuGA:

https://github.com/GeoscienceAustralia/anuga_core

# Requirements
You need to have AnuGA and QGIS installed on your computer.

# Installation
Download this repo as zip file, extract the zip file and place the folder under QGIS plugin directory (in Windows for example: C:\Users\NAME\.qgis2\python\plugins\ in Linux: ~/.qgis2/plugins/python

# How to use AnuGA-GUI
First you need to define your GIS input layers:

Define a polygon layer for defining areas of different resolution with attributes Type (char) MaxTriArea (float)

  * Type (char):
     + B - boundary polygon
     + H - hole (needn't have a maxtriarea)
     + I - internal region
  * MaxTriArea (decimal)
	 + Maximum triangle area
Define a line layer, with the following attributes, ensure the layer is snapped to the boundary polygon entity above

  * Type (char):
     + BT - boundary tag
  * Name (char)
	 + its name

Run the plugin and select relevant layers to generate mesh.