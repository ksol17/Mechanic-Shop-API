import unittest
from app import create_app
from config import TestingConfig

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()


    # Positive test: create inventory item
    def test_create_inventory_item_success(self):
        payload = {
            "name": "Oil Filter",
            "quantity": 10,
            "price": 15.99
        }
        response = self.client.post('/inventory/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Oil Filter", response.get_data(as_text=True))

    # Negative test: create inventory item with missing required field
    def test_create_inventory_item_missing_field(self):
        payload = {
            "name": "Brake Pad"
            # Missing 'quantity' and 'price'
        }
        response = self.client.post('/inventory/', json=payload)
        self.assertEqual(response.status_code, 400)

    # Positive test: get inventory item by ID
    def test_get_inventory_item_success(self):
        payload = {
            "name": "Spark Plug",
            "quantity": 5,
            "price": 7.99
        }
        create_resp = self.client.post('/inventory/', json=payload)
        item_id = create_resp.get_json().get("id")
        response = self.client.get(f'/inventory/{item_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Spark Plug", response.get_data(as_text=True))

    # Negative tests: get, update, and delete inventory item not found
    def test_get_inventory_item_not_found(self):
        response = self.client.get('/inventory/99999')
        self.assertEqual(response.status_code, 404)

    # Negative test: update inventory item not found
    def test_update_inventory_item_not_found(self):
        payload = {
            "name": "Updated Item",
            "quantity": 20,
            "price": 19.99
        }
        response = self.client.put('/inventory/99999', json=payload)
        self.assertEqual(response.status_code, 404)

    def test_delete_inventory_item_not_found(self):
        response = self.client.delete('/inventory/99999')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
