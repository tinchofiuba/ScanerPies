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
        self.diccionarioErrores={}
        self.diccionariosDescripciones={}
        self.direccionDeGuardado = os.getcwd()
        self.cargarConfiguracionInicial()
        self.archivos = []
        self.listaArchivosConError=[]
        self.listaErrores=[]
        self.largoLandmarks=22 #ver bien cuantas dimensiones tiene
        self.ui.pushButton_5.setEnabled(False)
        self.descripcionErrores=""
        if self.ui.comboBox.currentText()!= 'Operador/a' and self.ui.lineEdit.text()!='':
            self.ui.pushButton.setEnabled(True)
        else:
            self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton_2.clicked.connect(lambda: self.cambiarDireccionCsv())
        self.ui.comboBox.currentIndexChanged.connect(lambda: self.chequeoBotones("combobox")) #si cambia el combobox
        self.ui.lineEdit.textChanged.connect(lambda: self.chequeoBotones("lineedit")) #si cambia el lineedit
        #en caso de que sucedan estas 2 coasa se habilitará el boton para predecir las medias del pie   
        self.ui.pushButton_4.clicked.connect(lambda: self.infoUsuario())
        #self.ui.pushButton_3.clicked.connect(lambda: self.comenzarAnalisis())
        self.ui.pushButton.clicked.connect(lambda: self.cargarArchivos()) 
        self.ui.pushButton_5.clicked.connect(lambda: self.limpiarDatos())

    def limpiarDatos(self):
        print("limpiando datos")
                                             
    def chequeoBotones(self, tipo):
        if tipo=="combobox":
            self.cambiarOperador()
            if self.ui.comboBox.currentText()!= 'Operador/a' and self.ui.lineEdit.text()!='':
                self.ui.pushButton_3.setEnabled(True)
            else:
                self.ui.pushButton_3.setEnabled(False)
        elif tipo=="lineedit":
            self.guardarLugar()
            if self.ui.comboBox.currentText()!= 'Operador/a' and self.ui.lineEdit.text()!='':
                self.ui.pushButton.setEnabled(True)
            else:
                self.ui.pushButton.setEnabled(False)

    def guardarLugar(self):
        with open('back.json') as f:
            data = json.load(f)
        if self.ui.lineEdit.text()!='':
            data['lugar']=self.ui.lineEdit.text()
            with open('back.json', 'w') as f:
                json.dump(data, f)

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
        msg = QMessageBox(self)
        msg.setWindowTitle("Información")
        msg.setText(notaInicial)
        msg.exec_()

    def muestraErrores(self,listaArchivosConError,listaErrores):
        texto=""    
        for i in range(len(listaArchivosConError)):
            lineaMensaje="Archivo con error: "+listaArchivosConError[i]+"\nError: "+listaErrores[i]+"\n"
            texto+=lineaMensaje if i==0 else lineaMensaje
        return texto
    
    def chequeoDatos(self,listaDf,erroresTotales):
        for DF in listaDf:
            lineasErroneas=[]
            listaArchivosConError=[]
            nombreArchivo=os.path.basename(DF)
            df=pd.read_table(DF,skiprows=None,delim_whitespace=(True),names=["X","Y","Z"])
            df=df.apply(lambda x: pd.to_numeric(x, errors='coerce'))
            errores=0
            descripcionErrores=""
            if df.isnull().values.any():
                errores+=1
                erroresTotales+=1
                listaArchivosConError.append(nombreArchivo)
                descripcionErrores+="Hay datos tipo NaN/null"
                for i in range(len(df)):
                    if df.iloc[i].isnull().values.any():
                        lineasErroneas.append(i)
            if "landmark" in nombreArchivo:
                if len(df)!=self.largoLandmarks:
                        lineaDeError="ay una cantidad de Landmarks distinta a la esperada"
                        if errores==0:
                            listaArchivosConError.append(nombreArchivo)
                            errores+=1
                            erroresTotales+=1
                        descripcionErrores+=" y h"+lineaDeError if errores>0 else "H"+lineaDeError
            if errores>0:
                if "landmark" in nombreArchivo:
                    self.dictErrores['landmarks'].append(nombreArchivo)
                    if len(lineasErroneas)>0:
                        self.dictErrores['filasLandmark'].append(lineasErroneas)
                    self.dictDescripciones['landmarks'].append(descripcionErrores)
                else:
                    self.dictErrores['scaneo'].append(nombreArchivo)
                    if len(lineasErroneas)>0:
                        self.ictErrores['filasScaneo'].append(lineasErroneas)
                    self.dictDescripciones['scaneo'].append(descripcionErrores)
            else:
                print("No hay errores")
            return erroresTotales,self.dictErrores,self.dictDescripciones

    def cargarArchivos(self):
        erroresTotales=0
        self.dictErrores={'landmarks':[],'scaneo':[],'filasLandmark':[],'filasScaneo':[]} #creo un dict que almacena los archivos erroneos y las filas  
        self.dictDescripciones={'landmarks':[],'scaneo':[]}
        self.archivos, _ = QFileDialog.getOpenFileNames(self, "Seleccionar los archivos landmarks", "", "Archivos xyz (*.xyz);;Todos los archivos (*)")
        if len(self.archivos)>0:
            self.listaArchivosConError=[]
            self.listaErrores=[]
            for archivo in self.archivos:
                self.direccionXYZ=os.path.dirname(self.archivos[0])+'/'
                self.nombreArchivo=os.path.basename(archivo)
                if "landmark" in archivo:
                    self.archivoScaneo=self.nombreArchivo.replace("landmark","")
                    dirArchivoScaneo=self.direccionXYZ+self.archivoScaneo
                    if not os.path.exists(dirArchivoScaneo):
                        self.ui.label_2.setText("Hay archivos insuficientes, volver a cargar")
                        self.ui.label_2.setStyleSheet("color: red")
                        self.ui.pushButton_3.setEnabled(False)
                        self.listaArchivosConError.append(self.nombreArchivo)
                        self.listaErrores.append("No se encontró archivo de escaneo")
                    else:
                        erroresTotales,dictErr,dictDesc=self.chequeoDatos([archivo,dirArchivoScaneo],erroresTotales) 
                        if erroresTotales>0:
                            self.ui.label_2.setText("Hay un errores en los datos. Limpiar datos antes de procesar")
                            self.ui.pushButton_5.setEnabled(True)
                            self.ui.label_2.setStyleSheet("color: red")
                            self.ui.pushButton_3.setEnabled(False)
                            textoLandmarks=""
                            textoEscaneo=""
                            if len(dictErr['landmarks'])>0:
                                erroresLandmarks=zip(dictErr['landmarks'],dictDesc['landmarks'])
                                for errores in erroresLandmarks:
                                    textoLandmarks+=errores[0]+": "+errores[1]+"\n"
                            if len(dictErr['scaneo'])>0:
                                erroresScaneo=zip(dictErr['scaneo'],dictDesc['scaneo'])
                                for errores in erroresScaneo:
                                    textoEscaneo+=errores[0]+": "+errores[1]+"\n"
                            msg = QMessageBox(self)
                            msg.setWindowTitle("Hay errores de datos!")
                            msg.setText("Errores en landmarks:\n"+textoLandmarks+"\nErrores en escaneo:\n"+textoEscaneo)
                            msg.exec_()
                        else:
                            self.ui.label_2.setText("Archivos cargados correctamente y sin errores")
                            self.ui.label_2.setStyleSheet("color: green")
                            self.ui.pushButton_5.setEnabled(False)
                            self.ui.pushButton_3.setEnabled(True)
                else:
                    self.ui.label_2.setText("Hay archivos mal cargados, repetir la carga")
                    self.ui.label_2.setStyleSheet("color: red")
                    self.ui.pushButton_3.setEnabled(False)
                    self.listaArchivosConError.append(self.nombreArchivo)
                    self.listaErrores.append("No es un archivo landmark")
        else:
            self.ui.pushButton_3.setEnabled(False)
            self.ui.label_2.setText("No se cargaron archivos")
        if len(self.listaArchivosConError)>0:
            print(self.listaArchivosConError)
            texto=self.muestraErrores(self.listaArchivosConError,self.listaErrores)
            msg = QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setText(texto)
            msg.exec_()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec_())

