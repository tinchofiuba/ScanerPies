import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from funcionesPie import InicioTalon,norma,medidaPerimetral,Metatarso

#defino variables a utilizar
lZmin=[]
lZmax=[]
lYmin=[]
lYmax=[]
listaDedos=[]
MedidasPerim=[] 
xyz=["X","Y","Z"]
datosPersonales=['TAG','USUARIO','FECHA','LUGAR','OBSERVACIONES']
PerimetrosAMedir=['PERIM ENTRADA','PERIM EMPEINE','PERIM METATARSO','PERIM TALON-ENTRADA','PERIM INICIO TALON-ENTRADA','PERIM TALON-EMPEINE','PERIM INICIO TALON-EMPEINE']
MedidasAbsolutas=['LARGO','ANCHO TOTAL','ALTURA ENTRADA','ALTURA EMPEINE','ALTURA TALON','ALTURA ARCO']
MedidasCalculadas=['LARGO TALON-ENTRADA','LARGO TALON-EMPEINE','LARGO INICIO TALON-ENTRADA','LARGO INICIO TALON-EMPEINE','ANCHO METATARSICO','TIPO DE PIE']
listaCsv=datosPersonales+PerimetrosAMedir+MedidasAbsolutas+MedidasCalculadas

dfMedicion=pd.DataFrame(columns=listaCsv)
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
iniMetaTarso,finMetaTarso,anchoMetatarsiano=Metatarso(df,minx,maxx)
dfMedicion.at[0,'ANCHO METATARSICO']=np.round(anchoMetatarsiano,1)
dfInMetaTarso=pd.DataFrame([iniMetaTarso],columns=xyz)
dfFinMetaTarso=pd.DataFrame([finMetaTarso],columns=xyz)
#------------------------------------------------------------------------------
AlturaMaxTalon=df[df['Y']==miny]['Z'].min().round(1)
dfMedicion.at[0,'ALTURA TALON']=AlturaMaxTalon
xAlturaMaxTalon=df[(df['Z']==AlturaMaxTalon) & (df['Y']==miny)]['X'].mean()
arrayAlturaTalon=[xAlturaMaxTalon,0,AlturaMaxTalon]#<--------------------array alturaTalon
dfAlturaTalon=pd.DataFrame([arrayAlturaTalon],columns=xyz)
#------------------------------------------------------------------------------
#distanciaTobillo=np.abs(dfLandmarks.iloc[1]['X']-dfLandmarks.iloc[2]['X'])#<--------------------largo del ancho del tobillo
LargoPie=maxy-miny
dfMedicion.at[0,'LARGO']=LargoPie
AnchoPie=maxx-minx
dfMedicion.at[0,'ANCHO TOTAL']=AnchoPie
arrayEntradaPie=dfLandmarks.iloc[11]#<--------------------array entradaPie
Zentrada=df[df['Y']==arrayEntradaPie['Y']]['Z'].max()
Xentrada=df[(df['Y']==arrayEntradaPie['Y']) & (df['Z']==Zentrada)]['X'].mean()
#reasigno los valores de X y Z para un valor máximo de Z (en ocasiones el landmark está corrido en el sentido X)
arrayEntradaPie['X']=Xentrada
arrayEntradaPie['Z']=Zentrada
dfEntradaPie=pd.DataFrame([arrayEntradaPie],columns=xyz)
dfMedicion.at[0,'ALTURA ENTRADA']=arrayEntradaPie['Z']
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
listaLandmarksDedos=[7,8,20,21,9]
listaDedos=[dfLandmarks.iloc[dedo]['Y'].round(1) for dedo in listaLandmarksDedos]
dfDedos=dfLandmarks.iloc[listaLandmarksDedos] #esto, y lo de abajo, lo hago solo para tener un df y poder graficarlo.
dfDedoscopia=dfDedos.copy()
dfDedoscopia['Z']=0
dfDedoscopia['TIPO']='DEDOS'
dfDedoscopia['TAMAÑO']=tamañoLandmark
dfDedoscopia['Y'].round(1)
if listaDedos[0]>listaDedos[1]:
    tipoPie='Egipcio'
elif listaDedos[0]<listaDedos[1] and listaDedos[1]>listaDedos[2]:
    tipoPie='Griego'
elif listaDedos[0]<listaDedos[1] and listaDedos[1]<listaDedos[2]:
    tipoPie='Cuadrado'
dfMedicion.at[0,'TIPO DE PIE']=tipoPie

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

dfCircEntrada,MedidasPerim=medidaPerimetral(df,MedidasPerim,arrayEntradaPie,'PERIMETRO ENTRADA PIE',paso=0.4,plano='ZX') #medicion en el plano Zx del perimetro
dfCircEmpeine,MedidasPerim=medidaPerimetral(df,MedidasPerim,arrayAlturaEmpeine,'PERIMETRO EMPEINE',paso=0.4,plano='ZX') #medicion en el plano Zx del perimetro
dfcircMetaTarso,MedidasPerim=medidaPerimetral(df,MedidasPerim,[dfInMetaTarso,dfFinMetaTarso],'PERIMETRO METATARSO',diagonal=True,paso=0.2,plano='ZX') #medicion en el plano Zx del perimetro
dfCircTalonEntrada,MedidasPerim=medidaPerimetral(df,MedidasPerim,[dfAlturaTalon,dfEntradaPie],'PERIMETRO TALON - ENTRADA PIE',paso=0.2,inclinado='YX') #medicion en el plano Zx del perimetro
dfCircInTalonEntrada,MedidasPerim=medidaPerimetral(df,MedidasPerim,[dfInicioTalon,dfEntradaPie],'PERIMETRO INICIO TALON - ENTRADA PIE',paso=0.2,inclinado='YX') #medicion en el plano Zx del perimetro
dfCircTalonEmpeine,MedidasPerim=medidaPerimetral(df,MedidasPerim,[dfAlturaTalon,dfEmpeine],'PERIMETRO TALON - EMPEINE',paso=0.1,inclinado='YX') #medicion en el plano Zx del perimetro
dfCircInTalonEmpeine,MedidasPerim=medidaPerimetral(df,MedidasPerim,[dfInicioTalon,dfEmpeine],'PERIMETRO INICIO TALON - EMPEINE',paso=0.2,inclinado='YX') #medicion en el plano Zx del perimetro

for i in range(len(MedidasPerim)):
    dfMedicion.at[0,PerimetrosAMedir[i]]=MedidasPerim[i]
dfMedicion.to_csv('Mediciones.csv',index=False)

dfFinal=pd.concat([df,dfLandmarks3,dfDedoscopia,dfCircEntrada,dfCircEmpeine,dfcircMetaTarso,dfCircTalonEntrada,dfCircInTalonEntrada,dfCircTalonEmpeine,dfCircInTalonEmpeine],ignore_index=True)
fig=px.scatter_3d(dfFinal,x='X',y='Y',z='Z',color='TIPO',size='TAMAÑO',size_max=13)
fig.update_layout(scene=dict(aspectratio=dict(x=1.1, y=3.1, z=1),))
fig.show()







