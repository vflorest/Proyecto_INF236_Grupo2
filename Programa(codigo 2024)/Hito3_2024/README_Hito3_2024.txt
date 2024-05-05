
Antes de ejecutar, se deben instalar las siguientes librerías:
pip install googlesearch-python
pip install google-auth google-auth-oauthlib
pip install google-api-python-client
pip install openai
pip install tabulate
pip install streamlit
pip install requests
pip install Flask
pip install pandas 
pip install Pillow
pip install psycopg2-binary
pip install python-docx
pip install fpdf





Luego, para ejecutar el código siga los siguientes pasos:
1:Se ingresan datos en config.py
2:Se crea la base de datos con .\crear_bd.py  
3:Abra 2 terminales en el directorio donde esta el código (Hito 6) o navegue hasta el directorio.
4:Levante la api con el siguiente comando en una de las terminales: python .\api.py
5:Ejecute la interfaz de streamlit con el comando en la otra terminal: streamlit run streamlit_interface.py

Con eso ya se puede usar el programa.
