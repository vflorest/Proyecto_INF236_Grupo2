import unittest
import requests
from api import app

class TestAPIEndpoints(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.base_url = 'http://localhost:5000'  # URL base de la API Flask
        self.valid_api_key = "poner aqui api key"
        self.invalid_api_key = "poner cualquier cosa"

    @classmethod
    def tearDown(cls):
        del cls.valid_api_key
        del cls.invalid_api_key

    #caso de prueba para api key válida
    def test_openai_key_valid(self):
        with app.test_client() as client:
            # Realizar una solicitud POST al endpoint '/configure_openai_key' con la clave de OpenAI
            response = client.post('/configure_openai_key', json={'api_key': self.valid_api_key})

            # Verificar si la solicitud fue exitosa (código de estado 200)
            self.assertEqual(response.status_code, 200)

            # Verificar si la respuesta contiene el mensaje esperado
            data = response.json
            self.assertEqual(data['message'], 'OpenAI API Key configured successfully')

        payload = {'api_key': self.valid_api_key}
        response = requests.post(f'{self.base_url}/configure_openai_key', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'OpenAI API Key configured successfully')

    #caso de prueba api key inválida
    def test_openai_key_invalid(self):
        with app.test_client() as client:
            # Realizar una solicitud POST al endpoint '/configure_openai_key' con la clave de OpenAI
            response = client.post('/configure_openai_key', json={'api_key': self.invalid_api_key})

            # Verificar si la solicitud falló (código de estado 400)
            self.assertEqual(response.status_code, 400)

            # Verificar si la respuesta contiene el mensaje esperado
            data = response.json
            self.assertIn('error', data)

        payload = {'api_key': self.invalid_api_key}
        response = requests.post(f'{self.base_url}/configure_openai_key', json=payload)
        print(response.json())
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

if __name__ == '__main__':
    unittest.main()
