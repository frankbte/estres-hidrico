import re
import pandas as pd

# Función para extraer títulos y enlaces desde un archivo
def extract_links_and_titles(file_path, base_url):
    # Leer el contenido del archivo
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Usar expresiones regulares para extraer los enlaces y los títulos
    pattern = r'<a class="heading" href=["\'](.*?)["\'].*?title=["\'](.*?)["\']'
    matches = re.findall(pattern, html_content)  # Extraer todas las coincidencias

    # Completar los enlaces relativos y emparejarlos con los títulos
    datasets = [{"Enlace": base_url + link, "Titulo": title} for link, title in matches]

    return datasets

# Ruta al archivo guardado
file_path = "pagina_completa.txt"
base_url = "https://datos.sonora.gob.mx"  # Parte que falta antes de '/dataset'

# Extraer los títulos y enlaces desde el archivo
datasets = extract_links_and_titles(file_path, base_url)

# Mostrar los títulos y enlaces encontrados
print("\nTítulos y enlaces encontrados:")
for idx, dataset in enumerate(datasets, start=1):
    print(f"{idx}. {dataset['Titulo']}: {dataset['Enlace']}")

# Guardar los títulos y enlaces en un archivo CSV
df = pd.DataFrame(datasets)
df.to_csv("links_y_titulos.csv", index=False)
print("\nLos títulos y enlaces han sido guardados en 'links_y_titulos.csv'.")
