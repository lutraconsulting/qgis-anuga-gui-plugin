# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmListBox.ui'
#
# Created: Fri Aug  8 11:01:21 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,252,175).size()).expandedTo(Dialog.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(Dialog)
        self.gridlayout.setObjectName("gridlayout")

        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,3)

        self.regionComboBox = QtGui.QComboBox(Dialog)
        self.regionComboBox.setObjectName("regionComboBox")
        self.gridlayout.addWidget(self.regionComboBox,1,0,1,3)

        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,2,0,1,3)

        self.boundaryTagComboBox = QtGui.QComboBox(Dialog)
        self.boundaryTagComboBox.setObjectName("boundaryTagComboBox")
        self.gridlayout.addWidget(self.boundaryTagComboBox,3,0,1,3)

        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,4,0,1,2)

        self.minTriAngleLineEdit = QtGui.QLineEdit(Dialog)
        self.minTriAngleLineEdit.setObjectName("minTriAngleLineEdit")
        self.gridlayout.addWidget(self.minTriAngleLineEdit,4,2,1,1)

        self.generateButton = QtGui.QPushButton(Dialog)
        self.generateButton.setObjectName("generateButton")
        self.gridlayout.addWidget(self.generateButton,5,0,1,1)

        self.closeButton = QtGui.QPushButton(Dialog)
        self.closeButton.setObjectName("closeButton")
        self.gridlayout.addWidget(self.closeButton,5,1,1,2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.closeButton,QtCore.SIGNAL("clicked()"),Dialog.close)
        QtCore.QObject.connect(self.generateButton,QtCore.SIGNAL("clicked()"),Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "ANUGA Interface - Generate Mesh", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Region Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Boundary Tag Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Minimum Triangle Angle (degrees)", None, QtGui.QApplication.UnicodeUTF8))
        self.minTriAngleLineEdit.setText(QtGui.QApplication.translate("Dialog", "28", None, QtGui.QApplication.UnicodeUTF8))
        self.generateButton.setText(QtGui.QApplication.translate("Dialog", "Generate", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

