import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

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
        if v>max_lZmin:
            indice=lZmin.index(v)
            if lZmin[indice+2]>max_lZmin:
                break
    return lYmin[indice],lZmin[indice]

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
def PolyAjuste(df,punto,**kwargs):
  coord='XYZ'
  columnas=['X','Y','Z']
  for key, value in kwargs.items():
    if key=='plano':
      avance=value[0]
      avanceRecta=value[1]
      #le saco "X" a coord (XYZ)
      for i in range(2):
        coord=coord.replace(value[i],'')
      ultimaCoord=coord #me quedo con la coordenada que no se eligió en el plano.
      #{ejecucion de la funcion}
    if key=='paso': #seteo el paso +- del corte 
      paso=value
    else:
      paso=0.5
    if key=='grado':
      grado=value
    else:
      grado=5
  dfAjuste=df[(df[ultimaCoord]>punto[1]-paso) &(df[ultimaCoord]<punto[1]+paso)]
  dfAjuste[ultimaCoord]=punto[1]
  dfAjuste['TIPO']='DATO'
  dfAjuste['TAMAÑO']=12
  df1=dfAjuste[(dfAjuste[avanceRecta]>=punto[0])]
  df2=dfAjuste[(dfAjuste[avanceRecta]<punto[0])]
  dfs=[df1,df2]
  cuadrantes=[]
  cuadSupInf=[]
  #grafico df1 solamente
  #guardo en un txt a df1
  df1.to_csv('df1.csv',sep=',',index=False)
  #plt.plot(df1[avanceRecta],df1[avance],label='df1')
  #plt.show()
  for i in range(2):
    DF=dfs[i]
    if i==0:
      maxMin_AvRecta=DF[avanceRecta].max()
    else:
      maxMin_AvRecta=DF[avanceRecta].min()
    minAv=DF[DF[avanceRecta]==maxMin_AvRecta][avance].min()
    print(f"minimo Z: {minAv} para {i} si es 0 es mayor al X")
    DFsup=DF[DF[avance]>=minAv]
    DFinf=DF[DF[avance]<=minAv]
    cuadSupInf.append([DFsup,DFinf]) #guardo 1°cuadrante, 2°cuadrante si i=0 sino 3° y 4°
    fig=px.scatter_3d(cuadSupInf[0][0],x='X',y='Y',z='Z',color='TIPO',size='TAMAÑO',size_max=13)
    fig.update_layout(scene=dict(aspectratio=dict(x=1.1, y=3.1, z=1),))
    fig.show()
  DFsup=pd.concat([cuadSupInf[0][0],cuadSupInf[1][0]],ignore_index=True)
  DFinf=pd.concat([cuadSupInf[0][1],cuadSupInf[1][1]],ignore_index=True)
  cuadSupInf=[DFsup,DFinf]
  lAjuste=[]
  for i in range(2):
    avRectaCombo=cuadSupInf[i][avanceRecta]
    avanceCombo=cuadSupInf[i][avance]
    cuadrantes.append(dfAjuste)
  return cuadrantes

 

def medicionPerimetro(df,dictlargos,tamañoLandmark):
  j=0
  dictPerimetroSumados={}
  listaPerimetros=[]
  for key,dfcurva in dictlargos.items():
      dfcurva['TIPO']=key
      dfcurva['TAMAÑO']=tamañoLandmark
      dfcurva.sort_values(by='Z', ascending=False, inplace=True)
      #teniendo las coordenadas x,y,z calculo el largo de la curva
      largoCurva=0
      largoCurvas=[]
      for i in range(len(dfcurva)-1):
          coordenada=dfcurva[df.columns[0:3]]
          largoCurva+=norma(coordenada.iloc[i],coordenada.iloc[i+1])
      dictPerimetroSumados['Largo '+key]=largoCurva
      print(f'Largo de {key}: {largoCurva}mm')
      j+=1
  #itero de dos en dos para sumar key0 con key1 y asì sucesivamente
  for i in range(0,len(dictPerimetroSumados),2):
      key0=list(dictPerimetroSumados.keys())[i]
      key1=list(dictPerimetroSumados.keys())[i+1]
      suma=dictPerimetroSumados[key0]+dictPerimetroSumados[key1]
      listaPerimetros.append(suma)
  indiceMax=listaPerimetros.index(max(listaPerimetros))
  dictlargos['PMaxm']=dictlargos[list(dictlargos.keys())[indiceMax*2]]
  dictlargos['PMaxM']=dictlargos[list(dictlargos.keys())[indiceMax*2+1]]
  perimMax=np.max(listaPerimetros)
  print(f'El perimetro máximo es: {perimMax}mm')
  df=pd.concat([df,dictlargos['PMaxm']],ignore_index=True)
  df=pd.concat([df,dictlargos['PMaxM']],ignore_index=True)
  return df,dictlargos 

def curvasPerimetrales(df,ejeMax,ejeCorte): #ejemax, eje donde se busca un máximo, ejecorte,
  #eje en el cual se buscan valores mayores o menores al corte
  maxZ=np.round(df[ejeMax].max(),1)
  df1=df.copy()
  df1=df1[df1[ejeMax]==maxZ]
  if len(df1)==1:
    corte=df1[ejeCorte].values[0]
    df1a=df[df[ejeCorte]>=corte] 
    df1b=df[df[ejeCorte]<corte]
  else:
    corte=df1[ejeCorte].mean()
    df1a=df[df[ejeCorte]>=corte] 
    df1b=df[df[ejeCorte]<corte]
  return df1a,df1b

def caso_vertical(df,avance,avanceRecta,ultimaCol,ordIni):
  dictlargos={}
  #armo un dict vacio
  dfm,dfM=curvasPerimetrales(df[df[avanceRecta]==ordIni],avance,ultimaCol)
  #añado al diccionario las curvas
  dictlargos['curvaLandmark_m']=dfm
  dictlargos['curvaLandmark_M']=dfM
  for paso in range(1,13,1):
    dfm,dfM=curvasPerimetrales(df[df[avanceRecta]==ordIni-np.round(paso/10,1)],avance,ultimaCol)
    dictlargos[f'curva+{paso}m']=dfm
    dictlargos[f'curva+{paso}M']=dfM
    dfm,dfM=curvasPerimetrales(df[df[avanceRecta]==ordIni-np.round(-paso/10,1)],avance,ultimaCol)
    dictlargos[f'curva-{paso}m']=dfm
    dictlargos[f'curva-{paso}M']=dfM
  #maximo1=dfma[avanceRecta].max()
  #dfmaxavancerecta=dfma[dfma[avanceRecta]==maximo1][avance]
  return pd.DataFrame(df[df[avanceRecta]==ordIni]),dictlargos #devuelve df y luego las curvas.
#las curvas van el orden de (curva1,curva2,y el resto en duplas que van en 4,8,12 +-

def generacionLinea(df,avance,avanceRecta,ordIni,ordFin,abscisaIni,abscisaFin):
    #en función de las coordenadas ingresadas en "avance" y en "avanceRecta"
    #obtengo la variable que no es ni "avance" ni "avanceRecta"
    col=df.columns
    colDif=col.difference([avance,avanceRecta])
    ultimaCol=colDif.to_list()[0]
    columnas=[avance,avanceRecta,ultimaCol]
    dictCurva={avance:[],avanceRecta:[],ultimaCol:[]}
    #ingreso un df y los puntos inciales para obtener una linea y calculo m y b
    if (ordFin-ordIni)==0: #si quiero un corte vertical
      return caso_vertical(df,avance,avanceRecta,ultimaCol,ordIni)
    elif (abscisaFin-abscisaIni)==0: #si quiero un corte horizontal (en este caso no serìa útil)
      df1a,df2b=curvasPerimetrales(df[df[avanceRecta]==ordIni],avance,ultimaCol)
      return pd.DataFrame(df[df[avanceRecta]==ordFin]),df1a,df2b
    else:
      m=round((abscisaFin-abscisaIni)/(ordFin-ordIni),6)
      b=round(abscisaIni-ordIni*m,6)
      #genero una linea con np.linspace con un paso de 0.1 entre ordIni y ordFin
      NumPasos=int(abs(ordFin-ordIni)*10)
      pasos=np.round(np.linspace(ordIni,ordFin,NumPasos),1)#hago los pasos en el sentido de las ordenadas
      for paso in pasos:
        PasoRecta=round(m*paso+b,1)
        coord=df[(df[avance]==paso) & (df[avanceRecta]==PasoRecta)][ultimaCol]
        if len(coord)>1:
          dictCurva[columnas[0]].append(paso)
          dictCurva[columnas[1]].append(PasoRecta)
          dictCurva[columnas[2]].append(np.round(coord.min(),1))
          dictCurva[columnas[0]].append(paso)
          dictCurva[columnas[1]].append(PasoRecta)
          dictCurva[columnas[2]].append(np.round(coord.max(),1))
        elif len(coord)==1:
          dictCurva[columnas[0]].append(paso)
          dictCurva[columnas[1]].append(PasoRecta)
          dictCurva[columnas[2]].append(np.round(coord.min(),1))
      
      return pd.DataFrame(dictCurva)

    


