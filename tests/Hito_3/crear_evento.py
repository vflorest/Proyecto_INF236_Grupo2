import unittest
import requests

class TestCrearEvento(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Realizar configuraciones previas a todas las pruebas de la clase
        cls.url = 'http://localhost:5000/crear_evento'
        cls.datos_evento_validos = {
            "titulo_evento": "Taller de Python Avanzado",
            "descripcion_evento": "Aprende sobre programación avanzada en Python.",
            "vacantes": 20,
            "sesiones": 3,
            "modalidad": 2,  
            "experiencia_tallerista": "Experiencia del tallerista aquí",
            "instagram": "instagram_user",
            "tiktok": "tiktok_user"
        }
        cls.evento_creado_id = None  # ID del evento creado durante las pruebas

        cls.datos_evento_faltantes = {
            "descripcion_evento": "Aprende sobre programación avanzada en Python.",
            "vacantes": 20,
            "sesiones": 3,
            "modalidad": 2,  
            "experiencia_tallerista": "Experiencia del tallerista aquí",
            "instagram": "instagram_user",
            "tiktok": "tiktok_user"
        }

    @classmethod
    def tearDownClass(cls):
        # Limpiar datos después de todas las pruebas de la clase
        if cls.evento_creado_id:
            # Eliminar el evento creado durante las pruebas
            response = requests.delete(f'http://localhost:5000/evento/{cls.evento_creado_id}')
            print("Evento eliminado después de las pruebas.")

    def test_crear_evento_exitoso(self):
        response = requests.post(self.url, json=self.datos_evento_validos)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Evento creado correctamente.', response.json()['message'])
        

    def test_crear_evento_faltan_datos(self):
        response = requests.post(self.url, json=self.datos_evento_faltantes)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
