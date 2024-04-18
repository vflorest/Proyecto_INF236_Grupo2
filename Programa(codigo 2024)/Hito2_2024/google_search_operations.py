#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from googleapiclient.discovery import build
from google.oauth2 import service_account

def configure_google_credentials(credentials_file):
    return service_account.Credentials.from_service_account_file(
        'zeta-dock-403001-016ee9fa4a6f.json',
        scopes=['https://www.googleapis.com/auth/cse']
    )


def buscar_tallerista(query, num_results=10, country="", region=""):
    cse_id = '94b5a3f9d79d0417b'  # ID del motor de búsqueda personalizado de Google

    query += f" persona en region metropolitana,chile site:linkedin.com"
    query += f" que realize talleres" 

    # Crear una nueva instancia de la búsqueda personalizada
    service = build('customsearch', 'v1', credentials=configure_google_credentials('tu_archivo_credenciales.json'))

    resultados = service.cse().list(
        q=query,
        cx=cse_id,
        num=num_results
    ).execute()

    return resultados.get('items', [])

def buscar_insumos(query, num_results=10, country="", region=""):
    cse_id = '94b5a3f9d79d0417b'  # ID del motor de búsqueda personalizado de Google

    query += f" ofertas y compras de {query} en chile, region metropolitana"

    # Crear una nueva instancia de la búsqueda personalizada
    service = build('customsearch', 'v1', credentials=configure_google_credentials('tu_archivo_credenciales.json'))

    resultados = service.cse().list(
        q=query,
        cx=cse_id,
        num=num_results
    ).execute()

    return resultados.get('items', [])

