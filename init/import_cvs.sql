-- Crear la tabla 'presas'
CREATE TABLE IF NOT EXISTS presas (
    clave_presa VARCHAR(10) PRIMARY KEY,
    nombre_completo VARCHAR(255) NOT NULL,
    nombre_comun VARCHAR(255),
    estado VARCHAR(100),
    municipio VARCHAR(100),
    rio VARCHAR(100),
    latitud DECIMAL(10, 8),
    longitud DECIMAL(11, 8),
    altitud DECIMAL(7, 2)
);

-- Crear la tabla 'almacenamiento'
CREATE TABLE IF NOT EXISTS almacenamiento (
    id_almacenamiento SERIAL PRIMARY KEY,
    clave_presa VARCHAR(10) REFERENCES presas(clave_presa),
    fecha DATE NOT NULL,
    nivel_agua DECIMAL(10, 2)
);

-- Crear la tabla 'clima' con las columnas necesarias
CREATE TABLE IF NOT EXISTS clima (
    clave_presa VARCHAR(10) REFERENCES presas(clave_presa),
    fecha DATE NOT NULL,
    temperatura DECIMAL(5, 2),
    precipitacion DECIMAL(5, 2),
    temperatura_max DECIMAL(5, 2),
    temperatura_min DECIMAL(5, 2),
    rango_temperatura DECIMAL(5, 2),
    velocidad_viento DECIMAL(5, 2),
    presion DECIMAL(5, 2),
    dia_con_precipitacion BOOLEAN,
    PRIMARY KEY (clave_presa, fecha)
);

-- Cargar los datos en la tabla 'presas' desde el archivo CSV correspondiente
COPY presas (
    clave_presa,
    nombre_completo,
    nombre_comun,
    estado,
    municipio,
    rio,
    latitud,
    longitud,
    altitud
)
FROM '/docker-entrypoint-initdb.d/presas.csv'  -- Asegúrate de que el archivo CSV esté en este directorio
WITH (
    FORMAT csv,
    HEADER true,  -- Si el archivo CSV tiene una fila de encabezado
    DELIMITER ',',
    QUOTE '"',
    ESCAPE '"'
);

-- Cargar los datos en la tabla 'almacenamiento' desde el archivo CSV correspondiente
COPY almacenamiento (
    clave_presa,
    fecha,
    nivel_agua
)
FROM '/docker-entrypoint-initdb.d/almacenamiento.csv'  -- Asegúrate de que el archivo CSV esté en este directorio
WITH (
    FORMAT csv,
    HEADER true,  -- Si el archivo CSV tiene una fila de encabezado
    DELIMITER ',',
    QUOTE '"',
    ESCAPE '"'
);

-- Cargar los datos en la tabla 'clima' desde el archivo CSV correspondiente
COPY clima (
    clave_presa,
    fecha,
    temperatura,
    precipitacion,
    temperatura_max,
    temperatura_min,
    rango_temperatura,
    velocidad_viento,
    presion,
    dia_con_precipitacion
)
FROM '/docker-entrypoint-initdb.d/datos_con_clima_y_condiciones.csv'  -- Ruta del archivo CSV generado por tu script Python
WITH (
    FORMAT csv,
    HEADER true,  -- Si el archivo CSV tiene una fila de encabezado
    DELIMITER ',',
    QUOTE '"',
    ESCAPE '"'
);
