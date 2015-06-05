from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

from anuga.pmesh.mesh import *

from frmAuditMesh import Ui_Dialog

from Numeric import array, size, zeros
import Numeric
import time

class Dialog(QDialog, Ui_Dialog):

  def __init__(self, iface):
    
    # Do init stuff
    QDialog.__init__(self)
    self.iface = iface
    self.setupUi(self)

  def accept(self):
    
    m = self.getPickledMesh()
    
    # Create some Numeric arrays for the mesh (much faster)
    triangleNumArray = m.getTriangulation()
    verticeNumArray = m.getMeshVertices()
    #QMessageBox.information(None, "DEBUG", 'Tri 0 has verts ' + str(self.triangleNumArray[0]) )
    #QMessageBox.information(None, "DEBUG", 'Vert 942 is at ' + str(self.verticeNumArray[942]) )
    triCnt = len(triangleNumArray)
    verCnt = len(verticeNumArray)
    triangleNumArray = array( triangleNumArray, Numeric.Int32 )
    #verticeNumArray = array( verticeNumArray, Numeric.Int32 )
    
    # Blank list of neighbors
    neighbors         = zeros( (triCnt, 3), Numeric.Int32 )
    linkedNeighborCnt = zeros( triCnt, Numeric.Int32 )
    
    self.progressBar.setMinimum(0)
    self.progressBar.setMaximum(triCnt)
    
    startTime = time.time()
    for T in xrange(triCnt):
      self.progressBar.setValue(T)
      if linkedNeighborCnt[T] < 3:
        me = triangleNumArray[T]
        for t in xrange(triCnt):
          if linkedNeighborCnt[t] < 3 and t != T:
            them = triangleNumArray[t]
            commonVerts = 0
            for i in xrange(3):
              if them[i] == me[0] or them[i] == me[1] or them[i] == me[2]:
                commonVerts += 1
            if commonVerts == 2:
              add = True
              for i in xrange(linkedNeighborCnt[T]):
                if neighbors[T][i] == t:
                  add = False
              if add:
                neighbors[T][linkedNeighborCnt[T]] = t
                linkedNeighborCnt[T] += 1
                """except:
                  QMessageBox.information(None, 'DEBUG', 'T is ' + str(T) )
                  QMessageBox.information(None, 'DEBUG', 'its neighbors are ' + str(neighbors[T]) )
                  QMessageBox.information(None, 'DEBUG', 'we tried to add ' + str(t) )"""
                neighbors[t][linkedNeighborCnt[t]] = T
                linkedNeighborCnt[t] += 1
    
    QMessageBox.information(None, 'DEBUG', 'Done in ' + str(time.time() - startTime) + ' seconds' )
    
    """badTriAreaCnt = 0
    balls = 0
    for tri in self.triangleNumArray[:]:
      currentArea = self.tri_area(tri)
      #QMessageBox.information(None, "DEBUG", 'Tri ' + str(balls) + ' has area ' + str(currentArea) )
      for nTri in self.getTriNeighbors(tri):
        a = self.tri_area(nTri)
        if a >= currentArea:
          ratio = a / currentArea
        else:
          ratio = currentArea / a
        if ratio > 1.5:
          badTriAreaCnt += 1
          #QMessageBox.information(None, "DEBUG", 'Tri ' + str(balls) + ' has ratio of  ' + str(ratio) )
      balls += 1
    QMessageBox.information(None, "DEBUG", str(badTriAreaCnt) + ' dodgy triangles' )"""
    
  def findNeighbors(self, idx):
    neighbors = []
    me = self.triangleNumArray[idx]
    for triIdx in range(self.triCnt):
      if self.linkedNeighborCnt[triIdx] < 3 and triIdx != idx:
        them = self.triangleNumArray[triIdx]
        commonVerts = 0
        for i in range(3):
          if them[i] == me[0] or them[i] == me[1] or them[i] == me[2]:
            commonVerts += 1
        if commonVerts == 2:
          neighbors.append(triIdx)
          # note that it's been taken
          self.linkedNeighborCnt[triIdx] += 1
    return neighbors

  def tri_area(self, tri):
    area = 0.0
    vertices = []
    for v_index in range(3):
        vertices.append(self.verticeNumArray[tri[v_index]])
    #vertices = array(vertices)
    
    ax = vertices[0][0]
    #QMessageBox.information(None, "DEBUG", 'ax is ' + str(ax) )
    ay = vertices[0][1]
    
    bx = vertices[1][0]
    by = vertices[1][1]
    
    cx = vertices[2][0]
    cy = vertices[2][1]
    
    area = abs((bx*ay-ax*by)+(cx*by-bx*cy)+(ax*cy-cx*ay))/2
    return area            

  def getPickledMesh(self):
    import os
    import string
    # Look for a pickled mesh with the same file path and prefix as the 
    # selected layer
    meshLayer = self.iface.activeLayer()
    if meshLayer is None:
      QMessageBox.information(None, "ERROR", 'Please select the mesh layer' )
      return
    meshLayerSrc = meshLayer.source()
    if str(meshLayerSrc).find('.shp') < 0:
      meshLayerSrc = str(meshLayerSrc) + '.pkl'
    else:
      meshLayerSrc = str(meshLayerSrc).replace('.shp','.pkl')
    if not os.access(meshLayerSrc, os.F_OK):
      QMessageBox.information(None, "ERROR", 'Could not find pickled mesh ' + meshLayerSrc )
      return
    # pickled mesh exists, open it
    m = loadPickle(meshLayerSrc)
    return m
