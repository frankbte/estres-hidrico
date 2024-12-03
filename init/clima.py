import pandas as pd
from meteostat import Point, Daily
from datetime import datetime

# Leer el archivo XLSX desde la ruta adecuada
df = pd.read_excel(r'Descarga_de_datos\descargas_recursos_hidricos\Datos_hídricos_2020-2024XLSX.xlsx')

# Limpiar los nombres de las columnas
df.columns = df.columns.str.strip()

# Convertir la columna 'Fecha' a formato datetime
df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')

# Definir el rango de fechas desde el archivo
start_date = df['Fecha'].min()
end_date = df['Fecha'].max()

# Definir la ubicación (latitud y longitud de la estación)
latitud = 29.072967 
longitud = -110.955919

# Crear un objeto Point de Meteostat con la ubicación
location = Point(latitud, longitud)

# Obtener los datos climáticos diarios desde el rango
data_clima = Daily(location, start_date, end_date)
data_clima = data_clima.fetch()

# Asegurarse de que las fechas están en el mismo formato (sin hora)
data_clima.index = data_clima.index.date
df['Fecha'] = df['Fecha'].dt.date

# Agregar las columnas de temperatura, precipitación, etc.
def obtener_dato_clima(fecha, variable):
    try:
        return data_clima.loc[fecha, variable] if fecha in data_clima.index else 0
    except KeyError:
        return 0

df['Temperature'] = df['Fecha'].apply(lambda x: obtener_dato_clima(x, 'tavg'))
df['Precipitation'] = df['Fecha'].apply(lambda x: obtener_dato_clima(x, 'prcp'))
df['Max Temperature'] = df['Fecha'].apply(lambda x: obtener_dato_clima(x, 'tmax'))
df['Min Temperature'] = df['Fecha'].apply(lambda x: obtener_dato_clima(x, 'tmin'))
df['Temperature Range'] = df['Max Temperature'] - df['Min Temperature']

# Condiciones adicionales
df['Wind Speed'] = df['Fecha'].apply(lambda x: obtener_dato_clima(x, 'wspd'))
df['Pressure'] = df['Fecha'].apply(lambda x: obtener_dato_clima(x, 'pres'))
df['Day with Precipitation'] = df['Precipitation'].apply(lambda x: x > 0 if pd.notnull(x) else False)

# Rellenar con 0 cualquier valor nulo (NaN) en todo el DataFrame
df = df.fillna(0)

# Guardar el DataFrame como archivo CSV en lugar de Excel
df.to_csv('init/datos_con_clima_y_condiciones.csv', index=False)
