# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GUIpbsFtO.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.comboBox = QComboBox(Dialog)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(10, 20, 101, 21))
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(170, 20, 141, 20))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(130, 20, 41, 21))
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(10, 60, 101, 23))
        self.pushButton_2 = QPushButton(Dialog)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(10, 100, 61, 21))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(130, 60, 261, 21))
        self.pushButton_3 = QPushButton(Dialog)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(10, 140, 151, 31))
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(80, 100, 311, 21))
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 180, 371, 21))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Dialog", u"Operador/a", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Dialog", u"PT", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Dialog", u"JA", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Dialog", u"VR", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Dialog", u"VL", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("Dialog", u"CL", None))

        self.label.setText(QCoreApplication.translate("Dialog", u"LUGAR", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Cargar archivos", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"Ruta .csv", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"No se observan errores", None))
        self.pushButton_3.setText(QCoreApplication.translate("Dialog", u"Analizar y extraer medidas", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"default: Escritorio", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Errores: 0", None))
    # retranslateUi

