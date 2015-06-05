# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmAuditMesh.ui'
#
# Created: Thu Apr 09 16:51:37 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(239, 109)
        self.closePushButton = QtGui.QPushButton(Dialog)
        self.closePushButton.setGeometry(QtCore.QRect(160, 80, 75, 24))
        self.closePushButton.setObjectName("closePushButton")
        self.auditPushButton = QtGui.QPushButton(Dialog)
        self.auditPushButton.setGeometry(QtCore.QRect(80, 80, 75, 24))
        self.auditPushButton.setObjectName("auditPushButton")
        self.changeInAjasentAreaLabel = QtGui.QLabel(Dialog)
        self.changeInAjasentAreaLabel.setGeometry(QtCore.QRect(10, 10, 161, 16))
        self.changeInAjasentAreaLabel.setObjectName("changeInAjasentAreaLabel")
        self.changeInAjasentAreaLineEdit = QtGui.QLineEdit(Dialog)
        self.changeInAjasentAreaLineEdit.setGeometry(QtCore.QRect(180, 10, 51, 20))
        self.changeInAjasentAreaLineEdit.setObjectName("changeInAjasentAreaLineEdit")
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(10, 40, 221, 23))
        self.progressBar.setProperty("value", QtCore.QVariant(0))
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.closePushButton, QtCore.SIGNAL("clicked()"), Dialog.close)
        QtCore.QObject.connect(self.auditPushButton, QtCore.SIGNAL("clicked()"), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Audit Mesh", None, QtGui.QApplication.UnicodeUTF8))
        self.closePushButton.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.auditPushButton.setText(QtGui.QApplication.translate("Dialog", "Audit", None, QtGui.QApplication.UnicodeUTF8))
        self.changeInAjasentAreaLabel.setText(QtGui.QApplication.translate("Dialog", "Change In Ajasent Element Area", None, QtGui.QApplication.UnicodeUTF8))
        self.changeInAjasentAreaLineEdit.setText(QtGui.QApplication.translate("Dialog", "0.5", None, QtGui.QApplication.UnicodeUTF8))

