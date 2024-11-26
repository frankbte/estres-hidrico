import os
import requests
from bs4 import BeautifulSoup

# URL del conjunto de datos
url = 'https://datos.sonora.gob.mx/dataset/Recursos%20H%C3%ADdricos'

# Directorio donde se guardarán los archivos descargados
directorio_descargas = 'descargas_recursos_hidricos'
os.makedirs(directorio_descargas, exist_ok=True)

# Obtener el contenido de la página
respuesta = requests.get(url)
respuesta.raise_for_status()

# Parsear el HTML
soup = BeautifulSoup(respuesta.text, 'html.parser')

# Buscar todos los enlaces de descarga
enlaces_descarga = soup.find_all('a', class_='resource-url-analytics')

# Descargar cada archivo
for enlace in enlaces_descarga:
    href = enlace['href']
    nombre_archivo = href.split('/')[-1]  # Obtener el nombre del archivo desde la URL
    ruta_archivo = os.path.join(directorio_descargas, nombre_archivo)
    
    print(f'Descargando {nombre_archivo}...')
    respuesta_archivo = requests.get(href)
    respuesta_archivo.raise_for_status()
    
    # Guardar el archivo
    with open(ruta_archivo, 'wb') as archivo:
        archivo.write(respuesta_archivo.content)
    print(f'{nombre_archivo} guardado en {ruta_archivo}')

print("Descarga completa.")
