# Usa una imagen oficial de Python
FROM python:3.10

# Configura el directorio de trabajo
WORKDIR /app

# Copia el archivo de dependencias y lo instala
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia el código del proyecto
COPY . .

#Copiar el archivo CSV de 'presas' al directorio de inicialización de PostgreSQL
COPY init/presas.csv /docker-entrypoint-initdb.d/presas.csv;

#Copiar el archivo CSV de 'datos_clima' al directorio de inicialización de PostgreSQL
COPY init/datos_clima.csv /docker-entrypoint-initdb.d/datos_clima.csv;

#Copiar el archivo CSV de 'almacenamiento' al directorio de inicialización de PostgreSQL
COPY init/almacenamiento.csv /docker-entrypoint-initdb.d/almacenamiento.csv;


# Expone el puerto de Django
EXPOSE 8000
