from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

from frmGenerateMesh import Ui_Dialog
from anuga.pmesh.mesh import *
import copy
import string

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
        if layer.geometryType() == 1 or layer.geometryType() == 2:	# Line or Polygon
          if len( self.featuresOfType(layer, "Type", ["S"]) ) > 0:
            self.listWidgetUserSegments.addItem(layer.name())
          if layer.geometryType() == 1:															# Just a Poly line
            if len( self.featuresOfType(layer, "Type", ["BT"]) ) > 0:
              self.listWidgetBoundaryTags.addItem(layer.name())
          if layer.geometryType() == 2:															# Just a Polygon
            if len( self.featuresOfType(layer, "Type", ["B"]) ) > 0:
              self.comboBoxMeshBoundary.addItem(layer.name())
        elif layer.geometryType() == 0:													# Point
          if len( self.featuresOfType(layer, "Type", ["R"]) ) > 0:
            self.listWidgetUserRegions.addItem(layer.name())
          if len( self.featuresOfType(layer, "Type", ["H"]) ) > 0:
            self.listWidgetUserHoles.addItem(layer.name())
          if len( self.featuresOfType(layer, "Type", ["P"]) ) > 0:
            self.listWidgetUserPoints.addItem(layer.name())
    #filename = QFileDialog.getSaveFileName(self, "Save As", ".", "Text Files (*.txt)")
    
    # Select all in all lists
    i = 0
    while i < self.listWidgetUserSegments.count():
      item = self.listWidgetUserSegments.item(i)
      self.listWidgetUserSegments.setItemSelected( item, True )
      i = i + 1
    i = 0
    while i < self.listWidgetUserRegions.count():
      item = self.listWidgetUserRegions.item(i)
      self.listWidgetUserRegions.setItemSelected( item, True )
      i = i + 1
    i = 0
    while i < self.listWidgetUserHoles.count():
      item = self.listWidgetUserHoles.item(i)
      self.listWidgetUserHoles.setItemSelected( item, True )
      i = i + 1
    i = 0
    while i < self.listWidgetUserPoints.count():
      item = self.listWidgetUserPoints.item(i)
      self.listWidgetUserPoints.setItemSelected( item, True )
      i = i + 1
    i = 0
    while i < self.listWidgetBoundaryTags.count():
      item = self.listWidgetBoundaryTags.item(i)
      self.listWidgetBoundaryTags.setItemSelected( item, True )
      i = i + 1
    
    # Try to guess the boundary layer correctly:
    #self.comboBoxMeshBoundary.setCurrentIndex(1)
    i = 0
    while i < self.comboBoxMeshBoundary.count():
      if self.comboBoxMeshBoundary.itemText(i).find('bound') != -1:
        self.comboBoxMeshBoundary.setCurrentIndex(i)
      i = i + 1


  #====================================================================
  #
  # accept(self)
  #
  #====================================================================
  def accept(self):
    
    outFile = QFileDialog.getSaveFileName(self, 'Save mesh','/home/', ("Meshes (*.tsh)"))
    
    #QMessageBox.information(None, "DEBUG", "" )
    
    vertLayers    = self.vertLayersFromDialog()
    segLayers     = self.segLayersFromDialog()
    regionLayers  = self.regionLayersFromDialog()
    holeLayers    = self.holeLayersFromDialog()
    tagLayers     = self.tagLayersFromDialog()
    
    userVerts, userSegs = self.vertsAndSegsFromLayers( vertLayers, 
                                                       segLayers,
                                                       tagLayers )
    userRegions = self.regionsFromLayers( regionLayers )
    userHoles   = self.holesFromLayers( holeLayers )
    
    m = Mesh( userVertices=userVerts,
              userSegments=userSegs,
              regions=userRegions,
              holes=userHoles )
              
    m.generate_mesh( maximum_triangle_area=200000 )
    m.export_mesh_file( outFile )
    
    # lets pickle this for later
    m.savePickle( str(outFile).replace('.tsh', '.pkl') )
    
    # Import the mesh into QGIS?
    if self.autoLoadMeshCheckBox.isChecked():
      self.meshToGIS( m, outFile )
    
    """ 
      generate the following:
        userSegments, userVertices, holes, regions, geo_reference
      generate
      write out
    """
    pass

  def vertLayersFromDialog(self):
    vertLayers = []
    for selectedItem in self.listWidgetUserPoints.selectedItems():
      vertLayers.append( self.layerByName(selectedItem.text()) )
    return vertLayers
    
  def segLayersFromDialog(self):
    segLayers = []
    segLayers.append( self.layerByName(self.comboBoxMeshBoundary.currentText()) )
    for selectedItem in self.listWidgetUserSegments.selectedItems():
      segLayers.append( self.layerByName(selectedItem.text()) )
    return segLayers
      
  def regionLayersFromDialog(self):
    regionLayers = []
    for selectedItem in self.listWidgetUserRegions.selectedItems():
      regionLayers.append( self.layerByName(selectedItem.text()) )
    return regionLayers
    
  def holeLayersFromDialog(self):
    holeLayers = []
    for selectedItem in self.listWidgetUserHoles.selectedItems():
      holeLayers.append( self.layerByName(selectedItem.text()) )
    return holeLayers
    
  def tagLayersFromDialog(self):
    tagLayers = []
    for selectedItem in self.listWidgetBoundaryTags.selectedItems():
      tagLayers.append( self.layerByName(selectedItem.text()) )
    return tagLayers
    
  def vertsAndSegsFromLayers(self, vertLayers, segLayers, tagLayers):
    userVerts = []
    userSegs = []
    # FIXME - ensure that the tags are put in here too
    for layer in segLayers:
      for entity in self.featuresOfType(layer, "Type", ['B', 'S']):
        firstBalls = None
        recentBalls = None
        i = 0
        while i > -1:
          qPoint = entity.geometry().vertexAt(i)
          # Check for error
          if qPoint.x() == 0.0 and qPoint.y() == 0.0:
            break
          # Check if we already have a vertice here
          balls = None
          for vert in userVerts:
            if abs( qPoint.x() - vert.x ) < 0.001:
              if abs( qPoint.y() - vert.y ) < 0.001:
                # Found a duplicate
                balls = vert
          if balls is None:
            userVerts.append( Vertex(qPoint.x(), qPoint.y()) )
            balls = userVerts[len(userVerts)-1]
          if i == 0: # First vert
            firstBalls = balls
          else:
            #QMessageBox.information(None, "DEBUG", 'adding ' + str(recentBalls) + ' and ' + str(balls) )
            tag = self.tagFromPoints(recentBalls, balls, tagLayers)
            userSegs.append( Segment(recentBalls, balls, tag) )
          recentBalls = balls
          i = i + 1
        """if entity.geometry().type() == 2: # Polygon
          userSegs.append( Segment(recentBalls, firstBalls) )"""
    # Add user defined vertices
    for layer in vertLayers:
      for entity in self.featuresOfType(layer, "Type", ['P']):
        qPoint = entity.geometry().vertexAt(0)
        for vert in userVerts:
          dupVert = False
          if abs( qPoint.x() - vert.x ) < 0.001:
            if abs( qPoint.y() - vert.y ) < 0.001:
              # Dup point
              dupVert = True
          if not dupVert:
            userVerts.append( Vertex(qPoint.x(), qPoint.y()) )
    return userVerts, userSegs
    
  def regionsFromLayers(self, regionLayers):
    userRegions = []
    for layer in regionLayers:
      for entity in self.featuresOfType(layer, "Type", ['R']):
        x = entity.geometry().vertexAt(0).x()
        y = entity.geometry().vertexAt(0).y()
        mArea = self.attributeValue(entity, layer, "MaxTriArea")
        r = Region(X=x, Y=y, maxArea=mArea)
        userRegions.append(r)
    return userRegions
    
  def holesFromLayers(self, holeLayers):
    userHoles = []
    for layer in holeLayers:
      for entity in self.featuresOfType(layer, "Type", ['H']):
        x = entity.geometry().vertexAt(0).x()
        y = entity.geometry().vertexAt(0).y()
        h = Hole(x,y)
        userHoles.append(h)
    return userHoles
    
  def layerByName(self, name):
    mc = self.iface.mapCanvas()
    nLayers = mc.layerCount()
    for l in range(nLayers):
      layer = mc.layer(l)
      if str(layer.name()) == str(name):
        return layer

  # ===================================================================
  #
  # featuresOfType -  returns a list of feature IDs matched by the 
  #                   specified type attribute - this function is shit
  #                   and should be re-written
  #
  # ===================================================================
  def featuresOfType(self, layer, attributeName, values):
    selectedFeatures = []
    provider = layer.dataProvider()
    if provider.fieldNameIndex(attributeName) == -1:
      #QMessageBox.information(None, "ERROR",
      #  "Could not find attribute called %s in layer %s" % (attributeName, layer.name()))
      return []
    for f in provider.getFeatures():
      for val in values:
        if f[attributeName] == val:
          selectedFeatures.append(f)
    return selectedFeatures

  def attributeValue(self, entity, layer, attributeName):
    try:
      return entity[attributeName]
    except KeyError:
      QMessageBox.information(None, "ERROR",
        "Could not find attribute called %s in layer %s" % (attributeName, layer.name()))
    
  def meshToGIS(self, mesh, fileName ):
    """
      Function to write a shape file of triangles from a mesh object
    """
    
    fileName = fileName.replace('c:','')
    fileName = fileName.replace('.tsh','.shp')
    fields = QgsFields()
    fields.append(QgsField("ID", QVariant.Int))
    # Check for existance of file and unlink if it's there
    if os.access(fileName, os.F_OK):
      os.remove(str(fileName))
    
    writer = QgsVectorFileWriter(fileName, "CP1250", fields, QGis.WKBPolygon, None)
    if writer.hasError() != QgsVectorFileWriter.NoError:
      QMessageBox.information(None, "ERROR", "Error when creating shapefile: " + str(writer.hasError()) )
      
    triangles = mesh.getTriangulation()
    verts = mesh.getMeshVertices()
    triID = 0
    for tri in triangles:
      i0 = tri[0]
      i1 = tri[1]
      i2 = tri[2]
      fet = QgsFeature(fields)
      p0 = QgsPoint(verts[i0][0], verts[i0][1])
      p1 = QgsPoint(verts[i1][0], verts[i1][1])
      p2 = QgsPoint(verts[i2][0], verts[i2][1])
      poly = QgsGeometry.fromPolygon( [ [ p0, p1, p2, p0 ] ] )
      fet.setGeometry( poly )
      fet[0] = triID
      writer.addFeature(fet)
      triID += 1
    QMessageBox.information(None, "DEBUG", "Wrote " + str(triID+1) + " triangles" )
    
    del writer
    tmpMeshLayer = QgsVectorLayer(fileName, "AnuGA Mesh", "ogr")
    if not tmpMeshLayer.isValid():
      QMessageBox.information(None, "ERROR", "Failed to load mesh shape file" )
    else:
      QgsMapLayerRegistry.instance().addMapLayer(tmpMeshLayer)
      
    # Create a spatial index in order to speed things up a little
    if tmpMeshLayer.dataProvider().createSpatialIndex() is False:
      QMessageBox.information(None, "ERROR", "Failed to create spatial index" )
    
  def loadMesh(self, fileName ):
    
    from string import split
    
    fileName = fileName.replace('c:','')
    inMesh = open( fileName, "r" )
    if inMesh is None:
      QMessageBox.information(None, "ERROR", "Failed to open " + fileName )
    
    fileName = fileName.replace('.tsh','.shp')
    #QMessageBox.information(None, "DEBUG", "meshFile is " + meshFile + " and shaleFile is " + shapeFile )
    fields = { 0 : QgsField("ID", QVariant.Int) }
    # Check for existance of file and unlink if it's there
    if os.access(fileName, os.F_OK):
      os.remove(str(fileName))
    
    writer = QgsVectorFileWriter(fileName, "CP1250", fields, QGis.WKBLineString, None)
    if writer.hasError() != QgsVectorFileWriter.NoError:
      QMessageBox.information(None, "ERROR", "Error when creating shapefile: " + str(writer.hasError()) )
    
    # Determine how many points we have
    fileLine = inMesh.readline()
    splitLine = split(fileLine)
    #QMessageBox.information(None, "DEBUG", "splitLine is " + splitLine[0] )
    pointCount = int(splitLine[0])
    
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
        
    tmpMeshLayer = QgsVectorLayer(fileName, "AnuGA Mesh", "ogr")
    if not tmpMeshLayer.isValid():
      QMessageBox.information(None, "ERROR", "Failed to load mesh shape file" )
    else:
      QgsMapLayerRegistry.instance().addMapLayer(tmpMeshLayer)
      #QMessageBox.information(None, "DEBUG", "Layer loaded" )
      
    # Create a spatial index in order to speed things up a little
    if tmpMeshLayer.dataProvider().createSpatialIndex() is False:
      QMessageBox.information(None, "ERROR", "Failed to create spatial index" )

  def tagFromPoints(self, p1, p2, tagLayers):
    
    qp1 = QgsPoint(p1.x, p1.y)
    qp2 = QgsPoint(p2.x, p2.y)
    
    for layer in tagLayers:
      for feature in self.featuresOfType(layer, "Type", ['BT']):
        i = 0
        while True:
          thisPoint = feature.geometry().vertexAt(i)
          nextPoint = feature.geometry().vertexAt(i+1)
          if thisPoint.x() == 0.0 and thisPoint.y() == 0.0:
            break
          i = i + 1
          if (qp1 == thisPoint and qp2 == nextPoint) or (qp1 == nextPoint and qp2 == thisPoint):
            return self.attributeValue(feature, layer, 'Tag')
    
    return None
