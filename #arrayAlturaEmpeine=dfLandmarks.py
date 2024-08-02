#arrayAlturaEmpeine=dfLandmarks.iloc[6]
#arrayAlturaArco=dfLandmarks.iloc[5]['Z']
#[7,8,20,21,9]
# Lista de valores
valores = [7, 8, 20, 21, 9]

# Generar el diccionario
data = {"dedos": {str(i+1): valor for i, valor in enumerate(valores)}}

# Mostrar el diccionario resultante
print(data)