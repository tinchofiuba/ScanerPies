import sys
import os
import json
import pandas as pd
from PySide2.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox
from ui_GUI import *
import numpy as np
from analisisPie import analisis
from procedimiento import notaInicial

class MiVentana(QDialog):
    def __init__(self, parent=None):
        super(MiVentana, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.direccionDeGuardado = os.getcwd()
        self.cargarConfiguracionInicial()
        self.archivos = []
        # Conectar señales a métodos
        self.ui.pushButton_2.clicked.connect(lambda: self.cambiarDireccionCsv())
        self.ui.comboBox.currentIndexChanged.connect(lambda: self.cambiarOperador())
        self.ui.pushButton_4.clicked.connect(lambda: self.infoUsuario())
        #self.ui.pushButton_3.clicked.connect(lambda: self.comenzarAnalisis())
        self.ui.pushButton.clicked.connect(lambda: self.cargarArchivos())

    def cargarConfiguracionInicial(self):
        if os.path.exists('back.json'):
            with open('back.json') as f:
                data = json.load(f)
            if 'direccionCsv' in data:
                direccionCsv = data['direccionCsv'] if data['direccionCsv'] else self.direccionDeGuardado
                self.ui.label_3.setText(direccionCsv)
            if data.get('operador'):
                self.ui.comboBox.setCurrentText(data['operador'])
            if data.get('lugar'):
                self.ui.lineEdit.setText(data['lugar'])

    #si apreto el boton pushButton_2 quiero se abre una ventana para seleccionar la dirección de guardado
    def cambiarDireccionCsv(self):
        global direccionDeGuardado
        direccionDeGuardado = QFileDialog.getExistingDirectory()
        self.ui.label_3.setText(direccionDeGuardado)

    def cambiarOperador(self):
        with open('back.json') as f:
            data = json.load(f)
        data['operador']=self.ui.comboBox.currentText()
        with open('back.json', 'w') as f:
            json.dump(data, f) 

    def infoUsuario(self):
    #al apretar el boton y ejecutar esta función se muestra una ventana en pop-up con la información del programa
        msg = QMessageBox(self)
        msg.setWindowTitle("Información")
        msg.setText(notaInicial)
        msg.exec_()

    def cargarArchivos(self):
        #los archivos seleciionados se guardan en una lista.
        archivos, _ = QFileDialog.getOpenFileNames(self, "Seleccionar los archivos landmarks", "", "Archivos xyz (*.xyz);;Todos los archivos (*)")
        #me quedo con la dirección del archivo, pero sin su nombre. Por ejemplo, escritorio/landmark.xyz -> escritorio/ 
        self.direccionXYZ=os.path.dirname(archivos[0])+'/'
        for archivo in archivos:
            if "landmark" in archivo:
                self.archivoScaneo=archivo.replace("landmark","")
                self.archivoScaneo=self.direccionXYZ+self.archivoScaneo
                print(self.archivoScaneo)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec_())

