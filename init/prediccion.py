import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Crear las carpetas si no existen
if not os.path.exists('fotos_predict'):
    os.makedirs('fotos_predict')

if not os.path.exists('csv_predict'):
    os.makedirs('csv_predict')

# Función para crear características adicionales
def crear_caracteristicas(df):
    df['dayofweek'] = df.index.dayofweek
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear
    df['dayofmonth'] = df.index.day
    df['weekofyear'] = df.index.isocalendar().week
    return df

# Función para agregar lags
def add_lags(df):
    target_map = df['almacenamiento'].to_dict()
    df['lag1'] = (df.index - pd.Timedelta('364 days')).map(target_map)
    df['lag2'] = (df.index - pd.Timedelta('728 days')).map(target_map)
    df['lag3'] = (df.index - pd.Timedelta('1092 days')).map(target_map)
    return df

# Función de predicción utilizando Random Forest
def prediccion_random_forest(df, clave):
    # Dividir el dataset
    train = df['almacenamiento'].loc[df.index < '2022-07-01']
    test = df['almacenamiento'].loc[df.index >= '2022-07-01']
    
    # Preprocesar los datos
    df = df.sort_index()
    df = add_lags(df)
    df = crear_caracteristicas(df)
    
    # Features y target
    FEATURES = ['dayofyear', 'dayofweek', 'quarter', 'month', 'year', 
                'lag1', 'lag2', 'lag3', 'Temperature', 'Precipitation', 
                'Max Temperature', 'Min Temperature', 'Wind Speed', 
                'Pressure', 'dia_con_precipitacion']
    TARGET = 'almacenamiento'
    
    X_all = df[FEATURES]
    y_all = df[TARGET]
    
    # Crear y entrenar el modelo Random Forest
    model_rf = RandomForestRegressor(n_estimators=100, random_state=42)
    model_rf.fit(X_all, y_all)
    
    # Hacer predicciones futuras
    future = pd.date_range('2023-06-26', '2024-12-01')
    future_df = pd.DataFrame(index=future)
    future_df['isfuture'] = True
    df['isfuture'] = False
    df_and_future = pd.concat([df, future_df])
    df_and_future = crear_caracteristicas(df_and_future)
    df_and_future = add_lags(df_and_future)

    future_w_features = df_and_future.query('isfuture').copy()
    future_w_features['pred'] = model_rf.predict(future_w_features[FEATURES])
    
    # Guardar gráfico de predicciones en la carpeta 'fotos_predict'
    plt.figure(figsize=(10, 5))
    future_w_features['pred'].plot(color='red', ms=1, lw=1, title=f'Predicciones futuras - {clave}')
    plt.savefig(f'fotos_predict/predicciones_random_forest_{clave}.png')
    plt.close()

    # Guardar las predicciones en un archivo CSV en la carpeta 'csv_predict'
    future_w_features[['pred']].to_csv(f'csv_predict/predicciones_random_forest_{clave}.csv')

# Cargar los datos
df_original = pd.read_csv('C:/Users/bdgae/Documents/GitHub/estres-hidrico/init/almacenamiento.csv', parse_dates=['fecha'])
df_clima = pd.read_csv('C:/Users/bdgae/Documents/GitHub/estres-hidrico/init/datos_con_clima_y_condicioness.csv', parse_dates=['Fecha'])

# Renombrar y combinar los datos
df_clima.rename(columns={'Day with Precipitation': 'dia_con_precipitacion'}, inplace=True)
df_original = pd.merge(df_original, df_clima, left_on=['clave', 'fecha'], right_on=['Clave', 'Fecha'], how='left')

df_original['fecha'] = pd.to_datetime(df_original['fecha'])
df_original.set_index('fecha', inplace=True)

# Reemplazar valores NaN en las columnas relevantes por 0
cols = ['Temperature', 'Precipitation', 'Max Temperature', 'Min Temperature', 'Wind Speed', 'Pressure', 'dia_con_precipitacion']
df_original[cols] = df_original[cols].fillna(0)

# Lista de presas
presas = df_original['clave'].unique()

# Iterar sobre las presas y hacer las predicciones
for presa in presas:
    df_presa = df_original[df_original['clave'] == presa].drop('clave', axis=1)
    prediccion_random_forest(df_presa, presa)
