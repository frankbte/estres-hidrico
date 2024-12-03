# Usa una imagen oficial de Python
FROM python:3.10

# Configura el directorio de trabajo
WORKDIR /app

# Copia el archivo de dependencias y lo instala
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copia toda la carpeta 'Descarga_de_datos' al contenedor


# Copia los archivos de inicialización de PostgreSQL
COPY init/presas.csv /docker-entrypoint-initdb.d/presas.csv
COPY init/almacenamiento.csv /docker-entrypoint-initdb.d/almacenamiento.csv


# Expone el puerto de Django
EXPOSE 8000

# Copia el resto del código del proyecto al contenedor
COPY . /app
