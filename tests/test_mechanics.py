import unittest
from app import create_app
from config import TestingConfig

class TestMechanics(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            from app import db
            db.drop_all()
            db.create_all()

    def test_create_mechanic_success(self):
        payload = {
            "name": "Test Mechanic",
            "email": "mechanic@example.com"
        }
        response = self.client.post('/mechanics/', json=payload)
        print("Create mechanic response:", response.status_code, response.get_json())
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.get_json())

    def test_create_mechanic_missing_field(self):
        payload = {
            "name": "Jane Doe"
            # Missing 'email'
        }
        response = self.client.post('/mechanics/', json=payload)
        print("Missing field response:", response.status_code, response.get_json())
        self.assertEqual(response.status_code, 400)

    def test_get_mechanic_success(self):
        # First, create a mechanic
        payload = {
            "name": "Test Mechanic",
            "email": "getmechanic@example.com"
        }
        create_resp = self.client.post('/mechanics/', json=payload)
        mechanic_id = create_resp.get_json().get("id")
        response = self.client.get(f'/mechanics/{mechanic_id}')
        print("Get mechanic response:", response.status_code, response.get_json())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Mechanic", response.get_data(as_text=True))

    def test_get_mechanic_not_found(self):
        response = self.client.get('/mechanics/99999')
        print("Get non-existent mechanic response:", response.status_code, response.get_json())
        self.assertEqual(response.status_code, 404)

    def test_update_mechanic_not_found(self):
        payload = {
            "name": "John Doe"
        }
        response = self.client.put('/mechanics/99999', json=payload)
        print("Update non-existent mechanic response:", response.status_code, response.get_json())
        self.assertEqual(response.status_code, 404)

    def test_delete_mechanic_not_found(self):
        response = self.client.delete('/mechanics/99999')
        print("Delete non-existent mechanic response:", response.status_code, response.get_json())
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
