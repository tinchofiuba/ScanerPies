#importo lo que necesito desde ui_GUI.py para poder mostrar e interaccionar con la interfaz
from ui_GUI import *
import sys
import pandas as pd
import numpy as np
import os   
import json
from analisisPie import analisis

num_cores = os.cpu_count() #<-------------------número de núcleos de la CPU

def comenzarAnalisis(): #falta definir los parametros de entrada para poder leer el df y dflandmark
    df0=pd.read_csv('df0.csv')
    dfLandmarks=pd.read_csv('dflandmarks.csv')
    analisis(df0,dfLandmarks)

#si apreto el boton pushButton_2 quiero se abre una ventana para seleccionar la dirección de guardado
def cambiarDireccionCsv(GUI):
    global direccionDeGuardado
    direccionDeGuardado = QFileDialog.getExistingDirectory()
    GUI.label_3.setText(direccionDeGuardado)
#guardo la direccion de guardado en el archivo "back.json", modificando solamente "direccionCsv"
    with open('back.json') as f:
        data = json.load(f)
    data['direccionCsv']=direccionDeGuardado
    with open('back.json', 'w') as f:
        json.dump(data, f)

def cambiarOperador(GUI):
    with open('back.json') as f:
        data = json.load(f)
    data['operador']=GUI.comboBox.currentText()
    with open('back.json', 'w') as f:
        json.dump(data, f)    

def infoUsuario(GUI):
    #al apretar el boton y ejecutar esta función se muestra una ventana en pop-up con la información del programa
    msg = QMessageBox(Dialog)
    msg.setWindowTitle("Información")
    msg.setText('''Procedimiento del programa:\n
                1-Se debe seleccionar el operador\n
                2-Se debe rellenar con el lugar del escaneo\n
                -Una vez realizado 1 y 2 se podrán cargar los datos\n
                3-cargar los archivos con denominación "landmarkNombreNumero.xyz"
                -Cada archivo landmark.xyz tiene asociado un archivo .xyz con los datos del escaneo\n
                4-Presión el boton "Analizar y extraer medidas" para obtener las medidas\n
                -En caso de haber seleccionado mal algún archivo o que suceda otra problema\n
                -El programa mostrará un mensaje de error, detallando el incidente
                5-Para poder acceder a al información abrir el archivo .csv \n''')
    msg.exec_()
    print("assaas")

app = QApplication(sys.argv)
Dialog = QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()

#defino la variable direccionDeGuardado a la dirección actual del archivo (dirección  por Default)
direccionDeGuardado=os.getcwd()
#me fijo si en el .json "back.json" esta defininido "DireccionCsv", si es así muestra la dirección en la interfaz
#en el label_3
if os.path.exists('back.json'):
    with open('back.json') as f:
        data = json.load(f)
    if 'direccionCsv' in data:
        if data['direccionCsv']!="":
            ui.label_3.setText(data['direccionCsv'])
        else:
            ui.label_3.setText(direccionDeGuardado)
        if data['operador']!="":
            ui.comboBox.setCurrentText(data['operador'])
        if data['lugar']!="":
            ui.lineEdit.setText(data['lugar'])
#si apreto el pushbutton_2 se ejecuta la funcion "cambiarDireccionCsv"
ui.pushButton_2.clicked.connect(lambda: cambiarDireccionCsv(ui))
#si el combobox cambia su valor se ejecuta la funcion "cambiarOperador"
ui.comboBox.currentIndexChanged.connect(lambda: cambiarOperador(ui))
#si apreto el boton pushButton se ejecuta la funcion "infoUsuario"
ui.pushButton_4.clicked.connect(lambda: infoUsuario(ui))
#si apreto el boton "Analizar y extraer medidas" se ejecuta la función "analizar"
ui.pushButton.clicked.connect(lambda: comenzarAnalisis())
sys.exit(app.exec_())
