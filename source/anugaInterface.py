# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import doGenerateMesh

import resources

# Our main class for the plugin
class AnugaInterface:

  def __init__(self, iface):
    # Save reference to the QGIS interface
    self.iface = iface

  def initGui(self):
    # Create Generate Mesh action
    self.generateMeshAction = QAction(QIcon(":/plugins/anugaInterface/generateMesh.png"), "Generate Mesh", self.iface.getMainWindow())
    self.generateMeshAction.setWhatsThis("Tool for generating an ANUGA mesh")
    QObject.connect(self.generateMeshAction, SIGNAL("activated()"), self.generateMesh)
    
    # Add toolbar button and menu item
    self.iface.addToolBarIcon(self.generateMeshAction)
    self.iface.addPluginMenu("&Anuga Interface", self.generateMeshAction)

  def unload(self):
    # Remove the plugin menu item and icon
    self.iface.removePluginMenu("&Anuga Interface",self.generateMeshAction)
    self.iface.removeToolBarIcon(self.generateMeshAction)

  def generateMesh(self):
    d = doGenerateMesh.Dialog(self.iface)
    d.exec_()
