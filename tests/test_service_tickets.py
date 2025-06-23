import unittest
from app import create_app
from config import TestingConfig
from sqlalchemy import text

class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            from app import db
            db.create_all()
            # Clear tables for a clean test environment
            db.session.execute(text("DELETE FROM mechanic_ticket"))
            db.session.execute(text("DELETE FROM service_tickets"))
            db.session.execute(text("DELETE FROM mechanics"))
            db.session.execute(text("DELETE FROM customers"))
            db.session.commit()
            # Create a customer and a mechanic for the tests
            cust_resp = self.client.post('/customers/', json={
                "name": "Test Customer",
                "email": "customer@example.com",
                "phone": "1234567890",
                "password": "password123"
            })
            mech_resp = self.client.post('/mechanics/', json={
                "name": "Test Mechanic",
                "email": "mechanic@example.com"
            })
            self.customer_id = cust_resp.get_json().get("id")
            self.mechanic_id= mech_resp.get_json().get("id")

    def test_create_service_ticket_success(self):
        payload = {
            "customer_id": self.customer_id,
            "mechanic_ids": [self.mechanic_id],
            "description": "Oil change",
            "status": "open"
        }
        response = self.client.post('/service_tickets/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Oil change", response.get_data(as_text=True))



    def test_get_service_ticket_success(self):
        # First, create a ticket
        payload = {
            "customer_id": self.customer_id,
            "mechanic_ids": [self.mechanic_id],
            "description": "Brake repair",
            "status": "open"
        }
        create_resp = self.client.post('/service_tickets/', json=payload)
        ticket_id = create_resp.get_json().get("id")
        response = self.client.get(f'/service_tickets/{ticket_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Brake repair", response.get_data(as_text=True))

    def test_get_service_ticket_not_found(self):
        response = self.client.get('/service_tickets/99999')
        self.assertEqual(response.status_code, 404)

    def test_update_service_ticket_success(self):
        # Create a ticket
        payload = {
            "customer_id": self.customer_id,
            "mechanic_ids": [self.mechanic_id],
            "description": "Tire rotation",
            "status": "open"
        }
        create_resp = self.client.post('/service_tickets/', json=payload)
        ticket_id = create_resp.get_json().get("id")
        update_payload = {
            "description": "Tire rotation and balance",
            "status": "closed",
            "customer_id": self.customer_id
        }
        response = self.client.put(f'/service_tickets/{ticket_id}', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Tire rotation and balance", response.get_data(as_text=True))

    def test_update_service_ticket_not_found(self):
        update_payload = {
            "description": "Updated description",
            "status": "closed",
            "customer_id": self.customer_id}
        
        response = self.client.put('/service_tickets/99999', json=update_payload)
        self.assertEqual(response.status_code, 404)

    def test_delete_service_ticket_success(self):
        # Create a ticket
        payload = {
            "customer_id": self.customer_id,
            "mechanic_ids": [self.mechanic_id],
            "description": "Alignment",
            "status": "open"
        }
        create_resp = self.client.post('/service_tickets/', json=payload)
        print("Create Response:", create_resp.get_json())
        ticket_id = create_resp.get_json().get("id")
        response = self.client.delete(f'/service_tickets/{ticket_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("deleted successfully", response.get_data(as_text=True))

    def test_delete_service_ticket_not_found(self):
        response = self.client.delete('/service_tickets/99999')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()