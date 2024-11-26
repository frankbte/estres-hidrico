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

-- Crear la tabla 'datos_clima' para almacenar la información del clima
CREATE TABLE IF NOT EXISTS datos_clima (
    id_clima SERIAL PRIMARY KEY,
    clave_clima VARCHAR(10) REFERENCES presas(clave_presa),
    fecha_lectura DATE NOT NULL,
    almacenamiento DECIMAL(10, 2),
    temp DECIMAL(5, 2),
    humidity DECIMAL(5, 2),
    precip DECIMAL(5, 2),
    preciptype INTEGER,
    uvindex DECIMAL(5, 2),
    conditions_Clear DECIMAL(5, 2),
    conditions_Overcast DECIMAL(5, 2),
    conditions_Partially_cloudy DECIMAL(5, 2),
    conditions_Rain DECIMAL(5, 2),
    conditions_Rain_Overcast DECIMAL(5, 2),
    conditions_Rain_Partially_cloudy DECIMAL(5, 2)
);

-- Crear la tabla 'almacenamiento'
CREATE TABLE IF NOT EXISTS almacenamiento (
    id_almacenamiento SERIAL PRIMARY KEY,
    clave_presa VARCHAR(10) REFERENCES presas(clave_presa),
    fecha DATE NOT NULL,
    nivel_agua DECIMAL(10, 2)
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

-- Cargar los datos en la tabla 'datos_clima' desde el archivo CSV correspondiente
COPY datos_clima (
    clave_clima,
    fecha_lectura,
    almacenamiento,
    temp,
    humidity,
    precip,
    preciptype,
    uvindex,
    conditions_Clear,
    conditions_Overcast,
    conditions_Partially_cloudy,
    conditions_Rain,
    conditions_Rain_Overcast,
    conditions_Rain_Partially_cloudy
)
FROM '/docker-entrypoint-initdb.d/datos_clima.csv'  -- Asegúrate de que el archivo CSV esté en este directorio
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


