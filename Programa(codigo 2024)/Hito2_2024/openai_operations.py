#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import openai

def configure_api_key(api_key):
    openai.api_key = api_key

def obtener_tipo_tallerista(descripcion):
    # Llama al modelo gpt-3.5-turbo-instruct en lugar de text-davinci-003
    respuesta = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"Descripción: {descripcion}\nTipo profesión recomendado para el taller, tiene que estar en singular, solo nombrar la profesión sin nada más ni espacios:",
        max_tokens=50,
    )

    tipo_tallerista = respuesta.choices[0].text.strip().split('\n')[0]
    return tipo_tallerista

def obtener_insumos(descripcion):
    # Llama al modelo gpt-3.5-turbo-instruct en lugar de text-davinci-003
    respuesta = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"Descripción: {descripcion}\nHasta 10 Insumos recomendados para el taller con su nombre completo, solo nombrarlos sin nada más y separados por comas, sin ninguna otra tipo de puntuación:",
        max_tokens=100,
    )

    insumos = respuesta.choices[0].text.strip()
    return insumos