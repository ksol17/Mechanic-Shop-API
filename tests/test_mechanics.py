import unittest
from app import create_app
from flask import json

class TestMechanics(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')  # ensure your app supports config modes
        self.client = self.app.test_client()

    def test_create_mechanic_success(self):
        payload = {
            "name": "John Doe",
            "specialization": "Brakes"
        }
        response = self.client.post('/mechanics', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("John Doe", response.get_data(as_text=True))

    def test_create_mechanic_missing_field(self):
        payload = {
            "name": "Jane Doe"
            # Missing 'specialization'
        }
        response = self.client.post('/mechanics', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_get_mechanic_not_found(self):
        response = self.client.get('/mechanics/99999')
        self.assertEqual(response.status_code, 404)
