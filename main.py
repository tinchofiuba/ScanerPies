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
        self.listaArchivosConError=[]
        self.listaErrores=[]
        self.largoLandmarks=22 #ver bien cuantas dimensiones tiene
        self.ui.pushButton_5.setEnabled(False)
        self.descripcionErrores=""
        self.dictErrores={'landmarks':[],'scaneo':[],'filasLandmark':[],'filasScaneo':[],'nombreLandmark':[],'nombreScaneo':[]} #creo un dict que almacena los archivos erroneos y las filas  
        self.dictDescripciones={'landmarks':[],'scaneo':[]}
        # Conectar señales a métodos
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
    
    def chequeoDatos(self,landmarks,scaneo):
        dataframes=[landmarks,scaneo]
        nombreArchivoLandmark=os.path.basename(landmarks)
        nombreArchivoEscaneo=nombreArchivoLandmark.replace("landmark","")
        for DF in dataframes:
            lineasErroneas=[]
            listaArchivosConError=[]
            nombreArchivo=os.path.basename(DF)
            df=pd.read_table(DF,skiprows=None,delim_whitespace=(True),names=["X","Y","Z"])
            df=df.apply(lambda x: pd.to_numeric(x, errors='coerce'))
            errores=0
            descripcionErrores=""
            if df.isnull().values.any():
                errores=1
                print("Hay datos del tipo null")
                listaArchivosConError.append(nombreArchivo)
                descripcionErrores+="Hay datos tipo null"
                for i in range(len(df)):
                    if df.iloc[i].isnull().values.any():
                        lineasErroneas.append(i)
            if not df.apply(lambda x: x.apply(np.isreal)).all().all():
                print("hay tipos de datos NO numéricos")
                #apendizo en la linea "lineasErroneas" el numero de linea si hay algún dato que no es numérico
                print(df)
                for i in range(len(df)):
                    if not df.iloc[i].apply(np.isreal).all():
                        lineasErroneas.append(i)
                lineaDeError="ay datos que no son numéricos"
                if errores==0:
                    listaArchivosConError.append(nombreArchivo)
                    descripcionErrores="H"+lineaDeError
                    errores+=1
                else:
                    descripcionErrores+=" y h"+lineaDeError
                    errores+=1

            if "landmark" in nombreArchivo:
                if len(df)!=self.largoLandmarks:
                        lineaDeError="ay una cantidad de Landmarks distinta a la esperada"
                        print("error en la cantidad de landmarks")
                        if errores==0:
                            listaArchivosConError.append(nombreArchivo)
                            errores+=1
                        descripcionErrores+=" y h"+lineaDeError if errores>0 else "H"+lineaDeError
            if errores>0:
                self.ui.pushButton_3.setEnabled(True)
                print(descripcionErrores)
                if "landmark" in nombreArchivo:
                    self.dictErrores['landmarks'].append(nombreArchivo)
                    if len(lineasErroneas)>0:
                        self.dictErrores['filasLandmark'].append(lineasErroneas)
                    self.dictDescripciones['landmarks']=descripcionErrores 
                else:
                    self.dictErrores['scaneo'].append(errores)
                    if len(lineasErroneas)>0:
                        self.ictErrores['filasScaneo'].append(lineasErroneas)
                    self.dictDescripciones['scaneo']=descripcionErrores
            else:
                self.ui.pushButton_3.setEnabled(False)
                print("No hay errores")
            return self.dictErrores,self.dictDescripciones

    def cargarArchivos(self):
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
                    print(dirArchivoScaneo)
                    if not os.path.exists(dirArchivoScaneo):
                        self.ui.label_2.setText("Hay archivos insuficientes, volver a cargar")
                        self.ui.label_2.setStyleSheet("color: red")
                        self.ui.pushButton_3.setEnabled(False)
                        self.listaArchivosConError.append(self.nombreArchivo)
                        self.listaErrores.append("No se encontró archivo de escaneo")
                    else:
                        dictErr,dictDesc=self.chequeoDatos(archivo,dirArchivoScaneo)
                        print(dictErr,dictDesc)
                        self.ui.label_2.setText("Archivos cargados correctmente")
                        self.ui.label_2.setStyleSheet("color: green")
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

