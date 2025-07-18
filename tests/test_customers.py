import unittest
from app import create_app
from config import TestingConfig

class TestCustomers(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            from app import db
            db.drop_all()
            db.create_all()

    # Positive test: create customer
    def test_create_customer_success(self):
        payload = {
            "name": "Test Customer",
            "email": "test@email.com",
            "phone": "1234567890",
            "password": "123"
        }
        response = self.client.post('/customers/', json=payload)
        print("Create customer response:", response.status_code, response.get_json())
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertIn("id", data)
        self.assertEqual(data["name"], "Test Customer")
        self.assertEqual(data["email"], "test@email.com")
        self.assertEqual(data["phone"], "1234567890")
        self.assertNotIn("password", data)  # Password should not be returned
        
    # Negative test: create customer with missing required field
    def test_create_customer_missing_field(self):
        payload = {
            "name": "Bob"
        }
        response = self.client.post('/customers/', json=payload)
        print("Missing field response:", response.status_code, response.get_json())
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Missing required fields")

    # Negative test: get non-existent customer
    def test_get_customer_not_found(self):
        response = self.client.get('/customers/99999')
        print("Get non-existent customer response:", response.status_code, response.get_json())
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Customer not found")



if __name__ == '__main__':
    unittest.main()
# This code is a unit test for the customers blueprint in a Flask application.
# It tests the creation of a customer and checks for proper error handling when required fields are missing.
# It also checks the response when trying to retrieve a customer that does not exist.
