import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from funcionesPie import InicioTalon,norma,generacionLinea,medicionPerimetro,PolyAjuste

#defino variables a utilizar
lZmin=[]
lZmax=[]
lYmin=[]
lYmax=[]
xyz=["X","Y","Z"]
tamañoDato=8
tamañoLandmark=8
indice=0
#comienzo
escaneo='archivos/FootProfile2.xyz'
Landmarks='archivos/Landmark2.xyz'
df0=np.round(pd.read_table(escaneo,skiprows=2,delim_whitespace=(True),names=xyz),1)
dfLandmarks=np.round(pd.read_table(Landmarks,delim_whitespace=(True),names=xyz),1)
#indexDrop=[0,3,4,6,8,10,13,15] #landmarks que me parecieron NO útiles
#dfLandmarks=dfLandmarks.drop(indexDrop) #indices dropeados
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
#------------------------------------------------------------------------------
AlturaMaxTalon=df[df['Y']==miny]['Z'].min().round(1) 
xAlturaMaxTalon=df[(df['Z']==AlturaMaxTalon) & (df['Y']==miny)]['X'].mean()
arrayAlturaTalon=[xAlturaMaxTalon,0,AlturaMaxTalon]#<--------------------array alturaTalon
distanciaTobillo=np.abs(dfLandmarks.iloc[1]['X']-dfLandmarks.iloc[2]['X'])#<--------------------largo del ancho del tobillo
LargoPie=maxy-miny
AnchoPie=maxx-minx
arrayEntradaPie=dfLandmarks.iloc[11]#<--------------------array entradaPie
print(type(arrayEntradaPie))

# arrayCentroTobillo=dfLandmarks.iloc[12]
# distanciaEntrada_Talon=norma(arrayEntradaPie,arrayAlturaTalon)#<--------------------distancia entre la entrada del pie y el talón
# yInicioTalon,zInicioTalon=InicioTalon(df,lZmin,lYmin,AlturaMaxTalon,arrayCentroTobillo['Y'])
# arrayInicioTalon=[xAlturaMaxTalon,yInicioTalon,zInicioTalon]#<--------------------array arrayInicioTalon
# distanciaEntrada_IniciTalon=norma(arrayEntradaPie,arrayInicioTalon)#<--------------------distancia entre el empeine y el inicio del talón
# print(f'Distancia Entrada de pie - inicio talon: {distanciaEntrada_IniciTalon}mm')
# print(f'Ancho de tobillo: {distanciaTobillo}mm')
# print(f'Distancia Entrada de pie - talon: {distanciaEntrada_Talon}mm')
# print(f'Largo del pie: {LargoPie}mm')
# print(f'Ancho del pie: {AnchoPie}mm')
# ###############################################################
# #--------------------------------------------------------------
df['TIPO']='DATO'
df['TAMAÑO']=tamañoDato
# #--------------------------------------------------------------
# dfInicioTalon=pd.DataFrame([arrayInicioTalon],columns=xyz)
# dfInicioTalon['TIPO']='INICIO TALON'
# dfInicioTalon['TAMAÑO']=tamañoLandmark
# df=pd.concat([df,dfInicioTalon],ignore_index=True)
# #--------------------------------------------------------------
# dfEntradaPie=pd.DataFrame([arrayEntradaPie],columns=xyz)
# dfEntradaPie['TIPO']='ENTRADA PIE'
# dfEntradaPie['TAMAÑO']=tamañoLandmark
# df=pd.concat([df,dfEntradaPie],ignore_index=True)
# #--------------------------------------------------------------
# dfAlturaTalon=pd.DataFrame([arrayAlturaTalon],columns=xyz)
# dfAlturaTalon['TIPO']='ALTURA TALON'
# dfAlturaTalon['TAMAÑO']=tamañoLandmark
# df=pd.concat([df,dfAlturaTalon],ignore_index=True)
# ###############################################################
# ordIni=arrayInicioTalon[1]
# absIni=arrayInicioTalon[2]
# ordFin=arrayEntradaPie[1]
# absFin=arrayEntradaPie[2]
# #selecciono las columnas xyz y especifico el avance, la imagen del avance y los puntos de inicio y fin
# intersecc=generacionLinea(df[xyz],'Y','Z',ordIni,ordFin,absIni,absFin)
# intersecc['TIPO']='INICIO TALON - ENTRADA'
# intersecc['TAMAÑO']=tamañoLandmark
# df=pd.concat([df,intersecc],ignore_index=True)

# ordIni=arrayAlturaTalon[1]
# absIni=arrayAlturaTalon[2]
# intersecc=generacionLinea(df[xyz],'Y','Z',ordIni,ordFin,absIni,absFin)
# intersecc['TIPO']='TALON - ENTRADA'
# intersecc['TAMAÑO']=tamañoLandmark
# df=pd.concat([df,intersecc],ignore_index=True)
# ordIni=arrayEntradaPie[1]
# absIni=0
# ordFin=ordIni
# absFin=arrayEntradaPie[2]
# #selecciono las columnas xyz y especifico el avance, la imagen del avance y los puntos de inicio y fin
# intersecc,dictlargos=generacionLinea(df[xyz],'Z','Y',ordIni,ordFin,absIni,absFin)
# df,dictlargos=medicionPerimetro(df,dictlargos,tamañoLandmark)
# #fig=px.scatter_3d(df,x='X',y='Y',z='Z',color='TIPO',size='TAMAÑO',size_max=13)

df=df.round(1)
dfLonja=PolyAjuste(df,arrayEntradaPie,paso=0.4,plano='ZX') 

'''
dfAJ=pd.DataFrame(listaAjuste,scolumns=xyz)
dfAJ['TIPO']='AJUSTADO'
dfAJ['TAMAÑO']=tamañoDato
df=pd.concat([df,dfAJ],ignore_index=True)

print(len(df1Sup))
zmaxdfFinal=dfFinal['Z'].max()
dfFinal1C=dfFinal[(dfFinal['X']>=arrayEntradaPie[0])]
dfFinal2C=dfFinal[(dfFinal['X']<arrayEntradaPie[0])]
xmaxdfFinal1C=dfFinal1C['X'].max()
xmindfFinal2C=dfFinal2C['X'].min()
print(xmindfFinal2C)
zMaxdfFinal1Csup=dfFinal1C[dfFinal1C['X']==xmaxdfFinal1C]['Z'].max()
zMaxdfFinal2Csup=dfFinal2C[dfFinal2C['X']==xmindfFinal2C]['Z'].max()
dfFinal1Csup=dfFinal1C[dfFinal1C['Z']>=zMaxdfFinal1Csup]
dfFinal2Csup=dfFinal2C[dfFinal2C['Z']>=zMaxdfFinal2Csup]
print(dfFinal2Csup)
#ajusto con un polinomio de grado 4 los datos de dfFinal1Csup
x1Cs=dfFinal1Csup['X']
Z1Cs=dfFinal1Csup['Z']
coeficientes1=np.polyfit(x1Cs,Z1Cs,5)
p1Cs=np.poly1d(coeficientes1)
#creo un vector X1 que vaya desde x.min() hasta x.max() con un paso de 0.1
X1CsAjustado=np.arange(x1Cs.min(),x1Cs.max(),0.1)
Z1CsAjustado=p1Cs(X1CsAjustado)

#creo un nuevo dfFinal1C con los valores de X1,Z1 y arrayEntradaPie[1]
dfFinal1CsupAjustado=pd.DataFrame(columns=xyz)
for i in range(len(X1CsAjustado)):
    vector=[X1CsAjustado[i],arrayEntradaPie[1],Z1CsAjustado[i]]
    dfFinal1CsupAjustado=dfFinal1CsupAjustado.append(pd.Series(vector,index=xyz),ignore_index=True)

dfFinal1CsupAjustado['TIPO']='AJUSTADO1C'
dfFinal1CsupAjustado['TAMAÑO']=tamañoDato

x2Cs=dfFinal2Csup['X']
print(x2Cs)
Z2Cs=dfFinal2Csup['Z']
coeficientes2=np.polyfit(x2Cs,Z2Cs,5)
p2Cs=np.poly1d(coeficientes2)
#creo un vector X1 que vaya desde x.min() hasta x.max() con un paso de 0.1
X2CsAjustado=np.arange(x1Cs.min(),x1Cs.max(),0.1)
Z2CsAjustado=p2Cs(X1CsAjustado)

#creo un nuevo dfFinal1C con los valores de X1,Z1 y arrayEntradaPie[1]
dfFinal2CsupAjustado=pd.DataFrame(columns=xyz)
for i in range(len(X2CsAjustado)):
    vector=[X2CsAjustado[i],arrayEntradaPie[1],Z2CsAjustado[i]]
    dfFinal2CsupAjustado=dfFinal2CsupAjustado.append(pd.Series(vector,index=xyz),ignore_index=True)

dfFinal2CsupAjustado['TIPO']='AJUSTADO2C'
dfFinal2CsupAjustado['TAMAÑO']=tamañoDato
#concateno dfFinal1CsupAjustado con dfFinal1Csup
dfFinal1Csup=pd.concat([dfFinal1Csup,dfFinal1CsupAjustado],ignore_index=True)
dfFinal2Csup=pd.concat([dfFinal2Csup,dfFinal2CsupAjustado],ignore_index=True)   

#dfPromedio=dfPromedio.append(dfFinala[(dfFinala['Y']>=i)&(dfFinala['Y']<i+10)].mean(),ignore_index=True)
#dfFinalb=dfFinal[dfFinal['X']>arrayEntradaPie[0]]
#df=pd.concat([df,dfPromedio],ignore_index=True)
dfjuntado=pd.concat([df1Sup,df1Inf],ignore_index=True)

fig=px.scatter_3d(df,x='X',y='Y',z='Z',color='TIPO',size='TAMAÑO',size_max=13)

# for key, dfcurva in dictlargos.items():
#     fig.add_trace(go.Scatter3d(x=dfcurva['X'], y=dfcurva['Y'], z=dfcurva['Z'], mode='lines', name=key,line=dict(color='red', width=4)))
# for i in range(2):
#     fig.add_trace(go.Scatter3d(x=dictlargos['PMaxm']['X'], y=dictlargos['PMaxm']['Y'], z=dictlargos['PMaxm']['Z'], mode='lines', name='PMaxm',line=dict(color='red', width=4)))
#     fig.add_trace(go.Scatter3d(x=dictlargos['PMaxM']['X'], y=dictlargos['PMaxM']['Y'], z=dictlargos['PMaxM']['Z'], mode='lines', name='PMaxM',line=dict(color='red', width=4)))
fig.update_layout(scene=dict(aspectratio=dict(x=1.1, y=3.1, z=1),))
fig.show()
#fig.write_html("plot.html")

fig.update_layout(scene=dict(aspectratio=dict(x=1.1, y=3.1, z=1),))
fig.show()'''




