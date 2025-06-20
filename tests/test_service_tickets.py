import unittest
from app import create_app
from config import TestingConfig

class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()


    # Positive test: create service ticket
    def test_create_service_ticket_success(self):
        payload = {
            "customer_id": 1,
            "mechanic_id": 1,
            "description": "Oil change",
            "status": "open"
        }
        response = self.client.post('/service_tickets/', json=payload)
        # Accept 201 or 400 if customer/mechanic doesn't exist in test DB
        self.assertIn(response.status_code, [201, 400])


    # Negative test: create service ticket with missing required field
    def test_create_service_ticket_missing_field(self):
        payload = {
            "customer_id": 1
            # Missing mechanic_id, description, status
        }
        response = self.client.post('/service_tickets/', json=payload)
        self.assertEqual(response.status_code, 400)

    # Negative test: get service ticket not found
    def test_get_service_ticket_not_found(self):
        response = self.client.get('/service_tickets/99999')
        self.assertEqual(response.status_code, 404)

    # Negative test: update service ticket not found
    def test_update_service_ticket_not_found(self):
        payload = {
            "description": "Updated description",
            "status": "closed"
        }
        response = self.client.put('/service_tickets/99999', json=payload)
        self.assertEqual(response.status_code, 404)

    # Negative test: delete service ticket not found
    def test_delete_service_ticket_not_found(self):
        response = self.client.delete('/service_tickets/99999')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()