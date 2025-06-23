import unittest
from sqlalchemy import text
from app import create_app
from config import TestingConfig

class TestMechanics(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            from app import db
            db.create_all()
            db.session.execute(text("DELETE FROM mechanic_ticket"))
            db.session.execute(text("DELETE FROM service_tickets"))
            db.session.execute(text("DELETE FROM mechanics"))
            db.session.execute(text("DELETE FROM customers"))
            db.session.commit()

    def test_create_mechanic_success(self):
        payload = {
            "name": "Test Mechanic",
            "email": "mechanic@example.com"
        }
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Test Mechanic", response.get_data(as_text=True))


    # Negative test: create mechanic with missing required field
    def test_create_mechanic_missing_field(self):
        payload = {
            "name": "Jane Doe"
            # Missing 'email', 'password', and 'phone'
        }
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 400)


    # Positive test: get mechanic 
    def test_get_mechanic_success(self):
        # First, create a mechanic
        payload = {
            "name": "Test Mechanic",
            "email": "getmechanic@example.com"
           
        }
        create_resp = self.client.post('/mechanics/', json=payload)
        mechanic_id = create_resp.get_json().get("id")
        # Now, get the mechanic
        response = self.client.get(f'/mechanics/{mechanic_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Mechanic", response.get_data(as_text=True))

    # Negative tests: get, update, and delete mechanic not found
    def test_get_mechanic_not_found(self):
        response = self.client.get('/mechanics/99999')
        self.assertEqual(response.status_code, 404)

    # Negative test: update mechanic not found
    def test_update_mechanic_not_found(self):
        payload = {
            "id": "100",
            "name": "John Doe"
        }
        response = self.client.put('/mechanics/99999', json=payload)
        self.assertEqual(response.status_code, 404)

    # Negative test: delete mechanic not found
    def test_delete_mechanic_not_found(self):
        response = self.client.delete('/mechanics/99999')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
