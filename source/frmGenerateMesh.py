# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmGenerateMesh.ui'
#
# Created: Sun Dec  2 12:00:01 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(792, 551)
        self.formLayout = QtGui.QFormLayout(Dialog)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelMeshBoundary = QtGui.QLabel(Dialog)
        self.labelMeshBoundary.setObjectName(_fromUtf8("labelMeshBoundary"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelMeshBoundary)
        self.comboBoxMeshBoundary = QtGui.QComboBox(Dialog)
        self.comboBoxMeshBoundary.setObjectName(_fromUtf8("comboBoxMeshBoundary"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBoxMeshBoundary)
        self.labelUserSegments = QtGui.QLabel(Dialog)
        self.labelUserSegments.setObjectName(_fromUtf8("labelUserSegments"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.labelUserSegments)
        self.listWidgetUserSegments = QtGui.QListWidget(Dialog)
        self.listWidgetUserSegments.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listWidgetUserSegments.setObjectName(_fromUtf8("listWidgetUserSegments"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.listWidgetUserSegments)
        self.labelUserRegions = QtGui.QLabel(Dialog)
        self.labelUserRegions.setObjectName(_fromUtf8("labelUserRegions"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.labelUserRegions)
        self.listWidgetUserRegions = QtGui.QListWidget(Dialog)
        self.listWidgetUserRegions.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listWidgetUserRegions.setObjectName(_fromUtf8("listWidgetUserRegions"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.listWidgetUserRegions)
        self.labelUserHoles = QtGui.QLabel(Dialog)
        self.labelUserHoles.setObjectName(_fromUtf8("labelUserHoles"))
        self.formLayout.setWidget(12, QtGui.QFormLayout.LabelRole, self.labelUserHoles)
        self.listWidgetUserHoles = QtGui.QListWidget(Dialog)
        self.listWidgetUserHoles.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listWidgetUserHoles.setObjectName(_fromUtf8("listWidgetUserHoles"))
        self.formLayout.setWidget(12, QtGui.QFormLayout.FieldRole, self.listWidgetUserHoles)
        self.labelUserPoints = QtGui.QLabel(Dialog)
        self.labelUserPoints.setObjectName(_fromUtf8("labelUserPoints"))
        self.formLayout.setWidget(16, QtGui.QFormLayout.LabelRole, self.labelUserPoints)
        self.listWidgetUserPoints = QtGui.QListWidget(Dialog)
        self.listWidgetUserPoints.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listWidgetUserPoints.setObjectName(_fromUtf8("listWidgetUserPoints"))
        self.formLayout.setWidget(16, QtGui.QFormLayout.FieldRole, self.listWidgetUserPoints)
        self.labelBoundaryTags = QtGui.QLabel(Dialog)
        self.labelBoundaryTags.setObjectName(_fromUtf8("labelBoundaryTags"))
        self.formLayout.setWidget(20, QtGui.QFormLayout.LabelRole, self.labelBoundaryTags)
        self.listWidgetBoundaryTags = QtGui.QListWidget(Dialog)
        self.listWidgetBoundaryTags.setObjectName(_fromUtf8("listWidgetBoundaryTags"))
        self.formLayout.setWidget(20, QtGui.QFormLayout.FieldRole, self.listWidgetBoundaryTags)
        self.labelMinimumTriangleArea = QtGui.QLabel(Dialog)
        self.labelMinimumTriangleArea.setObjectName(_fromUtf8("labelMinimumTriangleArea"))
        self.formLayout.setWidget(24, QtGui.QFormLayout.LabelRole, self.labelMinimumTriangleArea)
        self.lineEditMinimumTriangleArea = QtGui.QLineEdit(Dialog)
        self.lineEditMinimumTriangleArea.setMaxLength(3)
        self.lineEditMinimumTriangleArea.setObjectName(_fromUtf8("lineEditMinimumTriangleArea"))
        self.formLayout.setWidget(24, QtGui.QFormLayout.FieldRole, self.lineEditMinimumTriangleArea)
        self.autoLoadMeshCheckBox = QtGui.QCheckBox(Dialog)
        self.autoLoadMeshCheckBox.setObjectName(_fromUtf8("autoLoadMeshCheckBox"))
        self.formLayout.setWidget(25, QtGui.QFormLayout.FieldRole, self.autoLoadMeshCheckBox)
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonClose = QtGui.QPushButton(self.widget)
        self.pushButtonClose.setObjectName(_fromUtf8("pushButtonClose"))
        self.horizontalLayout.addWidget(self.pushButtonClose)
        self.pushButtonGenerate = QtGui.QPushButton(self.widget)
        self.pushButtonGenerate.setObjectName(_fromUtf8("pushButtonGenerate"))
        self.horizontalLayout.addWidget(self.pushButtonGenerate)
        self.formLayout.setWidget(26, QtGui.QFormLayout.SpanningRole, self.widget)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButtonGenerate, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.accept)
        QtCore.QObject.connect(self.pushButtonClose, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.labelMeshBoundary.setText(QtGui.QApplication.translate("Dialog", "Mesh Boundary", None, QtGui.QApplication.UnicodeUTF8))
        self.labelUserSegments.setText(QtGui.QApplication.translate("Dialog", "User Segments", None, QtGui.QApplication.UnicodeUTF8))
        self.labelUserRegions.setText(QtGui.QApplication.translate("Dialog", "User Regions", None, QtGui.QApplication.UnicodeUTF8))
        self.labelUserHoles.setText(QtGui.QApplication.translate("Dialog", "User Holes", None, QtGui.QApplication.UnicodeUTF8))
        self.labelUserPoints.setText(QtGui.QApplication.translate("Dialog", "User Points", None, QtGui.QApplication.UnicodeUTF8))
        self.labelBoundaryTags.setText(QtGui.QApplication.translate("Dialog", "Boundary Tags", None, QtGui.QApplication.UnicodeUTF8))
        self.labelMinimumTriangleArea.setText(QtGui.QApplication.translate("Dialog", "Minimum Triangle Angle (degrees)", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditMinimumTriangleArea.setText(QtGui.QApplication.translate("Dialog", "28", None, QtGui.QApplication.UnicodeUTF8))
        self.autoLoadMeshCheckBox.setText(QtGui.QApplication.translate("Dialog", "Automatically Load Mesh into GIS", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonClose.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonGenerate.setText(QtGui.QApplication.translate("Dialog", "Generate", None, QtGui.QApplication.UnicodeUTF8))

