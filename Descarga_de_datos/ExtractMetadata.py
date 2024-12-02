import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Ruta al directorio de metadatos
metadata_dir = "Metadatos"

# Crear el directorio si no existe
if not os.path.exists(metadata_dir):
    os.makedirs(metadata_dir)
    print(f"Directorio '{metadata_dir}' creado.")
else:
    print(f"Directorio '{metadata_dir}' ya existe.")

# Leer el archivo CSV con los enlaces y títulos
csv_file = "links_y_titulos.csv"
if not os.path.exists(csv_file):
    print(f"El archivo '{csv_file}' no existe. Asegúrate de generarlo antes de ejecutar este script.")
    exit()

# Leer el archivo CSV
df = pd.read_csv(csv_file)
print(f"Archivo '{csv_file}' leído correctamente.")

# Procesar cada enlace en el archivo
for index, row in df.iterrows():
    titulo = row['Titulo']
    enlace = row['Enlace']

    # Descargar el código fuente de la página
    print(f"Accediendo al enlace: {enlace}")
    response = requests.get(enlace)
    if response.status_code != 200:
        print(f"Error al acceder a {enlace}. Código de estado: {response.status_code}")
        continue

    # Parsear el HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Buscar la sección con clase 'module-content metaBone'
    metadata_section = soup.find('div', class_='module-content metaBone')
    if not metadata_section:
        print(f"No se encontró la sección 'Metadatos' en {enlace}.")
        continue

    # Buscar la tabla asociada en esta sección
    table = metadata_section.find('table')
    if not table:
        print(f"No se encontró una tabla en la sección 'Metadatos' de {enlace}.")
        continue

    # Extraer los datos de la tabla en formato clave-valor
    metadata = {}
    rows = table.find_all('tr')
    for row in rows:
        # Tomar las celdas <th> (clave) y <td> (valor)
        cols = row.find_all('th') + row.find_all('td')
        if len(cols) >= 2:  # Debe haber al menos dos columnas (clave y valor)
            key = cols[0].text.strip()
            value = cols[1].text.strip() if len(cols) > 1 else ""
            metadata[key] = value

    # Guardar los metadatos en un archivo CSV
    metadata_file = os.path.join(metadata_dir, f"{titulo.replace(' ', '_')}_metadatos.csv")
    metadata_df = pd.DataFrame(list(metadata.items()), columns=["Campo", "Valor"])
    metadata_df.to_csv(metadata_file, index=False)
    print(f"Metadatos extraídos y guardados en '{metadata_file}'.")

print("\nExtracción de metadatos completada.")
