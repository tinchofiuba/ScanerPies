import pandas as pd
import numpy as np
tag="Martin000"
df=pd.read_csv('Mediciones.csv')
if tag in df['TAG'].values:
    valores=df['TAG'].values
    print(valores)
    tags=np.unique([tagDuplicado for tagDuplicado in valores if tag in tagDuplicado])
    lenTags=[len(tag) for tag in tags]
    print(tags)
    print(lenTags)
    if len(tags)>1:
        tagMasLargo=tags[np.argmax(lenTags)]
        tag=tagMasLargo+".duplicado"
    else:
        tag=tag+".duplicado"
print(tag)