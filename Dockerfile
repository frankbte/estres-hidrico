# Usa una imagen oficial de Python
FROM python:3.10

# Configura el directorio de trabajo
WORKDIR /app

# Copia el archivo de dependencias y lo instala
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia toda la carpeta 'Descarga_de_datos' al contenedor
COPY Descarga_de_datos /app/Descarga_de_datos

# Copia los archivos de inicialización de PostgreSQL
COPY init/presas.csv /docker-entrypoint-initdb.d/presas.csv
COPY init/almacenamiento.csv /docker-entrypoint-initdb.d/almacenamiento.csv

# Ejecuta el script de descarga de recursos hidraulicos
RUN python /app/Descarga_de_datos/descargar_recursos_hidraulicos.py

# Expone el puerto de Django
EXPOSE 8000
