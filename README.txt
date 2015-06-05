This is a simple plugin to generate mesh for AnuGA:
https://github.com/GeoscienceAustralia/anuga_core

Requirements
You need to have AnuGA and QGIS installed on your computer.

Installation
Download this repo as zip file, extract the zip file and place the folder under QGIS plugin directory (in Windows for example: C:\Users\NAME\.qgis2\python\plugins\ in Linux: ~/.qgis2/plugins/python

How to use AnuGA-GUI
First you need to define your GIS input layers:

Define a poly layer for defining areas of different resolution with attributes Type (char) MaxTriArea (float)
  Type:
    B - boundary poly
    H - hole (needn't have a maxtriarea)
    I - internal region
    
Define a line layer, with the following atts, snap is to the B entity above
    Type (char) - "BT" boundary tag
    Name (char) it's name

Run the plugin and select relevant layers to generate mesh.