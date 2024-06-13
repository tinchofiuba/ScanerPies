import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from funcionesPie import InicioTalon,norma,generacionLinea,medicionPerimetro,medidaPerimetral

#defino variables a utilizar
lZmin=[]
lZmax=[]
lYmin=[]
lYmax=[]
xyz=["X","Y","Z"]
colMedicion=['Altura máxima del talón [mm]','Largo del pie [mm]','Ancho total del pie [mm]','Altura entrada del pie [mm]','Distancia entrada del pie - talón [mm]','Distancia entrada del pie - inicio talón [mm]']
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
print(dfMedicion['Altura máxima del talón [mm]'])
xAlturaMaxTalon=df[(df['Z']==AlturaMaxTalon) & (df['Y']==miny)]['X'].mean()
arrayAlturaTalon=[xAlturaMaxTalon,0,AlturaMaxTalon]#<--------------------array alturaTalon
distanciaTobillo=np.abs(dfLandmarks.iloc[1]['X']-dfLandmarks.iloc[2]['X'])#<--------------------largo del ancho del tobillo
LargoPie=maxy-miny
dfMedicion.at[0,'Largo del pie [mm]']=LargoPie
AnchoPie=maxx-minx
dfMedicion.at[0,'Ancho total del pie [mm]']=AnchoPie
arrayEntradaPie=dfLandmarks.iloc[11]#<--------------------array entradaPie
dfMedicion.at[0,'Altura entrada del pie [mm]']=arrayEntradaPie['Z']
arrayCentroTobillo=dfLandmarks.iloc[12]
distanciaEntrada_Talon=norma(arrayEntradaPie,arrayAlturaTalon)#<--------------------distancia entre la entrada del pie y el talón
dfMedicion.at[0,'Distancia entrada del pie - talón [mm]']=np.round(distanciaEntrada_Talon,1)
yInicioTalon,zInicioTalon=InicioTalon(df,lZmin,lYmin,AlturaMaxTalon,arrayCentroTobillo['Y'])
arrayInicioTalon=[xAlturaMaxTalon,yInicioTalon,zInicioTalon]#<--------------------array arrayInicioTalon
distanciaEntrada_IniciTalon=norma(arrayEntradaPie,arrayInicioTalon)#<--------------------distancia entre el empeine y el inicio del talón
dfMedicion.at[0,'Distancia entrada del pie - inicio talón [mm]']=np.round(distanciaEntrada_IniciTalon,1)
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
dfCircEntrPie=medidaPerimetral(df,arrayEntradaPie,paso=0.4,plano='ZX') #medicion en el plano Zx del perimetro
dfcircMetaTarso=medidaPerimetral(df,[dfInMetaTarso,dfFinMetaTarso],diagonal=True,paso=0.4,plano='ZX') #medicion en el plano Zx del perimetro



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




