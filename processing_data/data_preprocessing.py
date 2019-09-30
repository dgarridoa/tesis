import numpy as np
import pandas as pd
import pickle as pkl

#Importar la base de datos
df = pd.read_csv('../data/robos_prose.csv', index_col = 'id_prose', usecols = ['id_prose', 'sin_fecha_siniestro', 'sin_relato'], sep=',')
#cambiar el tipo de dato a timestamp
df['sin_fecha_siniestro'] = pd.to_datetime(df['sin_fecha_siniestro'])
#ordenar relatos por fecha
df.sort_values('sin_fecha_siniestro', inplace=True)
#seleccionar relatos entre 2011-2016 y omitir registros con relatos nulos
df = df[(df['sin_fecha_siniestro']>=pd.Timestamp(2011,1,1)) & (df['sin_fecha_siniestro']<pd.Timestamp(2017,1,1)) & (df['sin_relato'].isnull()==False)]

#exportar dataframe
df.to_pickle('../data/robos_prose_v1.pkl')
