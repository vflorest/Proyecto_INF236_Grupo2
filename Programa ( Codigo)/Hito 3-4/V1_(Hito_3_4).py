#!/usr/bin/env python
# coding: utf-8

# In[3]:


import openai

# Configura tu API key de OpenAI
api_key = "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"

# Función para analizar la descripción y obtener el tipo de tallerista
def obtener_tipo_tallerista(descripcion):
    openai.api_key = api_key

    # Realiza una solicitud a la API de OpenAI para el tipo de tallerista
    respuesta = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Descripción: {descripcion}\nTipo profecion recomendado para el taller ,tiene que estar en singular, solo nombrar la profecion sin nada mas ni espacios:",
        max_tokens=50,  # Ajusta según sea necesario
    )

    # Obtiene el texto de la respuesta
    tipo_tallerista = respuesta.choices[0].text.strip()

    # Filtra para obtener solo la profesión
    tipo_tallerista = tipo_tallerista.split('\n')[0]

    return tipo_tallerista

# Función para obtener los insumos recomendados
def obtener_insumos(descripcion):
    openai.api_key = api_key

    # Realiza una solicitud a la API de OpenAI para los insumos
    respuesta = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Descripción: {descripcion}\n Hasta 10 Insumos recomendados para el taller con su nombre completo , solo nombrarlos sin nada mas y separados por comas, sin ninguna otro tipo de puntuacion:",
        max_tokens=100,  # Ajusta según sea necesario
    )

    # Obtiene el texto de la respuesta
    insumos = respuesta.choices[0].text.strip()

    return insumos

# Solicita la descripción al usuario
descripcion = input("Descripción: ")

# Obtiene el tipo de tallerista
tipo_tallerista = obtener_tipo_tallerista(descripcion)

# Obtiene los insumos recomendados
insumos = obtener_insumos(descripcion)

# Imprime los resultados
print(f"Tipo Tallerista recomendado: {tipo_tallerista}")
print(f"Insumos recomendados: {insumos}")



# In[5]:


from googleapiclient.discovery import build
from google.oauth2 import service_account
from tabulate import tabulate
import datetime

# Configura las credenciales de la API de Google
credentials = service_account.Credentials.from_service_account_file(
    'zeta-dock-403001-016ee9fa4a6f.json',  # Reemplaza con la ruta de tu archivo de credenciales
    scopes=['https://www.googleapis.com/auth/cse']
)

# Crea un servicio de búsqueda personalizada de Google
custom_search_service = build('customsearch', 'v1', credentials=credentials)

def buscar_tallerista(query, num_results=10, country="", region=""):
    # ID del motor de búsqueda personalizado de Google
    cse_id = '94b5a3f9d79d0417b'  # Reemplaza con tu ID de motor de búsqueda personalizado

    # Agrega términos específicos a la consulta y limita la búsqueda a LinkedIn
    query += f" persona en region metropolitana,chile site:linkedin.com"
    query += f" que realize talleres" 

    # Realiza una búsqueda en Google
    resultados = custom_search_service.cse().list(
        q=query,
        cx=cse_id,
        num=num_results  # Número de resultados
    ).execute()

    return resultados.get('items', [])

# Función para realizar una búsqueda de insumos
def buscar_insumos(query, num_results=10, country="", region=""):
    # ID del motor de búsqueda personalizado de Google
    cse_id = '94b5a3f9d79d0417b'  # Reemplaza con tu ID de motor de búsqueda personalizado

    # Agrega "en Chile" o "compra en Chile" a la consulta
    query += f" ofertas y compras de {query} en chile ,reguion metropolitana"

    # Realiza una búsqueda en Google
    resultados = custom_search_service.cse().list(
        q=query,
        cx=cse_id,
        num=num_results  # Número de resultados
    ).execute()

    return resultados.get('items', [])

# País y región para Chile, Región Metropolitana
country = "cl"  # Código del país para Chile
region = "rm"  # Código para la Región Metropolitana

# Realiza una búsqueda para el tipo de tallerista en Chile
resultados_tipo_tallerista = buscar_tallerista(tipo_tallerista, num_results=10, country=country, region=region)

# Establece el ancho fijo de las columnas
column_width = 50

# Mostrar los resultados de tipo de tallerista en una tabla
table = []
for resultado in resultados_tipo_tallerista:
    table.append([resultado['title'][:column_width], resultado['link'][:column_width]])

print("Resultados para el tipo de tallerista en Chile:")
print(tabulate(table, headers=["Descripción", "Link"], tablefmt="fancy_grid"))

# Divide los insumos en una lista
insumos_lista = insumos.split(", ")
resultados_insumos = {}
for insumo in insumos_lista:
    resultados_insumos[insumo] = buscar_insumos(insumo, num_results=10, country=country, region=region)

# Mostrar los resultados de insumos en tablas
for insumo, resultados in resultados_insumos.items():
    table = []
    for resultado in resultados:
        table.append([resultado['title'][:column_width], resultado['link'][:column_width]])
    print(f"\nResultados para {insumo} en Chile:")
    print(tabulate(table, headers=["Descripción", "Link"], tablefmt="fancy_grid"))

# Obtén la fecha y hora actual
now = datetime.datetime.now()

# Crea un nombre de archivo basado en la fecha y hora actual
nombre_archivo = now.strftime("%Y-%m-%d_%H-%M-%S") + "_resultados.txt"

# Abre el archivo en modo de escritura con codificación UTF-8
with open(nombre_archivo, "w", encoding="utf-8") as archivo:
    archivo.write("Resultados para el tipo de tallerista en Chile:\n")
    for resultado in resultados_tipo_tallerista:
        archivo.write(f"{resultado['title'][:column_width]}\t{resultado['link'][:column_width]}\n")

    for insumo, resultados in resultados_insumos.items():
        archivo.write(f"\nResultados para {insumo} en Chile:\n")
        for resultado in resultados:
            archivo.write(f"{resultado['title'][:column_width]}\t{resultado['link'][:column_width]}\n")

print(f"Resultados guardados en el archivo: {nombre_archivo}")


# In[ ]:


input("Presiona Enter para salir...")

