import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

# URLs y directorios
url_principal = 'https://datos.sonora.gob.mx/dataset/Recursos%20H%C3%ADdricos'
directorio_descargas = 'descargas_recursos_hidricos'
directorio_metadatos = 'Metadatos'

# Asegurarse de que los directorios existen
os.makedirs(directorio_descargas, exist_ok=True)
os.makedirs(directorio_metadatos, exist_ok=True)

def obtener_metadatos(url_detalle):
    """Extraer metadatos de la página específica del archivo."""
    respuesta = requests.get(url_detalle)
    respuesta.raise_for_status()
    soup = BeautifulSoup(respuesta.text, 'html.parser')

    # Buscar la tabla en la sección 'module-content metaBone'
    metadatos = {}
    metadata_section = soup.find('div', class_='module-content metaBone')
    if metadata_section:
        tabla_metadatos = metadata_section.find('table')
        if tabla_metadatos:
            filas = tabla_metadatos.find_all('tr')
            for fila in filas:
                celdas = fila.find_all(['th', 'td'])
                if len(celdas) == 2:  # Deben ser clave y valor
                    clave = celdas[0].text.strip()
                    valor = celdas[1].text.strip()
                    metadatos[clave] = valor
    return metadatos

def cargar_metadatos_csv(nombre_archivo):
    """Cargar metadatos desde un archivo CSV."""
    ruta_metadatos = os.path.join(directorio_metadatos, f'{nombre_archivo}.csv')
    if os.path.exists(ruta_metadatos):
        df = pd.read_csv(ruta_metadatos)
        return dict(zip(df['Campo'], df['Valor']))
    return None

def guardar_metadatos_csv(nombre_archivo, metadatos):
    """Guardar metadatos en un archivo CSV."""
    ruta_metadatos = os.path.join(directorio_metadatos, f'{nombre_archivo}.csv')
    df = pd.DataFrame(list(metadatos.items()), columns=['Campo', 'Valor'])
    df.to_csv(ruta_metadatos, index=False)

def descargar_archivo(href_descarga, ruta_archivo):
    """Descargar un archivo desde un enlace y guardarlo."""
    respuesta_archivo = requests.get(href_descarga)
    respuesta_archivo.raise_for_status()
    with open(ruta_archivo, 'wb') as archivo:
        archivo.write(respuesta_archivo.content)
    print(f'Archivo descargado y guardado en: {ruta_archivo}')

# Obtener la página principal
respuesta = requests.get(url_principal)
respuesta.raise_for_status()
soup = BeautifulSoup(respuesta.text, 'html.parser')

# Buscar todos los elementos con la clase 'resource-item'
recursos = soup.find_all('li', class_='resource-item')
archivos_descargados = []

for recurso in recursos:
    enlace_detalle = recurso.find('a', class_='heading', href=True)
    if not enlace_detalle:
        continue

    url_detalle = f"https://datos.sonora.gob.mx{enlace_detalle['href']}"
    nombre_archivo = enlace_detalle.text.strip().replace(' ', '_')  # Nombre del recurso

    # Obtener los metadatos de la página de detalles
    print(f'Obteniendo metadatos de {url_detalle}...')
    metadatos_nuevos = obtener_metadatos(url_detalle)

    # Cargar metadatos existentes desde CSV
    metadatos_existentes = cargar_metadatos_csv(nombre_archivo)

    # Verificar si los metadatos han cambiado
    if not metadatos_existentes or metadatos_nuevos.get('Ãšltima actualizaciÃ³n de los datos') != metadatos_existentes.get('Ãšltima actualizaciÃ³n de los datos'):
        print(f'Metadatos actualizados o inexistentes para {nombre_archivo}. Descargando archivo...')

        # Obtener el enlace de descarga
        enlace_descarga = recurso.find('a', class_='resource-url-analytics', href=True)
        if enlace_descarga:
            href_descarga = enlace_descarga['href']
            ruta_archivo = os.path.join(directorio_descargas, f'{nombre_archivo}.xlsx')

            # Descargar el archivo
            descargar_archivo(href_descarga, ruta_archivo)
            archivos_descargados.append(nombre_archivo)

        # Guardar los nuevos metadatos en CSV
        guardar_metadatos_csv(nombre_archivo, metadatos_nuevos)
    else:
        print(f'Metadatos sin cambios para {nombre_archivo}. No se descarga el archivo.')

# Resumen final
if archivos_descargados:
    print("\nArchivos actualizados:")
    for archivo in archivos_descargados:
        print(f"- {archivo}.xlsx")
else:
    print("\nNo hay archivos nuevos o actualizados para descargar.")

print("Proceso completado.")
