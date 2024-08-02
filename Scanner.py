import sys
import os
import json
import pandas as pd
import time
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox, QLabel
from PyQt5.QtGui import QPixmap
from ui_GUI import *
import numpy as np
from analisisPie import extraccion
from configIniciales import notaInicial,PerimetrosAMedir,listaCsv
from multiprocessing import Process, freeze_support
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from funcionesPie import InicioTalon,norma,medidaPerimetral,Metatarso,tipoPie,alturaTalon,largoAnchoEntrada

class MiVentana(QDialog):
    def __init__(self, parent=None):
        super(MiVentana, self).__init__(parent)
        #hago que la ventana no pueda ser maximizada ni minimizada
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        #ni que se pueda agrandar o achicar con el mouse
        self.setFixedSize(400, 300)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Extracción de medidas - Scanner corporal") #titulo de la ventana
        self.setWindowIcon(QIcon('icono/3D.jpg')) #le cambio el icono a la ventana
        self.limpieza=0
        self.incluirLandmarks=0
        self.ploteo=0
        self.lugar=""
        self.operador=""
        self.guardarPlot=0
        self.dirCsv=""
        self.diccionarioErrores={}
        self.diccionariosDescripciones={}
        self.direccionDeGuardado = os.getcwd()
        self.archivosLandmarks = []
        self.listaArchivosConError=[]
        self.listaErrores=[]
        self.listaProcesos=[]
        self.cargarConfiguracionInicial()
        self.largoLandmarks=22 
        self.descripcionErrores=""
        if self.ui.comboBox.currentText()!= 'Operador/a' and self.ui.lineEdit.text()!='': #solo para la ocación.
            self.ui.pushButton.setEnabled(True)
        else:
            self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton_2.clicked.connect(lambda: self.cambiarDireccionCsv())
        self.ui.comboBox.currentIndexChanged.connect(lambda: self.chequeoBotones("combobox")) #si cambia el combobox
        self.ui.lineEdit.textChanged.connect(lambda: self.chequeoBotones("lineedit")) #si cambia el lineedit
        self.ui.pushButton_4.clicked.connect(lambda: self.infoUsuario())
        self.ui.pushButton.clicked.connect(lambda: self.cargarArchivos()) 
        self.ui.pushButton_3.clicked.connect(lambda: self.analisis())
        self.ui.checkBox.stateChanged.connect(lambda: self.chequeoBotones("checkbox"))
        self.ui.checkBox_2.stateChanged.connect(lambda: self.chequeoBotones("checkbox2"))
        self.ui.checkBox_3.stateChanged.connect(lambda: self.chequeoBotones("checkbox3"))                   
        #coloco la imagen con nombre "INTI.jpg" en wl Qlabel
        self.label_Imagen = QLabel(self)
        self.label_Imagen.setGeometry(10, 160, 130, 130)
        pixmap = QPixmap("icono/INTI.jpg")
        self.label_Imagen.setPixmap(pixmap)
        self.label_Imagen.setScaledContents(True)

    def limpiarDatos(self,df): #limpio los datos, saco valores duplicados y NaN
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)

    def analisis(self):
        numCores=os.cpu_count()
        self.operador=self.ui.comboBox.currentText()
        self.lugar=self.ui.lineEdit.text()
        #guardo un archivo de los landarks utilizados del tipo .json
        #en este archivo se pueden guardar los datos de los landmarks
        
        if len(self.archivosLandmarks)<=numCores:
            for i in range(len(self.archivosLandmarks)):
                p=Process(target=self.extraccion,args=(self.listaArchivosParaEscanear[i],self.archivosLandmarks[i]))
                print("processing!")
                p.start()   
                self.listaProcesos.append(p)
            for proceso in self.listaProcesos:
                proceso.join()
        else:
            numCiclos=len(self.archivosLandmarks)//numCores
            archivosResiduales=len(self.archivosLandmarks)%numCores
            #borro el archivo de landmarks.json para generar uno nuevo"
            if os.path.exists('landmarks.json'):
                os.remove('landmarks.json') 
            with open('landmarks.json', 'r') as file:
                data = json.load(file)
            for i in range(len(self.archivosLandmarks)):
                df=pd.read_table(self.archivosLandmarks,skiprows=None,delim_whitespace=(True),names=["X","Y","Z"])
                lDedos=[df.iloc[i] for i in [7,8,20,21,9]]
                dedos={"{i+1}":dedo for i,dedo in enumerate(lDedos)}
                empeine=df.iloc[6]
                entrada=
                alturaArco=df.iloc[5]  
                diccLandmarks={"landmark1":{"dedos":dedos, "empeine":empeine, "entrada":entrada, "alturaArco":alturaArco}}
                data.update
                with open('landmarks.json', 'W') as file:
                    data = json.load(file)
                

                    
            for ciclo in range(numCiclos):
                if ciclo==numCiclos-1:
                    lenArchivos=archivosResiduales
                else:
                    lenArchivos=numCores
                for i in range(lenArchivos):
                    p=Process(target=extraccion,args=(self.listaArchivosParaEscanear[i+ciclo*lenArchivos],self.archivosLandmarks[i+ciclo*lenArchivos],operador,lugar,1))
                    p.start()   
                    self.ListaProcesos.append(p)
                for proceso in self.ListaProcesos:
                    proceso.join()
                self.listaProcesos.clear()

    def chequeoBotones(self, tipo):
        if tipo=="combobox":
            self.cambiarOperador()
            if self.ui.comboBox.currentText()!= 'Operador/a' and self.ui.lineEdit.text()!='':
                self.ui.pushButton.setEnabled(True)
                if self.limpieza==1:
                    self.ui.pushButton_3.setEnabled(True)
                    self.ui.checkBox.setEnabled(True)
                    if self.ui.checkBox.isChecked():
                        self.ui.checkBox_2.setEnabled(True)
                        self.ui.checkBox_3.setEnabled(True)
                    else:
                        self.ui.checkBox_2.setEnabled(False)
                        self.ui.checkBox_3.setEnabled(False)
                else:
                    self.ui.pushButton_3.setEnabled(False)
                    self.ui.checkBox.setEnabled(False)
                    self.ui.checkBox_2.setEnabled(False)
                    self.ui.checkBox_3.setEnabled(False)
            else:
                self.ui.pushButton.setEnabled(False)
                self.ui.pushButton_3.setEnabled(False)
                self.ui.checkBox.setEnabled(False)
                self.ui.checkBox_2.setEnabled(False)
                self.ui.checkBox_3.setEnabled(False)
        elif tipo=="lineedit":
            self.guardarLugar()
            if self.ui.comboBox.currentText()!= 'Operador/a' and self.ui.lineEdit.text()!='':
                self.ui.pushButton.setEnabled(True)
            else:
                self.ui.pushButton.setEnabled(False)
        elif "checkbox" in tipo:
            if "2" in tipo:
                if self.ui.checkBox_2.isChecked():
                    self.guardarPlot=1
                else:
                    self.guardarPlot=0
            elif "3" in tipo:
                if self.ui.checkBox_3.isChecked():
                    self.incluirLandmarks=1
                else:
                    self.incluirLandmarks=0
            else:
                if self.ui.checkBox.isChecked():
                    self.ui.checkBox_2.setEnabled(True)
                    self.ui.checkBox_3.setEnabled(True)
                    self.ploteo=1
                    self.incluirLandmarks=0
                    self.guardarPlot=0
                else:
                    self.ui.checkBox_2.setEnabled(False)
                    self.ui.checkBox_3.setEnabled(False)
                    self.ploteo=0
                    self.incluirLandmarks=0
                    self.guardarPlot=0

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
                self.dirCsv = data['direccionCsv'] if data['direccionCsv'] else self.direccionDeGuardado
                self.ui.label_3.setText(self.dirCsv)
            if data.get('operador'):
                self.ui.comboBox.setCurrentText(data['operador'])
            if data.get('lugar'):
                self.ui.lineEdit.setText(data['lugar'])
            self.ui.checkBox.setEnabled(False)
            self.ui.checkBox_2.setEnabled(False)
            self.ui.checkBox_3.setEnabled(False)
            with open('back.json') as f:
                data = json.load(f)
                if "BotonPag1" in data:  # Verifica si 'BotonPag1' existe en el diccionario
                    if data["BotonPag1"]["tag"] == "":
                        self.ui.pushButton_5.setText(data["BotonPag1"]["tagDefault"])
                    else:
                        self.ui.pushButton_5.setText(data["BotonPag1"]["tag"])
                if "BotonPag2" in data:  # Verifica si 'BotonPag1' existe en el diccionario
                    if data["BotonPag2"]["tag"] == "":
                        self.ui.pushButton_6.setText(data["BotonPag2"]["tagDefault"])
                    else:
                        self.ui.pushButton_6.setText(data["BotonPag2"]["tag"])

    def cambiarDireccionCsv(self):
        self.dirCsv = QFileDialog.getExistingDirectory()
        if self.dirCsv=="":
            self.ui.label_3.setText(self.dirCsv)
        with open('back.json') as f:
            data = json.load(f)
        data['direccionCsv'] = self.dirCsv
        with open('back.json', 'w') as f:
            json.dump(data, f)

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
                if "landmark" in nombreArchivo:
                    errores+=1
                    erroresTotales+=1
                    listaArchivosConError.append(nombreArchivo)
                    descripcionErrores+="Hay datos tipo NaN/null"
                    for i in range(len(df)):
                        if df.iloc[i].isnull().values.any():
                            lineasErroneas.append(i)
                else:
                    print(len(df))
                    self.limpiarDatos(df)
                    print(len(df))
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
                        self.dictErrores['filasScaneo'].append(lineasErroneas)
                    self.dictDescripciones['scaneo'].append(descripcionErrores)
            else:
                print("No hay errores")
            print(erroresTotales,self.dictErrores,self.dictDescripciones)
        return erroresTotales,self.dictErrores,self.dictDescripciones

    def cargarArchivos(self):
        #abro la carpeta mediante la dirección que se encuentra en el back.json
        with open('back.json') as f:
            data = json.load(f)
        self.ultimaDireccionArchivos=data['direccionArchivos']
        erroresTotales=0
        self.dictErrores={'landmarks':[],'scaneo':[],'filasLandmark':[],'filasScaneo':[]} #creo un dict que almacena los archivos erroneos y las filas  
        self.dictDescripciones={'landmarks':[],'scaneo':[]}
        self.archivosLandmarks, _ = QFileDialog.getOpenFileNames(self, "Seleccionar los archivos landmarks",self.ultimaDireccionArchivos,"Archivos xyz (*.xyz);;Todos los archivos (*)")
        self.direccionArchivos=os.path.dirname(self.archivosLandmarks[0])
        if data['direccionArchivos']!=self.direccionArchivos:
            data['direccionArchivos']=self.direccionArchivos
            with open('back.json', 'w') as f:
                json.dump(data, f)
        self.listaArchivosParaEscanear=[]
        if len(self.archivosLandmarks)>0:
            self.listaArchivosConError=[]
            self.listaErrores=[]
            for archivo in self.archivosLandmarks:
                self.direccionXYZ=os.path.dirname(self.archivosLandmarks[0])+'/'
                self.nombreArchivo=os.path.basename(archivo)
                if "landmark" in archivo:
                    self.archivoScaneo=self.nombreArchivo.replace("landmark","")
                    dirArchivoScaneo=self.direccionXYZ+self.archivoScaneo
                    self.listaArchivosParaEscanear.append(dirArchivoScaneo)
                    if not os.path.exists(dirArchivoScaneo):
                        self.listaArchivosConError.append(self.nombreArchivo)
                        erroresTotales=-1
                        self.listaErrores.append("No se encontró archivo de escaneo")
                    else:
                        erroresTotales,dictErr,dictDesc=self.chequeoDatos([archivo,dirArchivoScaneo],erroresTotales) 
                        if erroresTotales>0:
                            self.ui.pushButton_3.setEnabled(False)
                            self.ui.checkBox.setEnabled(False)
                            self.ui.checkBox_2.setEnabled(False)
                            self.ui.checkBox_3.setEnabled(False)
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
                else:
                    self.ui.label_2.setText("Hay archivos mal cargados, repetir la carga")
                    self.ui.label_2.setStyleSheet("color: red")
                    self.ui.pushButton_3.setEnabled(False)
                    self.ui.checkBox.setEnabled(False)
                    self.ui.checkBox_2.setEnabled(False)
                    self.ui.checkBox_3.setEnabled(False)
                    self.listaArchivosConError.append(self.nombreArchivo)
                    self.listaErrores.append("No es un archivo landmark")
            if erroresTotales>0:
                msg = QMessageBox(self)
                msg.setWindowTitle("Hay errores de datos!")
                if len(textoLandmarks)==0:
                    if len(textoEscaneo)!=0:
                        self.ui.label_2.setText("Se corrigieron errores")
                        self.ui.label_2.setStyleSheet("color: green")
                elif len(textoEscaneo)==0:
                    self.ui.label_2.setText("Hay errores en landmarks")
                    self.ui.label_2.setStyleSheet("color: red")
                    msg.setText("Errores en landmarks:\n"+textoLandmarks)
                else:
                    msg.setText("Errores en landmarks:\n"+textoLandmarks+"\nErrores en escaneo:\n"+textoEscaneo)
                    self.ui.label_2.setText("Hay errores en ambos archivos")
                    self.ui.label_2.setStyleSheet("color: red")
                msg.exec_()
            elif erroresTotales==-1:
                self.ui.label_2.setText("Hay archivos insuficientes, volver a cargar")
                self.ui.label_2.setStyleSheet("color: red")
                self.ui.pushButton_3.setEnabled(False)
                self.ui.checkBox.setEnabled(False)
                self.ui.checkBox_2.setEnabled(False)
                self.ui.checkBox_3.setEnabled(False)

            else:
                self.ui.label_2.setText("Archivos cargados correctamente y sin errores")
                self.ui.label_2.setStyleSheet("color: green")
                self.ui.pushButton_3.setEnabled(True)
                self.ui.checkBox.setEnabled(True)
                if self.ui.checkBox.isChecked():
                    self.ui.checkBox_2.setEnabled(True)
                    self.ui.checkBox_3.setEnabled(True)
                else:
                    self.ui.checkBox_2.setEnabled(False)
                    self.ui.checkBox_3.setEnabled(False)

        else:
            self.ui.pushButton_3.setEnabled(False)
            self.ui.label_2.setText("No se cargaron archivos")
        if len(self.listaArchivosConError)>0:
            texto=self.muestraErrores(self.listaArchivosConError,self.listaErrores)
            msg = QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setText(texto)
            msg.exec_()

    def extraccion(self,df0,dfLandmarks):
        print("Empezando análisis")
        tamañoDato=8
        tamañoLandmark=8
        lZmin=[]
        lYmin=[]
        MedidasPerim=[] 
        xyz=["X","Y","Z"]
        tag=df0.split('/')[-1].split('.')[0]
        df0=np.round(pd.read_table(df0,skiprows=2,delim_whitespace=(True),names=xyz),1)
        dfLandmarks=np.round(pd.read_table(dfLandmarks,delim_whitespace=(True),names=xyz),1)

        dfMedicion=pd.DataFrame(columns=listaCsv)
        #guardo la fecha y hora de la medicion
        dfMedicion.at[0,'FECHA']=time.strftime("%d/%m/%Y %H:%M:%S")
        dfMedicion.at[0,'USUARIO']=self.operador
        dfMedicion.at[0,'LUGAR']=self.self
        df=df0.copy()
        for v in xyz: #me fijo si hay valores negativos, si es así llevo todos los valores a positivos
            minv=df[v].min()   
            if minv<0:
                df[v]=df[v]+np.abs(minv)  
                dfLandmarks[v]=dfLandmarks[v]+np.abs(minv)
            else:
                df[v]=df[v]-minv
                dfLandmarks[v]=dfLandmarks[v]-minv
        #------------------------------------------------------------------------------
        minx=df['X'].min()
        maxx=df['X'].max()
        miny=df['Y'].min()
        maxy=df['Y'].max()
        minz=df['Z'].min()
        maxz=df['Z'].max()
        #---------------------MEDICIONES----------------------------------------------
        #ENCUENTRO:
        #1-EL TIPO DE PIE
        #2-EL ALTO DE LA PUNTA DEL PIE
        #3-LA ALTURA A LA MITAD DEL PIE
        #4-EL TIPO DE PIE
        #5-SI EL PIE ES IZQ O DERECHO
        listaLandmarksDedos=[7,8,20,21,9]
        dfDedoscopia,dfMedicion,izqOder=tipoPie(df,listaLandmarksDedos,dfLandmarks,tamañoLandmark,dfMedicion) 
        #------------------------------------------------------------------------------
        #ENCUENTRO:
        #1-EL ANCHO METATARSIANO (el diagonal)
        #2-LA ALTURA MÁXIMA DEL METATARSO
        #3-LA ALTURA A LA MITAD DEL PIE
        #4-EL TIPO DE PIE
        #5-SI EL PIE ES IZQ O DERECHO
        iniMetaTarso,finMetaTarso,dfMedicion=Metatarso(df,maxx,maxy,izqOder,dfMedicion) #encuentro los puntos del metatarso, parte interna y externa
        dfInMetaTarso=pd.DataFrame([iniMetaTarso],columns=xyz)
        dfFinMetaTarso=pd.DataFrame([finMetaTarso],columns=xyz)
        #------------------------------------------------------------------------------
        #ENCUENTRO LA ALTURA DEL TALON Y EL VALOR DE "X" DE ESE PUNTO
        #ESTE VALOR DE "X" LO USO COMO SIMETRÍA EN EL EJE "Y"
        xAlturaMaxTalon,AlturaMaxTalon,dfMedicion=alturaTalon(df,miny,dfMedicion)
        arrayAlturaTalon=[xAlturaMaxTalon,0,AlturaMaxTalon]#<--------------------array alturaTalon
        dfAlturaTalon=pd.DataFrame([arrayAlturaTalon],columns=xyz)
        #------------------------------------------------------------------------------
        #ENCUENTRO:
        #1-EL LARGO DEL PIE
        #2-EL ANCHO TOTAL DEL PIE
        #3-LA ALTURA DE LA ENTRADA DEL PIE
        arrayEntradaPie,dfEntradaPie,dfMedicion=largoAnchoEntrada(df,dfLandmarks,maxy,miny,maxx,minx,xyz,dfMedicion)
        #------------------------------------------------------------------------------
        arrayCentroTobillo=dfLandmarks.iloc[12]
        distanciaEntrada_Talon=norma(arrayEntradaPie,arrayAlturaTalon)#<--------------------distancia entre la entrada del pie y el talón
        dfMedicion.at[0,'LARGO TALON-ENTRADA']=np.round(distanciaEntrada_Talon,1)
        arrayAlturaEmpeine=dfLandmarks.iloc[6]
        Zempieine=df[df['Y']==arrayAlturaEmpeine['Y']]['Z'].max()
        Xempeine=df[(df['Y']==arrayAlturaEmpeine['Y']) & (df['Z']==Zempieine)]['X'].mean()
        arrayAlturaEmpeine['Z']=Zempieine
        arrayAlturaEmpeine['X']=Xempeine

        dfEmpeine=pd.DataFrame([arrayAlturaEmpeine],columns=xyz)
        dfMedicion.at[0,'ALTURA EMPEINE']=np.round(Zempieine,1)
        arrayAlturaArco=dfLandmarks.iloc[5]['Z']
        dfMedicion.at[0,'ALTURA ARCO']=np.round(arrayAlturaArco,1)
        yInicioTalon,zInicioTalon=InicioTalon(df,lZmin,lYmin,AlturaMaxTalon,arrayCentroTobillo['Y'])
        arrayInicioTalon=[xAlturaMaxTalon,yInicioTalon,0]#<--------------------array arrayInicioTalon
        distanciaEmpeineTalon=norma(arrayAlturaEmpeine,arrayAlturaTalon)#<--------------------distancia entre el empeine y el talón
        dfMedicion.at[0,'LARGO TALON-EMPEINE']=np.round(distanciaEmpeineTalon,1)
        distanciaEmpeineInicioTalon=norma(arrayAlturaEmpeine,arrayInicioTalon)#<--------------------distancia entre el empeine y el inicio del talón
        dfMedicion.at[0,'LARGO INICIO TALON-EMPEINE']=np.round(distanciaEmpeineInicioTalon,1)
        distanciaEntrada_IniciTalon=norma(arrayEntradaPie,arrayInicioTalon)#<--------------------distancia entre el empeine y el inicio del talón
        dfMedicion.at[0,'LARGO INICIO TALON-ENTRADA']=np.round(distanciaEntrada_IniciTalon,1)

        df['TIPO']='DATO'
        df['TAMAÑO']=tamañoDato
        dfInicioTalon=pd.DataFrame([arrayInicioTalon],columns=xyz)
        dfInicioTalon['TIPO']='INICIO TALON'
        dfInicioTalon['TAMAÑO']=tamañoLandmark
        df=pd.concat([df,dfInicioTalon],ignore_index=True)
        #--------------------------------------------------------------
        dfEntradaPie=pd.DataFrame([arrayEntradaPie],columns=xyz)
        dfEntradaPie['TIPO']='ENTRADA PIE'
        dfEntradaPie['TAMAÑO']=tamañoLandmark
        df=pd.concat([df,dfEntradaPie],ignore_index=True)
        #--------------------------------------------------------------
        dfAlturaTalon=pd.DataFrame([arrayAlturaTalon],columns=xyz)
        dfAlturaTalon['TIPO']='ALTURA TALON'
        dfAlturaTalon['TAMAÑO']=tamañoLandmark
        df=pd.concat([df,dfAlturaTalon],ignore_index=True)

        df=df.round(1)
        dfLandmarks3=dfLandmarks.copy()
        for i in range(len(dfLandmarks3)):
            dfLandmarks3.at[i,'TIPO']=str(i)
            dfLandmarks3.at[i,'TAMAÑO']=tamañoLandmark
        dfLandmarks['TIPO']='LANDMARK'
        dfLandmarks['TAMAÑO']=tamañoLandmark
        dfLandmarks2=pd.DataFrame([dfLandmarks.iloc[7]],columns=xyz)
        dfLandmarks2['TIPO']='LANDMARK'
        dfLandmarks2['TAMAÑO']=tamañoLandmark

        dfCircEntrada,MedidasPerim=medidaPerimetral(df,MedidasPerim,arrayEntradaPie,'PERIMETRO ENTRADA PIE',paso=0.6,plano='ZX') #medicion en el plano Zx del perimetro
        dfCircEmpeine,MedidasPerim=medidaPerimetral(df,MedidasPerim,arrayAlturaEmpeine,'PERIMETRO EMPEINE',paso=0.6,plano='ZX') #medicion en el plano Zx del perimetro
        dfcircMetaTarso,MedidasPerim=medidaPerimetral(df,MedidasPerim,[dfInMetaTarso,dfFinMetaTarso],'PERIMETRO METATARSO',diagonal=True,paso=0.4,plano='ZX') #medicion en el plano Zx del perimetro
        dfCircTalonEntrada,MedidasPerim=medidaPerimetral(df,MedidasPerim,[dfAlturaTalon,dfEntradaPie],'PERIMETRO TALON - ENTRADA PIE',paso=0.2,inclinado='YX') #medicion en el plano Zx del perimetro
        dfCircInTalonEntrada,MedidasPerim=medidaPerimetral(df,MedidasPerim,[dfInicioTalon,dfEntradaPie],'PERIMETRO INICIO TALON - ENTRADA PIE',paso=0.2,inclinado='YX') #medicion en el plano Zx del perimetro
        dfCircTalonEmpeine,MedidasPerim=medidaPerimetral(df,MedidasPerim,[dfAlturaTalon,dfEmpeine],'PERIMETRO TALON - EMPEINE',paso=0.1,inclinado='YX') #medicion en el plano Zx del perimetro
        dfCircInTalonEmpeine,MedidasPerim=medidaPerimetral(df,MedidasPerim,[dfInicioTalon,dfEmpeine],'PERIMETRO INICIO TALON - EMPEINE',paso=0.2,inclinado='YX') #medicion en el plano Zx del perimetro

        for i in range(len(MedidasPerim)):
            dfMedicion.at[0,PerimetrosAMedir[i]]=MedidasPerim[i]
        try: #si el .csv existe lo abro y le agrego la medicion, sino lo creo
            dfViejo=pd.read_csv('Mediciones.csv')
            print(tag)
            if tag in dfViejo['TAG'].values:
                valores=dfViejo['TAG'].values
                tags=np.unique([tagDuplicado for tagDuplicado in valores if tag in tagDuplicado])
                lenTags=[len(tag) for tag in tags]
                if len(tags)>1:
                    tagMasLargo=tags[np.argmax(lenTags)]
                    tag=tagMasLargo+".duplicado"
                else:
                    tag=tag+".duplicado"
            dfMedicion.at[0,'TAG']=tag
            dfMedicion=pd.concat([dfViejo,dfMedicion],ignore_index=True)
            dfMedicion.to_csv(self.dirCsv+'/Mediciones.csv',index=False)
        except:
            dfMedicion.at[0,'TAG']=tag
            dfMedicion.to_csv(self.dirCsv+'/Mediciones.csv',index=False)
        if self.mostrarPlot==1:
            if self.incluirLandmarks==1:
                dfFinal=pd.concat([df,dfLandmarks3,dfDedoscopia,dfCircEntrada,dfCircEmpeine,dfcircMetaTarso,dfCircTalonEntrada,dfCircInTalonEntrada,dfCircTalonEmpeine,dfCircInTalonEmpeine],ignore_index=True)
            else:
                dfFinal=pd.concat([df,dfDedoscopia,dfCircEntrada,dfCircEmpeine,dfcircMetaTarso,dfCircTalonEntrada,dfCircInTalonEntrada,dfCircTalonEmpeine,dfCircInTalonEmpeine],ignore_index=True)
            fig=px.scatter_3d(dfFinal,x='X',y='Y',z='Z',color='TIPO',size='TAMAÑO',size_max=13)
            fig.update_layout(scene=dict(aspectratio=dict(x=1.1, y=3.1, z=1),))
            fig.show()
            
        if self.guardarPlot==1:
            #grafico el dfFinal con otro graficador que no sea plotly
            if self.incluirLandmarks==1:
                dfFinal=pd.concat([df,dfLandmarks3,dfDedoscopia,dfCircEntrada,dfCircEmpeine,dfcircMetaTarso,dfCircTalonEntrada,dfCircInTalonEntrada,dfCircTalonEmpeine,dfCircInTalonEmpeine],ignore_index=True)
            else:
                dfFinal=pd.concat([df,dfDedoscopia,dfCircEntrada,dfCircEmpeine,dfcircMetaTarso,dfCircTalonEntrada,dfCircInTalonEntrada,dfCircTalonEmpeine,dfCircInTalonEmpeine],ignore_index=True)
            fig = go.Figure(data=[go.Scatter3d(x=dfFinal['X'], y=dfFinal['Y'], z=dfFinal['Z'],mode='markers',marker=dict(size=3,color='blue'))])
            fig.write_html("grafico.html")

def main():
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    freeze_support()  
    main()