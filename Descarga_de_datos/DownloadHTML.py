import requests

# URL de la página principal donde se listan los datasets
main_url = "https://datos.sonora.gob.mx/dataset/Recursos%20H%C3%ADdricos"

# Archivo donde se guardará el HTML descargado
file_path = "pagina_completa.txt"

# Descargar el HTML desde la URL y guardarlo en un archivo
response = requests.get(main_url)
response.raise_for_status()  # Verificar si la solicitud fue exitosa

# Guardar el contenido del HTML en un archivo .txt
with open(file_path, "w", encoding="utf-8") as file:
    file.write(response.text)

print(f"HTML descargado y guardado en {file_path}.")
