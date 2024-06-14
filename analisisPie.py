import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from funcionesPie import InicioTalon,norma,medidaPerimetral

#defino variables a utilizar
lZmin=[]
lZmax=[]
lYmin=[]
lYmax=[]
xyz=["X","Y","Z"]
colMedicion=['Altura máxima del talón [mm]','Largo del pie [mm]','Ancho total del pie [mm]','Altura entrada del pie [mm]','Distancia entrada del pie - talón [mm]','Distancia entrada del pie - inicio talón [mm]','Altura de arco [mm]','Altura empeine [mm]','Perímetro metarso [mm]','Perímetro entrada pie [mm]','Perímetro empeine [mm]','Tipo de pie']
dfMedicion=pd.DataFrame(columns=colMedicion)
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
maxyMetatarzoIn=df[df['X']==minx]['Y'].max()
maxzMetatarzoIn=df[(df['X']==minx) & (df['Y']==maxyMetatarzoIn)]['Z'].max()
iniMetaTarso=[minx,maxyMetatarzoIn,maxzMetatarzoIn]#<--------------------vector inicio del metatarzo, izquierda
maxyMetatarsoFin=df[df['X']==maxx]['Y'].max()
maxzMetatarsoFin=df[(df['X']==maxx) & (df['Y']==maxyMetatarsoFin)]['Z'].max()
finMetaTarso=[maxx,maxyMetatarsoFin,maxzMetatarsoFin]#<--------------------vector fin del metatarzo, derecha
dfInMetaTarso=pd.DataFrame([iniMetaTarso],columns=xyz)
dfFinMetaTarso=pd.DataFrame([finMetaTarso],columns=xyz)
#------------------------------------------------------------------------------
AlturaMaxTalon=df[df['Y']==miny]['Z'].min().round(1)
dfMedicion.at[0,'Altura máxima del talón [mm]']=AlturaMaxTalon
xAlturaMaxTalon=df[(df['Z']==AlturaMaxTalon) & (df['Y']==miny)]['X'].mean()
arrayAlturaTalon=[xAlturaMaxTalon,0,AlturaMaxTalon]#<--------------------array alturaTalon
dfAlturaTalon=pd.DataFrame([arrayAlturaTalon],columns=xyz)
distanciaTobillo=np.abs(dfLandmarks.iloc[1]['X']-dfLandmarks.iloc[2]['X'])#<--------------------largo del ancho del tobillo
LargoPie=maxy-miny
dfMedicion.at[0,'Largo del pie [mm]']=LargoPie
AnchoPie=maxx-minx
dfMedicion.at[0,'Ancho total del pie [mm]']=AnchoPie
arrayEntradaPie=dfLandmarks.iloc[11]#<--------------------array entradaPie
dfEntradaPie=pd.DataFrame([arrayEntradaPie],columns=xyz)
dfMedicion.at[0,'Altura entrada del pie [mm]']=arrayEntradaPie['Z']
arrayCentroTobillo=dfLandmarks.iloc[12]
distanciaEntrada_Talon=norma(arrayEntradaPie,arrayAlturaTalon)#<--------------------distancia entre la entrada del pie y el talón
dfMedicion.at[0,'Distancia entrada del pie - talón [mm]']=np.round(distanciaEntrada_Talon,1)
arrayAlturaEmpeine=dfLandmarks.iloc[6]
dfEmpeine=pd.DataFrame([arrayAlturaEmpeine],columns=xyz)
yEmpieine=arrayAlturaEmpeine['Y']
dfEmpeine['Z']=df[df['Y']==yEmpieine]['Z'].max()
dfMedicion.at[0,'Altura empeine [mm]']=np.round(arrayAlturaEmpeine,1)
arrayAlturaArco=dfLandmarks.iloc[5]
dfMedicion.at[0,'Altura de arco [mm]']=np.round(arrayAlturaArco,1)
yInicioTalon,zInicioTalon=InicioTalon(df,lZmin,lYmin,AlturaMaxTalon,arrayCentroTobillo['Y'])
arrayInicioTalon=[xAlturaMaxTalon,yInicioTalon,0]#<--------------------array arrayInicioTalon
distanciaEntrada_IniciTalon=norma(arrayEntradaPie,arrayInicioTalon)#<--------------------distancia entre el empeine y el inicio del talón
dfMedicion.at[0,'Distancia entrada del pie - inicio talón [mm]']=np.round(distanciaEntrada_IniciTalon,1)
listaDedos=[]
listaLandmarksDedos=[7,8,20,21,9]
for dedo in listaLandmarksDedos:
    listaDedos.append(dfLandmarks.iloc[dedo]['Y'].round(1))
dfDedos=dfLandmarks.iloc[listaLandmarksDedos]
dfDedos['Z']=0
dfDedos['TIPO']='DEDOS'
dfDedos['TAMAÑO']=tamañoLandmark
dfDedos['Y'].round(1)
if listaDedos[0]>listaDedos[1]:
    tipoDedo='Egipcio'
elif listaDedos[0]<listaDedos[1] and listaDedos[1]>listaDedos[2]:
    tipoDedo='Griego'
elif listaDedos[0]<listaDedos[1] and listaDedos[1]<listaDedos[2]:
    tipoDedo='Cuadrado'
dfMedicion.at[0,'Tipo de pie']=tipoDedo
dfMedicion.to_csv('Mediciones.csv',index=False)

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
#defino un dfLandmarks3 que sea dfLandmarks pero que según el index tenga un ['TIPO']= igual al numero de index
dfLandmarks3=dfLandmarks.copy()
for i in range(len(dfLandmarks3)):
    dfLandmarks3.at[i,'TIPO']=str(i)
    dfLandmarks3.at[i,'TAMAÑO']=tamañoLandmark
dfLandmarks['TIPO']='LANDMARK'
dfLandmarks['TAMAÑO']=tamañoLandmark
dfLandmarks2=pd.DataFrame([dfLandmarks.iloc[7]],columns=xyz)
dfLandmarks2['TIPO']='LANDMARK'
dfLandmarks2['TAMAÑO']=tamañoLandmark
dfCircEntrada=medidaPerimetral(df,arrayEntradaPie,'PERIMETRO ENTRADA PIE',paso=0.4,plano='ZX') #medicion en el plano Zx del perimetro
dfCircEmpeine=medidaPerimetral(df,arrayAlturaEmpeine,'PERIMETRO EMPEINE',paso=0.5,plano='ZX') #medicion en el plano Zx del perimetro
dfcircMetaTarso=medidaPerimetral(df,[dfInMetaTarso,dfFinMetaTarso],'PERIMETRO METATARSO',diagonal=True,paso=0.3,plano='ZX') #medicion en el plano Zx del perimetro
dfCircTalonEntrada=medidaPerimetral(df,[dfAlturaTalon,dfEntradaPie],'PERIMETRO TALON - ENTRADA PIE',diagonal=True,paso=0.1,inclinado='YX') #medicion en el plano Zx del perimetro
dfCircInTalonEntrada=medidaPerimetral(df,[dfInicioTalon,dfEntradaPie],'PERIMETRO INICIO TALON - ENTRADA PIE',diagonal=True,paso=0.1,inclinado='YX') #medicion en el plano Zx del perimetro
dfCircTalonEmpeine=medidaPerimetral(df,[dfAlturaTalon,dfEmpeine],'PERIMETRO TALON - EMPEINE',diagonal=True,paso=0.1,inclinado='YX') #medicion en el plano Zx del perimetro
dfCircInTalonEmpeine=medidaPerimetral(df,[dfInicioTalon,dfEmpeine],'PERIMETRO INICIO TALON - EMPEINE',diagonal=True,paso=0.2,inclinado='YX') #medicion en el plano Zx del perimetro
df=pd.concat([df,dfCircEntrada,dfCircEmpeine,dfcircMetaTarso,dfCircTalonEntrada,dfCircInTalonEntrada,dfCircTalonEmpeine,dfCircInTalonEmpeine],ignore_index=True)
fig=px.scatter_3d(df,x='X',y='Y',z='Z',color='TIPO',size='TAMAÑO',size_max=13)
fig.add_trace(go.Scatter3d(x=dfDedos['X'], y=dfDedos['Y'], z=dfDedos['Z'], mode='lines', name='Tipo de pie',line=dict(color='red', width=4)))
fig.update_layout(scene=dict(aspectratio=dict(x=1.1, y=3.1, z=1),))
fig.show()

'''
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




