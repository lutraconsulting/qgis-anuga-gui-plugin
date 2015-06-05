# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmListBox.ui'
#
# Created: Tue Oct 28 22:51:26 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,252,206).size()).expandedTo(Dialog.minimumSizeHint()))

        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(9,9,234,16))
        self.label.setObjectName("label")

        self.regionComboBox = QtGui.QComboBox(Dialog)
        self.regionComboBox.setGeometry(QtCore.QRect(9,30,234,22))
        self.regionComboBox.setObjectName("regionComboBox")

        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(9,59,234,16))
        self.label_2.setObjectName("label_2")

        self.boundaryTagComboBox = QtGui.QComboBox(Dialog)
        self.boundaryTagComboBox.setGeometry(QtCore.QRect(9,80,234,22))
        self.boundaryTagComboBox.setObjectName("boundaryTagComboBox")

        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(9,109,192,22))
        self.label_3.setObjectName("label_3")

        self.minTriAngleLineEdit = QtGui.QLineEdit(Dialog)
        self.minTriAngleLineEdit.setGeometry(QtCore.QRect(206,109,37,22))
        self.minTriAngleLineEdit.setObjectName("minTriAngleLineEdit")

        self.generateButton = QtGui.QPushButton(Dialog)
        self.generateButton.setGeometry(QtCore.QRect(9,170,91,26))
        self.generateButton.setObjectName("generateButton")

        self.closeButton = QtGui.QPushButton(Dialog)
        self.closeButton.setGeometry(QtCore.QRect(110,170,133,26))
        self.closeButton.setObjectName("closeButton")

        self.force24CheckBox = QtGui.QCheckBox(Dialog)
        self.force24CheckBox.setGeometry(QtCore.QRect(10,140,171,21))
        self.force24CheckBox.setObjectName("force24CheckBox")

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
        self.force24CheckBox.setText(QtGui.QApplication.translate("Dialog", "Force python 2.4", None, QtGui.QApplication.UnicodeUTF8))

