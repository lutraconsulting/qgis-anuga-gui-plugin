# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

#import doGenerateMesh
import doGenerateMeshNG
#import doAuditMesh

import resources

# Our main class for the plugin
class AnugaInterface:

  def __init__(self, iface):
    # Save reference to the QGIS interface
    self.iface = iface

  def initGui(self):
    # Create Generate Mesh action
    #self.generateMeshAction = QAction(QIcon(":/plugins/anugaInterface/generateMesh.png"), "Generate Mesh", self.iface.mainWindow())
    self.generateMeshNGAction = QAction(QIcon(":/plugins/anugaInterface/generateMesh.png"), "Generate Mesh", self.iface.mainWindow())
    #self.auditMeshAction = QAction(QIcon(":/plugins/anugaInterface/auditMesh.png"), "Audit Mesh", self.iface.mainWindow())
    #self.generateMeshAction.setWhatsThis("Tool for generating an ANUGA mesh")
    self.generateMeshNGAction.setWhatsThis("Tool for generating an ANUGA mesh (NG)")
    #self.auditMeshAction.setWhatsThis("Analyse mesh quality and highlight suspect elements")
    #QObject.connect(self.generateMeshAction, SIGNAL("activated()"), self.generateMesh)
    QObject.connect(self.generateMeshNGAction, SIGNAL("activated()"), self.generateMeshNG)
    #QObject.connect(self.auditMeshAction, SIGNAL("activated()"), self.auditMesh)
    
    # Add toolbar button and menu item
    #self.iface.addToolBarIcon(self.generateMeshAction)
    self.iface.addToolBarIcon(self.generateMeshNGAction)
    #self.iface.addToolBarIcon(self.auditMeshAction)
    #self.iface.addPluginToMenu("&Anuga Interface", self.generateMeshAction)

  def unload(self):
    # Remove the plugin menu item and icon
    #self.iface.removePluginMenu("&Anuga Interface",self.generateMeshAction)
    #self.iface.removeToolBarIcon(self.generateMeshAction)
    self.iface.removeToolBarIcon(self.generateMeshNGAction)
    #self.iface.removeToolBarIcon(self.auditMeshAction)

  """def generateMesh(self):
    d = doGenerateMesh.Dialog(self.iface)
    d.exec_()"""
	
  def generateMeshNG(self):
    d = doGenerateMeshNG.Dialog(self.iface)
    d.exec_()
    
  """def auditMesh(self):
    d = doAuditMesh.Dialog(self.iface)
    d.exec_()"""
