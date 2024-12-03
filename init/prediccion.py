import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import TimeSeriesSplit

# Cargar los datos desde archivos CSV
df_almacenamiento = pd.read_csv('C:/Users/bdgae/Documents/GitHub/estres-hidrico/init/almacenamiento.csv', parse_dates=['fecha'])
df_clima = pd.read_csv('C:/Users/bdgae/Documents/GitHub/estres-hidrico/init/datos_con_clima_y_condiciones.csv', parse_dates=['Fecha'])

# Verifica los nombres de las columnas
print("Columnas de df_almacenamiento:", df_almacenamiento.columns)
print("Columnas de df_clima:", df_clima.columns)

# Combinar los datos de almacenamiento y clima
df_original = pd.merge(df_almacenamiento, df_clima, left_on=['clave', 'fecha'], right_on=['Clave', 'Fecha'], how='left')

# Verifica las primeras filas para asegurarte de que los datos se combinan correctamente
print(df_original.head())

# Verificar las columnas después de la combinación
print("Columnas de df_original:", df_original.columns)

# Lista de presas
presas = ['LCDSO', 'PECSO', 'AOBSO', 'AGZCH', 'ARCSO', 'PMOSO', 'ARLSO', 'CHTSO', 'IRASO']

# Funciones auxiliares
def crear_caracteristicas(df):
    df = df.copy()
    df['dayofweek'] = df.index.dayofweek
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear
    df['dayofmonth'] = df.index.day
    df['weekofyear'] = df.index.isocalendar().week
    return df

def add_lags(df):
    target_map = df['almacenamiento'].to_dict()  # Cambiar 'nivel_agua' por 'almacenamiento'
    df['lag1'] = (df.index - pd.Timedelta('364 days')).map(target_map)
    df['lag2'] = (df.index - pd.Timedelta('728 days')).map(target_map)
    df['lag3'] = (df.index - pd.Timedelta('1092 days')).map(target_map)
    return df

def prediccion(df, clave):
    # Asegúrate de que la columna 'almacenamiento' existe en el DataFrame
    if 'almacenamiento' not in df.columns:
        print(f"Error: 'almacenamiento' no encontrada en los datos para la presa {clave}")
        return
    
    # Convertir la fecha límite en un objeto datetime
    fecha_limite = pd.to_datetime('2022-07-01')
    
    # Dividir el dataset
    train = df['almacenamiento'].loc[df.index < fecha_limite]
    test = df['almacenamiento'].loc[df.index >= fecha_limite]
    
    df = df.sort_index()
    df = add_lags(df)
    
    # Asegurarse de que las columnas categóricas sean convertidas a tipo numérico
    df['dia_con_precipitacion'] = df['dia_con_precipitacion'].astype(int)
    
    # Hacemos cross-validation para series temporales
    tss = TimeSeriesSplit(n_splits=3, test_size=365, gap=24)
    df = df.sort_index()

    fold = 0
    preds = []
    scores = []
    
    for train_idx, val_idx in tss.split(df):
        train = df.iloc[train_idx]
        test = df.iloc[val_idx]

        train = crear_caracteristicas(train)
        test = crear_caracteristicas(test)

        FEATURES = ['dayofyear', 'dayofweek', 'quarter', 'month', 'year',
                    'lag1', 'lag2', 'lag3', 'Temperature', 'Precipitation', 'Max Temperature', 'Min Temperature', 
                    'Temperature Range', 'Wind Speed', 'Pressure', 'Day with Precipitation']
        TARGET = 'almacenamiento'  # Cambiar 'nivel_agua' por 'almacenamiento'

        X_train = train[FEATURES]
        y_train = train[TARGET]

        X_test = test[FEATURES]
        y_test = test[TARGET]

        # Crear modelo de XGBoost
        reg = xgb.XGBRegressor(base_score=0.5, booster='gbtree',    
                               n_estimators=1000,
                               early_stopping_rounds=50,
                               objective='reg:squarederror',  # Cambiar a reg:squarederror
                               max_depth=3,
                               learning_rate=0.01)
        reg.fit(X_train, y_train,
                eval_set=[(X_train, y_train), (X_test, y_test)],
                verbose=False)

        y_pred = reg.predict(X_test)
        preds.append(y_pred)
        score = np.sqrt(mean_squared_error(y_test, y_pred))
        scores.append(score)
        
        print(f'[Presa {clave}] Score across folds: {np.mean(scores):0.4f}')
 
    # Hacer predicciones futuras
    df = crear_caracteristicas(df)
    FEATURES = ['dayofyear', 'dayofweek', 'quarter', 'month', 'year',
                'lag1', 'lag2', 'lag3', 'Temperature', 'Precipitation', 'Max Temperature', 'Min Temperature', 
                'Temperature Range', 'Wind Speed', 'Pressure', 'Day with Precipitation']
    TARGET = 'almacenamiento'  # Cambiar 'nivel_agua' por 'almacenamiento'

    X_all = df[FEATURES]
    y_all = df[TARGET]

    reg = xgb.XGBRegressor(base_score=0.5,
                           booster='gbtree',    
                           n_estimators=200,
                           objective='reg:squarederror',  # Cambiar a reg:squarederror
                           max_depth=3,
                           learning_rate=0.01)
    reg.fit(X_all, y_all,
            eval_set=[(X_all, y_all)],
            verbose=False)
    
    future = pd.date_range('2023-06-26', '2024-12-01')
    future_df = pd.DataFrame(index=future)
    future_df['isfuture'] = True
    df['isfuture'] = False
    df_and_future = pd.concat([df, future_df])
    df_and_future = crear_caracteristicas(df_and_future)
    df_and_future = add_lags(df_and_future)

    future_w_features = df_and_future.query('isfuture').copy()
    future_w_features['pred'] = reg.predict(future_w_features[FEATURES])
    
    # Guardar gráfico
    future_w_features['pred'].plot(figsize=(10, 5),
                                   color=sns.color_palette()[4],
                                   ms=1,
                                   lw=1,
                                   title=f'Predicciones 2024 - {clave}')
    plt.savefig(f'predicciones_{clave}.png')
    plt.close()

    # Guardar las predicciones en un archivo CSV
    future_w_features.to_csv(f'predicciones_{clave}.csv')

# Iterar sobre todas las presas
for presa in presas:
    df_presa = df_original[df_original['clave'] == presa].drop('clave', axis=1)  # Cambiar 'clave_presa' por 'clave'
    prediccion(df_presa, presa)
