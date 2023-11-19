#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from googleapiclient.discovery import build
from google.oauth2 import service_account

def configure_google_credentials(credentials_file):
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file,
        scopes=['https://www.googleapis.com/auth/cse']
    )
    return build('customsearch', 'v1', credentials=credentials)

def buscar_tallerista(service, query, num_results=10, country="", region=""):
    cse_id = '94b5a3f9d79d0417b'  # Reemplaza con tu ID de motor de búsqueda personalizado

    query += f" persona en region metropolitana,chile site:linkedin.com"
    query += f" que realize talleres" 

    resultados = service.cse().list(
        q=query,
        cx=cse_id,
        num=num_results
    ).execute()

    return resultados.get('items', [])

def buscar_insumos(service, query, num_results=10, country="", region=""):
    cse_id = '94b5a3f9d79d0417b'  # Reemplaza con tu ID de motor de búsqueda personalizado

    query += f" ofertas y compras de {query} en chile, region metropolitana"

    resultados = service.cse().list(
        q=query,
        cx=cse_id,
        num=num_results
    ).execute()

    return resultados.get('items', [])

