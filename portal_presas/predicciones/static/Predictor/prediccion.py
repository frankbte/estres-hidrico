import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error

# Directorio donde se guardarán las predicciones y fotos
directorio_predictor = 'static/Predictor'

# Crear la carpeta si no existe
os.makedirs(directorio_predictor, exist_ok=True)

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
    
    # Convertir 'dia_con_precipitacion' a numérico si es necesario
    df['dia_con_precipitacion'] = df['dia_con_precipitacion'].apply(lambda x: 1 if x == 'Yes' else 0)
    
    return df

# Función de predicción utilizando XGBoost
def prediccion_xgboost(df, clave):
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
    
    # Crear y entrenar el modelo XGBoost
    reg = xgb.XGBRegressor(base_score=0.5, booster='gbtree',    
                           n_estimators=1000,
                           early_stopping_rounds=50,
                           objective='reg:squarederror',  
                           max_depth=3,
                           learning_rate=0.01)
    
    # Dividir en entrenamiento y validación usando TimeSeriesSplit
    tscv = TimeSeriesSplit(n_splits=5)
    for train_index, test_index in tscv.split(X_all):
        X_train, X_test = X_all.iloc[train_index], X_all.iloc[test_index]
        y_train, y_test = y_all.iloc[train_index], y_all.iloc[test_index]
        
        reg.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
        
        # Evaluar el modelo
        y_pred = reg.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f'Mean Squared Error for {clave}: {mse}')

    # Hacer predicciones futuras
    future = pd.date_range('2023-06-26', '2024-12-01')
    future_df = pd.DataFrame(index=future)
    future_df['isfuture'] = True
    df['isfuture'] = False
    df_and_future = pd.concat([df, future_df])
    df_and_future = crear_caracteristicas(df_and_future)
    df_and_future = add_lags(df_and_future)

    future_w_features = df_and_future.query('isfuture').copy()
    future_w_features['pred'] = reg.predict(future_w_features[FEATURES])
    
    # Guardar gráfico de predicciones directamente en la carpeta 'Predictor'
    plt.figure(figsize=(10, 5))
    future_w_features['pred'].plot(color='red', ms=1, lw=1, title=f'Predicciones futuras - {clave}')
    plt.savefig(f'{directorio_predictor}/predicciones_{clave}.png')
    plt.close()

    # Guardar las predicciones en un archivo CSV directamente en la carpeta 'Predictor'
    future_w_features[['pred']].to_csv(f'{directorio_predictor}/predicciones_{clave}.csv')

# Cargar los datos
df_original = pd.read_csv('static/Predictor/datos/almacenamiento.csv', parse_dates=['fecha'])
df_clima = pd.read_csv('static/Predictor/datos/datos_con_clima_y_condiciones.csv', parse_dates=['Fecha'])

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
    prediccion_xgboost(df_presa, presa)
