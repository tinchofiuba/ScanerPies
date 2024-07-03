#importo lo que necesito desde ui_GUI.py para poder mostrar e interaccionar con la interfaz
from ui_GUI import *
import sys
import pandas as pd
import numpy as np

#muestro la interfaz grafica.

app = QApplication(sys.argv)
Dialog = QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()
sys.exit(app.exec_())





#muestro la interfaz ui_GUI.py
