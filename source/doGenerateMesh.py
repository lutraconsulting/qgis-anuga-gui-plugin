from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

from frmListBox import Ui_Dialog

import os
from string import split

class Dialog(QDialog, Ui_Dialog):

  #====================================================================
  #
  # __init__ 
  #
  #====================================================================
  def __init__(self, iface):
    
    # Do init stuff
    QDialog.__init__(self)
    self.iface = iface
    self.setupUi(self)
    
    # Populate dialogs
    mapCanvas = self.iface.mapCanvas()
    for i in range(mapCanvas.layerCount()):
      layer = mapCanvas.layer(i)
      if layer.type() == layer.VectorLayer:
        if layer.geometryType() == 2:
          # Found a polygon layer
          self.regionComboBox.addItem(layer.name())
        elif layer.geometryType() == 1:
          # Found a lines layer
          self.boundaryTagComboBox.addItem(layer.name())
          
          
          
  #====================================================================
  #
  # accept -  On user clicking "Generate" a python script will be
  #           created to generate a mesh.
  #
  #           TODO
  #             Add windows support manualCheckBox
  #
  #====================================================================
  def accept(self):
    
    # Set up a temp work directory
    temp_dir = "/tmp/anugaInterface"
    self.setupTempDir(temp_dir)
    
    # Get geo-referencing info from boundary poly layer
    
    
    # Write a CSV describing the boundary polygon to disk
    regionLayerName = self.regionComboBox.currentText()
    regionLayer = self.getVectorLayerByName(regionLayerName)
    # Grab all bounding polygons (there should be only 1)
    boundingPolySelection = self.featuresOfType(regionLayer, "B")
    if len(boundingPolySelection) < 1:
      QMessageBox.information(None, "ERROR", "Did not find any boundary polygons" )
      return
    elif len(boundingPolySelection) > 1:
      QMessageBox.information(None, "ERROR", "Found more than one boundary polygon" )
      return
    regionLayer.setSelectedFeatures(boundingPolySelection)
    boundaryPolyCSVFilename = temp_dir + "/boundingPoly.csv"
    boundaryPolyFeature = regionLayer.selectedFeatures()[0]
    if self.writeCSV(boundaryPolyCSVFilename, boundaryPolyFeature) != 0:
      QMessageBox.information(None, "ERROR", "Could not write out boundary CSV" )
      return
      
    # Store MaxTriArea
    domMaxTriArea = boundaryPolyFeature.attributeMap()[1].toString()
    
    # Write a CSV for each internal region
    internalRegionSelection = self.featuresOfType(regionLayer, "I")
    regionLayer.setSelectedFeatures(internalRegionSelection)
    length = len(internalRegionSelection)
    internalPolyFileNames = []
    internalPolyResolutions = []
    i = 0
    while i < length:
      filename = temp_dir + "/internalPoly_%03d.csv" % (i)
      internalPolyFeature = regionLayer.selectedFeatures()[i]
      internalPolyFileNames.append(filename)
      internalPolyResolutions.append( internalPolyFeature.attributeMap()[1].toString() )
      if not (internalPolyResolutions[i] > 0.0):
        QMessageBox.information(None, "ERROR", "Internal polygon (" + str(i) + ") doesn't have a resolution assigned (" + str(internalPolyResolutions[i]) + ")" )
        return
      if self.writeCSV(filename, internalPolyFeature) != 0:
        QMessageBox.information(None, "ERROR", "Could not write out internal region CSV (" + str(i) + ")" )
        return
      i = i + 1
    
    # Write a CSV for each hole
    internalHoleSelection = self.featuresOfType(regionLayer, "H")
    regionLayer.setSelectedFeatures(internalHoleSelection)
    length = len(internalHoleSelection)
    holePolyFileNames = []
    i = 0
    while i < length:
      filename = temp_dir + "/holePoly_%03d.csv" % (i)
      holePolyFeature = regionLayer.selectedFeatures()[i]
      holePolyFileNames.append(filename)
      if self.writeCSV(filename, holePolyFeature) != 0:
        QMessageBox.information(None, "ERROR", "Could not write out hole region CSV (" + str(i) + ")" )
        return
      i = i + 1
    
    # Construct boundary tags
    boundaryTagLayerName = self.boundaryTagComboBox.currentText()
    boundaryTagLayer = self.getVectorLayerByName(boundaryTagLayerName)
    bTagList = self.createBoundaryTags( regionLayer, boundaryTagLayer )
    
    #Store the minimum triangle area:
    minTriAngle = self.minTriAngleLineEdit.text()
    
    # Get geo-referencing info from boundary poly layer - currently 
    # commented out due to a possible bug in QGIS - tagged already
    srsID = regionLayer.srs().srsid()
    
    # QMessageBox.information(None, "DEBUG", "Just got srsID of " + str(srsID) )
    # srsID = 2992
        
    # Write python script to generate our mesh
    if self.writeMeshGenerationScript( boundaryPolyCSVFilename, domMaxTriArea, minTriAngle, internalPolyFileNames, holePolyFileNames, internalPolyResolutions, bTagList, srsID ) != 0:
      QMessageBox.information(None, "ERROR", "Could not write out mesh generation scripts" )
      return
      
    if self.force24CheckBox.checkState() == 2:
      os.system("python2.4 /tmp/anugaInterface/generateMesh.py")
    elif self.force24CheckBox.checkState() == 0:
      os.system("python /tmp/anugaInterface/generateMesh.py")

    self.asciiMeshToGIS( "/tmp/anugaInterface/genMSH.tsh" )
    
    tmpMeshLayer = QgsVectorLayer("/tmp/anugaInterface/testOut.shp", "Temp Mesh", "ogr")
    if not tmpMeshLayer.isValid():
      QMessageBox.information(None, "ERROR", "Failed to load mesh shape" )
    else:
      QgsMapLayerRegistry.instance().addMapLayer(tmpMeshLayer)
      QMessageBox.information(None, "DEBUG", "Layer loaded" )

    # Execute the python script we just made
    
    # Read in the mesh as GIS layers
      
    #inFileName = "/tmp/anugaInterface/meshGEN.tsh"
    #outFileName = "/tmp/anugaInterface/balls.shp"
    # Mesh should now have been written out - read it into a GIS layer
    #if self.asciiMeshToGIS( inFileName, outFileName ) != 0:
    #  QMessageBox.information(None, "ERROR", "Could not read ASCII mesh" )
    #  return
    #

  
  
  #====================================================================
  # 
  # asciiMeshToGIS -  imports the generated mesh as a collection of 
  #                   lines allowing the user to visualise the mesh in 
  #                   the GIS environment
  # 
  #====================================================================
  def asciiMeshToGIS(self, meshFile):
    
    fields = { 0 : QgsField("ID", QVariant.Int) }
               
    writer = QgsVectorFileWriter("/tmp/anugaInterface/testOut.shp", "CP1250", fields, QGis.WKBLineString, None)
    
    if writer.hasError() != QgsVectorFileWriter.NoError:
      QMessageBox.information(None, "ERROR", "Error when creating shapefile: " + writer.hasError() )
      
    inMesh = open( meshFile, "r" )
    
    # Determine how many points we have
    fileLine = inMesh.readline()
    splitLine = split(fileLine)
    pointCount = int(splitLine[0])
    #QMessageBox.information(None, "DEBUG", splitLine[0] + " Points" )
    
    points = []
    
    i = 0
    while i < pointCount:
      fileLine = inMesh.readline()
      splitLine = split(fileLine)
      xVal = float(splitLine[1])
      yVal = float(splitLine[2])
      # Add the data
      points.append( [xVal, yVal] )
      i = i + 1
      
    fileLine = inMesh.readline()
    fileLine = inMesh.readline()
    splitLine = split(fileLine)
    triCount = int(splitLine[0])
    
    i = 0
    while i < triCount:
      fileLine = inMesh.readline()
      splitLine = split(fileLine)
      triID = int(splitLine[0])
      vertOne = int(splitLine[1])
      vertTwo = int(splitLine[2])
      vertThree = int(splitLine[3])
      
      fet = QgsFeature()
      fet.setGeometry(QgsGeometry.fromPolyline( [QgsPoint(points[vertOne][0],points[vertOne][1]),QgsPoint(points[vertTwo][0],points[vertTwo][1])] ))
      fet.addAttribute(0, QVariant(triID))
      writer.addFeature(fet)
      
      fet = QgsFeature()
      fet.setGeometry(QgsGeometry.fromPolyline( [QgsPoint(points[vertTwo][0],points[vertTwo][1]),QgsPoint(points[vertThree][0],points[vertThree][1])] ))
      fet.addAttribute(0, QVariant(triID))
      writer.addFeature(fet)
      
      fet = QgsFeature()
      fet.setGeometry(QgsGeometry.fromPolyline( [QgsPoint(points[vertThree][0],points[vertThree][1]),QgsPoint(points[vertOne][0],points[vertOne][1])] ))
      fet.addAttribute(0, QVariant(triID))
      writer.addFeature(fet)     
      
      i = i + 1
    
    inMesh.close()
    
    del writer
        
    # Set up a new layer
    
    # Load the mesh file into a structure
    
    # To start with, lets just draw one line
    #prov = destLayer.dataProvider()
    #testFeature = QgsFeature()
    #testFeature.setGeometry(QgsGeometry.fromPoint(QgsPoint(10,10)))
    #testFeature.setGeometry(QgsGeometry.fromPolyline( [ QgsPoint(692219.0,14156225.0), QgsPoint(693018.0,14156967.0) ] ) )
    #testFeature.setAttributeMap( { 0 : QVariant("Johny") } )
    #prov.addFeatures( [ testFeature ] )
    #destLayer.updateExtents()
    #destLayer.triggerRepaint()


    #gem = QgsGeometry.fromWkt( "LINESTRING ( 692219.0 14156225.0, 693018.0 14156967.0)" )
    #testFeature.setGeometry( gem )
    #testFeature.addAttribute( 0, QVariant("arse") )
    #if not destLayer.addFeature( testFeature ):
    #  QMessageBox.information(None, "ERROR", "Failed to add feature" )
    #  return -1
    #return 0
  
  
  
  # ===================================================================
  #
  # writeMeshGenerationScript  -  takes various things we have just
  #                               created such as CSVs and lists of
  #                               boundary tags and writes a python
  #                               script to actually generate the mesh
  # 
  # ===================================================================
  def writeMeshGenerationScript(self, boundaryPolyCSVFilename, domMaxTriArea, minTriAngle, internalPolyFileNames, holePolyFileNames, internalPolyResolutions, bTagList, srsID ):
    try:
      outFile = open( "/tmp/anugaInterface/generateMesh.py", "w" )
    except:
      QMessageBox.information(None, "Error", "File open failed or something, exiting")
      return -1
    
    outFile.write( "######################################\n" )
    outFile.write( "#                                    #\n" )
    outFile.write( "#          ##    ##   ###            #\n" )
    outFile.write( "#         #     #  #   #             #\n" )
    outFile.write( "#         # ##  ####   #             #\n" )
    outFile.write( "#         #  #  #  #   #             #\n" )
    outFile.write( "#          ##   #  #  ###            #\n" )
    outFile.write( "#                                    #\n" )
    outFile.write( "# GIS Anuga Interface auto-generated #\n" )
    outFile.write( "#   script - DO NOT EDIT THIS FILE   #\n" )
    outFile.write( "#                                    #\n" )
    outFile.write( "######################################\n\n" )
    
    outFile.write( "# Import nessisary libs\n" )
    outFile.write( "from anuga.utilities.polygon import read_polygon\n" )
    outFile.write( "from anuga.pmesh.mesh_interface import create_mesh_from_regions\n" )
    outFile.write( "from anuga.coordinate_transforms.geo_reference import Geo_reference\n\n" )
    
    # Determine our UTM zone:
    if srsID > 3043 and srsID < 3104:
      hem = "S"
      zone = srsID - 3043
    elif srsID > 2977 and srsID < 3038:
      hem = "N"
      zone = srsID - 2977
    else:
      QMessageBox.information(None, "ERROR", "SRSID " + str(srsID) + " doesn't appear to be a UTM zone" )
      return -1
    
    outFile.write( "# Geo_reference:\n" )
    outFile.write( "geo_ref = Geo_reference(zone = " + str(zone) + ",\n" )
    outFile.write( "                        xllcorner = 0.0,\n" )
    outFile.write( "                        yllcorner = 0.0,\n" )
    outFile.write( "                        datum = \"wgs84\",\n" )
    outFile.write( "                        projection = \"UTM\",\n" )
    outFile.write( "                        units = \"m\",\n" )
    outFile.write( "                        false_easting = 500000,\n" )
    if hem is "N":
      outFile.write( "                        false_northing = 0)\n\n" )
    else:
      outFile.write( "                        false_northing = 10000000)\n\n" )
    
    outFile.write( "# Bounding polygon for study area\n" )
    outFile.write( "bounding_polygon = read_polygon(\"" + boundaryPolyCSVFilename + "\")\n\n" )
    
    # Write out internal regions
    outFile.write( "# Interior polygons\n" )
    i = 0
    while i < len(internalPolyFileNames):
      outFile.write( "poly_reg" + str(i) + " = read_polygon(\"" + internalPolyFileNames[i] + "\")\n" )
      i = i + 1
    i = 0
    while i < len(holePolyFileNames):
      outFile.write( "hole_reg" + str(i) + " = read_polygon(\"" + holePolyFileNames[i] + "\")\n" )
      i = i + 1
    
    outFile.write( "\n" )
    
    # Write out internal region resolutions
    outFile.write( "# Interior polygons resolutions\n" )
    i = 0
    while i < len(internalPolyResolutions):
      outFile.write( "poly_res" + str(i) + " = " + str(internalPolyResolutions[i]) + "\n" )
      i = i + 1
      
    outFile.write( "\n" )
    if len(internalPolyFileNames) > 0:
      outFile.write( "interior_regions = [" )
    i = 0
    while i < len(internalPolyFileNames):
      if i == 0:
        outFile.write( "[poly_reg" + str(i) + ", poly_res" + str(i) + "]" )
      else:
        outFile.write( "                    [poly_reg" + str(i) + ", poly_res" + str(i) + "]" )
      if i < (len(internalPolyFileNames)-1):
        outFile.write( ",\n" )
      else:
        outFile.write( "]\n" )
      i = i + 1
    #i = 0
    #while i < len(holePolyFileNames):
    #  if i == 0 and len(internalPolyFileNames) < 1:
    #    outFile.write( "[hole_reg" + str(i) + ", hole_res" + str(i) + "]" )
    #  else:
    #    outFile.write( "                    [hole_reg" + str(i) + ", hole_res" + str(i) + "]" )
    #  if i < (len(holePolyFileNames)-1):
    #    outFile.write( ",\n" )
    #  else:
    #    outFile.write( "]\n" )
    #  i = i + 1
      
    outFile.write( "\n" )
    
    if len(holePolyFileNames) > 0:
      outFile.write( "interior_holes = [" )
    i = 0
    while i < len(holePolyFileNames):
      if i == 0:
        outFile.write( "hole_reg" + str(i) )
      else:
        outFile.write( "                  hole_reg" + str(i) )
      if i < (len(holePolyFileNames)-1):
        outFile.write( ",\n" )
      else:
        outFile.write( "]\n" )
      i = i + 1
      
    outFile.write( "\n" )
    
    outFile.write( "create_mesh_from_regions(bounding_polygon,\n" )
    outFile.write( "                         boundary_tags={")
    
    i = 0
    while i < len(bTagList):
      if i == 0:
        outFile.write( "\"TAG_" + str(i) + "\" : [" )
      else:
        outFile.write( "                                        \"TAG_" + str(i) + "\" : [" )
      # now write out the list of segments
      
      j = 0
      while j < len(bTagList[i]):
        outFile.write( str(bTagList[i][j]) )
        if j < (len(bTagList[i])-1):
          outFile.write( ", " )
        j = j + 1
      
      if i < (len(bTagList)-1):
        outFile.write( "],\n" )
      else:
        outFile.write( "]" )
      i = i + 1
    outFile.write( "},\n" )
    outFile.write( "                         maximum_triangle_area=" + str(domMaxTriArea) + ",\n")
    outFile.write( "                         filename=\"/tmp/anugaInterface/genMSH.tsh\",\n")
    if len(internalPolyFileNames) > 0:
      outFile.write( "                         interior_regions=interior_regions,\n")
    if len(holePolyFileNames) > 0:
      outFile.write( "                         interior_holes=interior_holes,\n")
    outFile.write( "                         poly_geo_reference = geo_ref,\n")
    outFile.write( "                         mesh_geo_reference = geo_ref,\n")
    outFile.write( "                         minimum_triangle_angle=" + str(minTriAngle) + ",\n")
    outFile.write( "                         use_cache=False,\n")
    outFile.write( "                         verbose=True)\n\n")
    
    outFile.close()
    return 0

  
  
  # ===================================================================
  #
  # createBoundaryTags -  takes a layer of boundary polygons and a 
  #                       layer of boundary tag lines and returns a 
  #                       pointer to a structure of boundary tags
  #
  # ===================================================================
  def createBoundaryTags(self, regionLayer, tagLayer):
    
    snapTol = 0.1
    
    # Ensure we have a selection in each layer of only the type of
    # objects we want - B(bounding polygon), BT(boundary tags)
    #
    boundaryPolySelection = self.featuresOfType(regionLayer, "B")
    regionLayer.setSelectedFeatures(boundaryPolySelection)
    boundaryTagLineSelection = self.featuresOfType(tagLayer, "BT")
    tagLayer.setSelectedFeatures(boundaryTagLineSelection)
    
    boundaryPoly = regionLayer.selectedFeatures()[0]
    
    bTagList = []
    
    bTagCount = len(boundaryTagLineSelection)
    i = 0
    while i < bTagCount:
      # for each tag, loop through all verts
      bTagList.append([])
      tag = tagLayer.selectedFeatures()[i]
      j = 0
      while j > -1:
        tagVertX = tag.geometry().vertexAt(j).x()
        tagVertY = tag.geometry().vertexAt(j).y()
        if tagVertX == 0.0 and tagVertY == 0.0:
          break
        # Look for a corresponding boundary polygon vertice:
        k = 0
        while k > -1:
          # Loop through boundary poly verts
          boundaryVertX = boundaryPoly.geometry().vertexAt(k).x()
          boundaryVertY = boundaryPoly.geometry().vertexAt(k).y()
          if boundaryVertX == 0.0 and boundaryVertY == 0.0:
            break
          if abs(boundaryVertX - tagVertX) <= snapTol and abs(boundaryVertY - tagVertY) <= snapTol:
            # We have a snapped vertice
            # QMessageBox.information(None, "DEBUG", "Tag " + str(i) + " has tVert " + str(j) + " snapped to bVert " + str(k) )
            bTagList[i].append(k)
            break
          k = k + 1
        j = j + 1
      # We should have not populated a list of boundingPoly verts, lets sort them
      bTagList[i].sort()
      # Now remove the last val to make it a list of segment IDs
      lastItemID = len(bTagList[i]) - 1
      # QMessageBox.information(None, "DEBUG", "Last ID is " + str(lastItemID) )
      del bTagList[i][lastItemID]
      i = i + 1
      
    # QMessageBox.information(None, "DEBUG", "bTagList[0][0] is " + str( bTagList[0][0] ) )
    # QMessageBox.information(None, "DEBUG", "bTagList[0][0] is " + str( bTagList[1][0] ) )
    
    return bTagList
    
    
    
  # ===================================================================
  #
  # writeCSV -  writes out the selected feature to a CSV file
  #
  # ===================================================================
  def writeCSV(self, filename, feature):
    try:
      outFile = open( filename, "w" )
    except:
      QMessageBox.information(None, "Error", "File open failed or something, exiting")
      return -1
    i = 0
    while i > -1:
      currentX = feature.geometry().vertexAt(i).x()
      currentY = feature.geometry().vertexAt(i).y()
      if currentX == 0.0 and currentY == 0.0:
        break
      outFile.write( str(currentX) + "," + str(currentY) + "\n" )
      i = i + 1
    outFile.close()
    return 0
  
  
  
  # ===================================================================
  #
  # featuresOfType -  returns a list of feature IDs matched by the 
  #                   specified type attribute
  #
  # ===================================================================
  def featuresOfType(self, selectedRegionLayer, type):
    f=QgsFeature()
    selection = []
    provider = selectedRegionLayer.dataProvider()
    #provider.reset()
    fieldmap=provider.fields()
    col = -1
    for (k,attr) in fieldmap.iteritems():      
      if ("Type"==attr.name()):
        #QMessageBox.information(None, "DEBUG", "Found type at " + str(k) )
        col = k
        allAttrs = provider.attributeIndexes()
        provider.select(allAttrs)
    if col == -1:
      QMessageBox.information(None, "ERROR", "Could not find attribute called \"Type\" in this layer" )
      return selection
    while (provider.nextFeature(f)):
      fieldmap=f.attributeMap()
      #QMessageBox.information(None, "DEBUG", "Looking at feature with " + str(len(fieldmap)) + " fields" )
      if fieldmap[col].toString() == type:
        selection.append(f.id())
        #QMessageBox.information(None, "DEBUG", "Found one" )
    return selection
  
  
  
  #====================================================================
  #
  # setupTempDir -  creates a volatile temporary working area
  #
  #====================================================================
  def setupTempDir(self, dir):
    
    # Remove the area
    if dir[-1] == os.sep:
      dir = dir[:-1]
    if os.path.isdir(dir):
      files = os.listdir(dir)
      for file in files:
        if file == '.' or file == '..':
          continue
        path = dir + os.sep + file
        try:
          os.unlink(path)
        except:
          QMessageBox.information(None, "DEBUG", "A problem occured while cleaning the temp area" )
    else:
      try:
        os.makedirs(dir)
      except OSError:
        QMessageBox.information(None, "ERROR", "Could not create temporary directory " + dir)
        return
      except:
        QMessageBox.information(None, "Unexpected Error", "Failed to create temp working area")
        return



  #====================================================================
  #
  # getVectorLayerByName -  gets a pointer to a layer using the layer
  #                         name as a reference
  #
  #====================================================================
  def getVectorLayerByName(self, myName):
    mc = self.iface.mapCanvas()
    nLayers = mc.layerCount()
    for l in range(nLayers):
      layer = mc.layer(l)
      if str(layer.name()) == str(myName):
      	return layer
        # vlayer = QgsVectorLayer(str(layer.source()),  str(myName),  str(layer.dataProvider().name()))
        # if vlayer.isValid():
        #   return vlayer
