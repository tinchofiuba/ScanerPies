import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

#función para determinar:
#1-altura de la punta del pie
#2-tipo de pie
#3-pie izquierdo o derecho
def tipoPie(df,listaLandmarksDedos,dfLandmarks,tamañoLandmark,dfMedicion): 
  listaDedos=[dfLandmarks.iloc[dedo]['Y'].round(1) for dedo in listaLandmarksDedos] #creo una lista con las coordenadas
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
  if 9 in listaLandmarksDedos:
    y=dfLandmarks.iloc[9]['Y'] #Y que ubica el soft para el dedo chiquito
    print(f"el y para la punta del pie es: {y-20}")
    alturaPuntaPie=df[df['Y']>(y-20)]['Z'].max() #le resto 2cm hacia el talón
  else:
    maxy=df['Y'].max()
    alturaPuntaPie=df[df['Y']>(maxy-30)]['Z'].max()
  if 9 in listaLandmarksDedos and 7 in listaLandmarksDedos:
    if dfLandmarks.iloc[7]['X']>dfLandmarks.iloc[9]['X']:
      izqOder='IZQUIERDO'
    else:
      izqOder='DERECHO'
  ymedia=df['Y'].max()/2
  dfYmedia=df[(df['Y']>ymedia-1) & (df['Y']<ymedia+1)]['Z']
  alturaMitadPie=dfYmedia.max()
  dfMedicion.at[0,'TIPO DE PIE']=tipoPie
  dfMedicion.at[0,'ALTURA PUNTA DE PIE']=alturaPuntaPie
  dfMedicion.at[0,'PIE IZQ/DER']=izqOder
  dfMedicion.at[0,'ALTURA MITAD DEL PIE']=alturaMitadPie
  return dfDedoscopia,dfMedicion,izqOder

def chequeoData(df):
  if df.isnull().values.any():
    print('Hay valores nulos en el dataframe')
  else:
    #si hay algun string en el dataframe encunetro la fila
    for i in range(len(df)):
      if df.iloc[i].apply(type).eq(str).any():
        print('Hay strings en el dataframe en la fila ',i)
        break
  return None

def izqOder(df,dflandmarks):
  #si el lado izquierdo es mayor que el derecho, es un pie izquierdo
  if dflandmarks['X'].max()>dflandmarks['X'].min():
    lado='IZQUIERDO'
  else:
    lado='DERECHO'
  return lado

def Metatarso(df,maxx,maxy,izqOder,dfMedicion):
  minx=df[df['Y']>maxy/2]['X'].min()
  maxyMetatarzoIn=df[df['X']==minx]['Y'].max()
  maxzMetatarzoIn=df[(df['X']==minx) & (df['Y']==maxyMetatarzoIn)]['Z'].max()
  iniMetaTarso=[minx,maxyMetatarzoIn,maxzMetatarzoIn]#<--------------------vector inicio del metatarzo, izquierda
  iniMetatarsoLargo=[minx,maxyMetatarzoIn,0]
  maxyMetatarsoFin=df[df['X']==maxx]['Y'].max()
  maxzMetatarsoFin=df[(df['X']==maxx) & (df['Y']==maxyMetatarsoFin)]['Z'].max()
  finMetaTarso=[maxx,maxyMetatarsoFin,maxzMetatarsoFin]#<--------------------vector fin del metatarzo, derecha
  finMetatarsoLargo=[maxx,maxyMetatarsoFin,0]
  anchoMetatarsiano=norma(iniMetatarsoLargo,finMetatarsoLargo)#<--------------------ancho metatarsiano
  if izqOder=='IZQUIERDO':
    z=df[(df['Y']>iniMetaTarso[1]-1) & (df['Y']<iniMetaTarso[1]+1)]['Z'].max()
    alturaMetatarso=z.max()
    #si se da esta desigualdad significa que la punta del pie tiene un punto más alto que el metatarso, lo que sería una anomalia/error
    #se guarda el la columna anomalías
    alturaDelanteraMetatarso=df[df['Y']>iniMetaTarso[1]]['Z'].max() 
    if alturaDelanteraMetatarso>alturaMetatarso:
      dfMedicion.at[0,'ANOMALIAS']='puntaPieAlta'
  elif izqOder=='DERECHO':
    z=df[(df['Y']>finMetaTarso[1]-1) & (df['Y']<finMetaTarso[1]+1)]['Z'].max()
    alturaMetatarso=z.max()
    #si se da esta desigualdad significa que la punta del pie tiene un punto más alto que el metatarso, lo que sería una anomalia/error
    #se guarda el la columna anomalías
    alturaDelanteraMetatarso=df[df['Y']>finMetaTarso[1]]['Z'].max() 
    if alturaDelanteraMetatarso>alturaMetatarso:
      dfMedicion.at[0,'ANOMALIAS']='puntaPieAlta'
  dfMedicion.at[0,'ANCHO METATARSICO']=np.round(anchoMetatarsiano,1)
  dfMedicion.at[0,'ALTURA MAX METATARSO']=np.round(alturaMetatarso,1)
  return iniMetaTarso,finMetaTarso,dfMedicion

def alturaTalon(df,miny,dfMedicion):
    AlturaMaxTalon=df[df['Y']==miny]['Z'].min().round(1)
    dfMedicion.at[0,'ALTURA TALON']=AlturaMaxTalon
    xAlturaMaxTalon=df[(df['Z']==AlturaMaxTalon) & (df['Y']==miny)]['X'].mean()
    return xAlturaMaxTalon,AlturaMaxTalon,dfMedicion

def ecRecta(p1,p2):
  m=(p2[1]-p1[1])/(p2[0]-p1[0])
  b=p1[1]-m*p1[0]
  return m,b

def anguloApertura(df):
  minxTrasero=df[df['Y']<df['Y'].max()/2]['X'].min()
  yminxTrasero=df[df['X']==minxTrasero]['Y'].min()
  p1=[minxTrasero,yminxTrasero]
  minxDelantero=df[df['Y']>df['Y'].max()/2]['X'].min()
  yminxDelantero=df[df['X']==minxDelantero]['Y'].max()
  p2=[minxDelantero,yminxDelantero]
  #-------------------------------
  maxxTrasero=df[df['Y'<df['Y'].max()/2]]['X'].max()
  ymaxxTrasero=df[df['X']==maxxTrasero]['Y'].min()
  p3=[maxxTrasero,ymaxxTrasero]
  maxxDelantero=df[df['Y']>df['Y'].max()/2]['X'].max()
  ymaxxDelantero=df[df['X']==maxxDelantero]['Y'].max()
  p4=[maxxDelantero,ymaxxDelantero]
  m1,b1=ecRecta(p1,p2)
  m2,b2=ecRecta(p3,p4)
  #con las dos rectas saco el angulo entre ellas
  apertura=np.arctan((m2-m1)/(1+m1*m2))
  return apertura

def largoAnchoEntrada(df,dfLandmarks,maxy,miny,maxx,minx,xyz,dfMedicion):
    LargoPie=np.round(maxy-miny,1)
    dfMedicion.at[0,'LARGO']=LargoPie
    AnchoPie=maxx-minx
    dfMedicion.at[0,'ANCHO TOTAL']=AnchoPie
    #si se da la siguiente desigualdad significa que hay una anomalía con el ancho del pie.
    #natualmente el ancho del pie está en la parte delantera del pie.
    #En caso contrario se guarda en la columna anomalías como "pieAnchoTrasero"
    yxMinimo=df[df['X']==minx]['Y'].min()
    if yxMinimo<(df['Y'].max()/2):
      #si la columna ANOMALIAS no está vacía le agrego ",pieAnchoTrasero" asi separo las anomalias
      if dfMedicion.at[0,'ANOMALIAS']!='':
          dfMedicion.at[0,'ANOMALIAS']+=',pieAnchoTrasero'
      else:
          dfMedicion.at[0,'ANOMALIAS']='pieAnchoTrasero'
    #me fijo que tipo de pie es, osea, si la apertura hacie adelante aumenta o disminuye
    apertura=anguloApertura(df)
    #en caso de que la apertura sea negativa significa que el pie se ensancha hacia adelante
    dfMedicion.at[0,'APERTURA']=apertura
    arrayEntradaPie=dfLandmarks.iloc[11]#<--------------------array entradaPie
    if len(df[df['Y']==arrayEntradaPie['Y']])>1:
        Zentrada=df[df['Y']==arrayEntradaPie['Y']]['Z'].max()
        Xentrada=df[(df['Y']==arrayEntradaPie['Y']) & (df['Z']==Zentrada)]['X'].mean()
        #reasigno los valores de X y Z para un valor máximo de Z 
        #(en ocasiones el landmark está corrido en el sentido X)
        arrayEntradaPie['X']=Xentrada
        arrayEntradaPie['Z']=Zentrada
    dfEntradaPie=pd.DataFrame([arrayEntradaPie],columns=xyz)
    dfMedicion.at[0,'ALTURA ENTRADA']=arrayEntradaPie['Z']
    return arrayEntradaPie,dfEntradaPie,dfMedicion

def InicioTalon(df,lZmin,lYmin,AlturaMaxTalon,limiteY):
    df_y=df[df['Y']<limiteY/2]
    for y in np.round(df_y['Y'].unique(),1):
        df_y2 = df_y[df_y['Y'] == y]
        if df_y2['Z'].min() < AlturaMaxTalon:
            lZmin.append(df_y2['Z'].min())
            lYmin.append(y)
    lZmin=lZmin[::-1]
    largo=int(len(lZmin)/3) 
    max_lZmin=np.max(lZmin[:largo])
    for v in lZmin:
        if v>max_lZmin+1:
            indice=lZmin.index(v)
            if lZmin[indice+1]>max_lZmin:
                break
    return lYmin[::-1][indice],np.round(lZmin[indice])

def norma(v1, v2):
    return np.linalg.norm(np.array(v1) - np.array(v2))

def Maximos(listaMax):
  maximos=[]
  largos=[]
  i=0
  for i,v in enumerate(listaMax):
    if i!=0:
      if v>listaMax[i-1]:
          if i+1<(len(listaMax)-1):
              if v>=listaMax[i+1]:
                  if v in maximos:
                    print('repetido')
                  else:
                    maximos.append(v)
                    largos.append(i)
    else:
      maximos.append(v)
      largos.append(i)
  return (maximos,largos)
   
def Minimos(listaMin):
  i=0
  largos=[]
  minimos=[]
  for i,v in enumerate(listaMin):
    if i!=0:
      if v<listaMin[i-1]:
        if i+1<(len(listaMin)-1):
          if v<listaMin[i+1]:
              if v in minimos:
                 print('repetido')
              else:
                minimos.append(v)
                largos.append(i)
    else:
      minimos.append(v)
      largos.append(i)
  return (minimos,largos)

#--------------------------------------------------------------
#--------------------------------------------------------------
#--------------------------------------------------------------

def MedicionPerimetro(df,coord):
  max1coord=df[coord[0]].max() #maximo de la coordenada 1
  max2_1coord=df[df[coord[0]]==max1coord][coord[1]].max() #busco que valores de coord[1] existen para el max1coord
  df1=df[df[coord[1]]>=max2_1coord]
  df2=df[df[coord[1]]<=max2_1coord]
  df1_2=[df1,df2]
  i=0
  listaCuadrantes=[]
  listaPerimetros=[]
  for dfi in df1_2:
    if i==0:
      limCoord1=dfi[coord[1]].max() #si estamos del lado de mayor coord[1]
    else:
      limCoord1=dfi[coord[1]].min() #si estamos del lado de menor coord[1]
    limcoord0=dfi[dfi[coord[1]]==limCoord1][coord[0]].max()
    dfi_M=dfi[dfi[coord[0]]>=limcoord0].sort_values(by=coord[1])
    sentido=np.sign(dfi_M[coord[0]].iloc[-1]-dfi_M[coord[0]].iloc[0])
    #viendo el sentido en cual va la curva en coord[0] si veo que al avanzar en coord[1] en un momento 
    #se retrocede en coord[0] elimino ese punto ya que al avanzar y retroceder el perimetro medirá más
    dfi_MFiltrado=dfi_M[dfi_M[coord[0]].diff().fillna(0)*sentido>=0]
    dfi_m=dfi[dfi[coord[0]]<=limcoord0].sort_values(by=coord[1])
    sentido=np.sign(dfi_m[coord[0]].iloc[-1]-dfi_m[coord[0]].iloc[0])
    #viendo el sentido en cual va la curva en coord[0] si veo que al avanzar en coord[1] en un momento 
    #se retrocede en coord[0] elimino ese punto ya que al avanzar y retroceder el perimetro medirá más
    dfi_mFiltrado=dfi_m[dfi_m[coord[0]].diff().fillna(0)*sentido>=0]
    listaCuadrantes.append([dfi_MFiltrado,dfi_mFiltrado])
    for j in range(2):
      dfij=listaCuadrantes[i][j]
      dfijCopia=dfij.copy()
      dfijCopia['TIPO']=f'Cuadrante {i+1} {j+1}'
      dist=np.linalg.norm(listaCuadrantes[i][j][coord].diff().dropna(), axis=1)
      perimInd=dist.sum()
      listaPerimetros.append(perimInd)
    i+=1
  medicion=np.round(sum(listaPerimetros),1)
  dfijCopia=pd.concat([listaCuadrantes[0][0],listaCuadrantes[0][1],listaCuadrantes[1][0],listaCuadrantes[1][1]],ignore_index=True)
  return dfijCopia,medicion

def funcPlano(df,puntos,paso,avance,avanceRecta,ultimaCoord,columnas,tag):
  if type(puntos)==list:
    punto=puntos[0]
  else:
    punto=puntos
  #falta ver el tema de la coordenada!
  cuadSupInf=[]
  dfLonja=df[(df[ultimaCoord]>punto[ultimaCoord]-paso) &(df[ultimaCoord]<punto[ultimaCoord]+paso)]
  dflonjaCopia=dfLonja.copy()
  dflonjaCopia['TIPO']=tag
  dflonjaCopia['TAMAÑO']=12
  dflonjaCopia[ultimaCoord]=punto[1]
  dfCortado,medicion=MedicionPerimetro(dflonjaCopia,[avance,avanceRecta])
  return dflonjaCopia,medicion

def funcPlanoInclinado(df,puntos,paso,avance,avanceRecta,ultimaCoord,columnas,tag):
  puntoIni=puntos[0][columnas]
  puntoFin=puntos[1][columnas]
  m=(puntoFin[ultimaCoord].iloc[0]-puntoIni[ultimaCoord].iloc[0])/(puntoFin[avance].iloc[0]-puntoIni[avance].iloc[0])
  b=puntoIni[ultimaCoord].iloc[0]-m*puntoIni[avance].iloc[0]
  pIni=puntoIni[avance].iloc[0]
  pFin=puntoFin[avance].iloc[0]
  ordenadas=np.linspace(pIni,pFin,int(abs(pIni-pFin)*10))
  ordenadas=np.round(ordenadas,1)
  imgRecta=np.round((m*ordenadas+b),1)
  maxCorte=[]
  minCorte=[]
  for i in range(len(imgRecta)):
    dfCorte=df[(df[avance]<=ordenadas[i]+paso) & (df[avance]>=ordenadas[i]-paso)]
    dfCorte=dfCorte[(dfCorte[ultimaCoord]<=imgRecta[i]+paso) & (dfCorte[ultimaCoord]>=imgRecta[i]-paso)]
    dfCorte[ultimaCoord]=imgRecta[i]
    dfCorte[avance]=ordenadas[i]
    if len(dfCorte)>0:
      maxCorte.append(dfCorte)
  dfCorte=pd.concat(maxCorte,ignore_index=True)
  dfCorte['TIPO']=tag
  dfCorte['TAMAÑO']=13
  dfCortado,medicion=MedicionPerimetro(dfCorte,[avance,avanceRecta])
  return dfCorte,medicion

def funcDiagonal(df,puntos,paso,avance,avanceRecta,ultimaCoord,columnas,tag):
  puntoIni=puntos[0]
  puntoFin=puntos[1]
  m=(puntoFin[ultimaCoord]-puntoIni[ultimaCoord])/(puntoFin[avanceRecta]-puntoIni[avanceRecta])
  m=m.iloc[0] 
  b=puntoIni[ultimaCoord]-m*puntoIni[avanceRecta]
  b=b.iloc[0]
  pIni=puntoIni[avanceRecta].iloc[0]
  pFin=puntoFin[avanceRecta].iloc[0]
  ordenadas=np.linspace(pIni,pFin,int(abs(pIni-pFin)*10))
  ordenadas=np.round(ordenadas,1)
  imgRecta=np.round((m*ordenadas+b),1)
  maxCorte=[]
  minCorte=[]
  for i in range(len(imgRecta)):
    dfCorte=df[df[avanceRecta]==ordenadas[i]]
    dfCorte=dfCorte[(dfCorte[ultimaCoord]<=imgRecta[i]+paso) & (dfCorte[ultimaCoord]>=imgRecta[i]-paso)]
    dfCorte[ultimaCoord]=imgRecta[i]
    if len(dfCorte)>0:
      maxCorte.append(dfCorte)
  dfCorte=pd.concat(maxCorte,ignore_index=True)
  dfCorte['TIPO']=tag
  dfCorte['TAMAÑO']=13
  dfCortado,medicion=MedicionPerimetro(dfCorte,[avance,avanceRecta])
  return dfCorte,medicion

def medidaPerimetral(df,listaMedidas,puntos,tag,**kwargs):
  coord='XYZ'
  columnas=['X','Y','Z']
  if 'paso' in kwargs:
    paso=kwargs['paso']
  else:
    paso=0
  if 'plano' in kwargs:
    avance=kwargs['plano'][0]
    avanceRecta=kwargs['plano'][1]
    for i in range(2):
      coord=coord.replace(kwargs['plano'][i],'')
    ultimaCoord=coord
    if 'diagonal' in kwargs:
      dfObtenido,medicion=funcDiagonal(df,puntos,paso,avance,avanceRecta,ultimaCoord,columnas,tag)
    else: #si no es diagonal es en un plano horizontal o vertical
      dfObtenido,medicion=funcPlano(df,puntos,paso,avance,avanceRecta,ultimaCoord,columnas,tag)
  elif 'inclinado' in kwargs:
    avance=kwargs['inclinado'][0]
    avanceRecta=kwargs['inclinado'][1]
    for i in range(2):
      coord=coord.replace(kwargs['inclinado'][i],'')
    ultimaCoord=coord
    dfObtenido,medicion=funcPlanoInclinado(df,puntos,paso,avance,avanceRecta,ultimaCoord,columnas,tag) 
  listaMedidas.append(medicion)
  return dfObtenido,listaMedidas