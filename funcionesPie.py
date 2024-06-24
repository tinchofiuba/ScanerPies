import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def Metatarso(df,minx,maxx):
  maxyMetatarzoIn=df[df['X']==minx]['Y'].max()
  maxzMetatarzoIn=df[(df['X']==minx) & (df['Y']==maxyMetatarzoIn)]['Z'].max()
  iniMetaTarso=[minx,maxyMetatarzoIn,maxzMetatarzoIn]#<--------------------vector inicio del metatarzo, izquierda
  iniMetatarsoLargo=[minx,maxyMetatarzoIn,0]
  maxyMetatarsoFin=df[df['X']==maxx]['Y'].max()
  maxzMetatarsoFin=df[(df['X']==maxx) & (df['Y']==maxyMetatarsoFin)]['Z'].max()
  finMetaTarso=[maxx,maxyMetatarsoFin,maxzMetatarsoFin]#<--------------------vector fin del metatarzo, derecha
  finMetatarsoLargo=[maxx,maxyMetatarsoFin,0]
  anchoMetatarsiano=norma(iniMetatarsoLargo,finMetatarsoLargo)#<--------------------ancho metatarsiano
  return iniMetaTarso,finMetaTarso,anchoMetatarsiano

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