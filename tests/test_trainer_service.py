import unittest
from unittest.mock import patch, MagicMock
from microservices.trainer_service.app import app

class TrainerServiceTestCase(unittest.TestCase):
    # Set up the test client
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    @patch('microservices.trainer_service.app.trainers_table.scan')
    def test_get_trainers_success(self, mock_scan):
        # Mock DynamoDB response for scan
        mock_scan.return_value = {
            'Items': [
                {'trainer_id': 1, 'name': 'John Doe', 'preferred_cities': ['New York'], 'skill_areas': ['Python', 'Java']},
                {'trainer_id': 2, 'name': 'Jane Smith', 'preferred_cities': ['London'], 'skill_areas': ['Data Science']}
            ]
        }

        # Make GET request to /trainers
        response = self.app.get('/trainers')

        # Assert the response status and data
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)
        self.assertIn(b'Jane Smith', response.data)

    # @patch('microservices.trainer_service.app.trainers_table.scan')
    # def test_get_trainers_error(self, mock_scan):
    #     # Mock DynamoDB ClientError
    #     mock_scan.side_effect = Exception('Error retrieving trainers')

    #     # Make GET request to /trainers
    #     response = self.app.get('/trainers')

    #     # Assert the response status and error message
    #     self.assertEqual(response.status_code, 500)
    #     self.assertIn(b'Error retrieving trainers', response.data)

    @patch('microservices.trainer_service.app.trainers_table.get_item')
    def test_get_trainer_success(self, mock_get_item):
        # Mock DynamoDB response for get_item
        mock_get_item.return_value = {
            'Item': {
                'trainer_id': 1,
                'name': 'John Doe',
                'preferred_cities': ['New York'],
                'skill_areas': ['Python', 'Java']
            }
        }

        # Make GET request to /trainers/1
        response = self.app.get('/trainers/1')

        # Assert the response status and data
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)

    @patch('microservices.trainer_service.app.trainers_table.get_item')
    def test_get_trainer_not_found(self, mock_get_item):
        # Mock DynamoDB response for get_item with no item
        mock_get_item.return_value = {}

        # Make GET request to /trainers/1
        response = self.app.get('/trainers/1')

        # Assert the response status and error message
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Trainer not found', response.data)

    @patch('microservices.trainer_service.app.trainers_table.put_item')
    @patch('microservices.trainer_service.app.trainers_table.scan')
    def test_register_trainer_success(self, mock_scan, mock_put_item):
        # Mock DynamoDB scan response to generate trainer ID
        mock_scan.return_value = {
            'Items': [{'trainer_id': 1}, {'trainer_id': 2}]
        }

        # Mock successful put_item
        mock_put_item.return_value = {}

        # Prepare data for POST request
        data = {
            'name': 'John Doe',
            'preferred_cities': ['New York'],
            'skills': ['Python', 'Java']
        }

        # Make POST request to /trainers
        response = self.app.post('/trainers', json=data)

        # Assert the response status and data
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Trainer registered successfully', response.data)

    @patch('microservices.trainer_service.app.trainers_table.put_item')
    @patch('microservices.trainer_service.app.trainers_table.scan')
    def test_register_trainer_missing_data(self, mock_scan, mock_put_item):
        # Prepare incomplete data for POST request
        data = {
            'name': 'John Doe'
            # 'skills' is missing
        }

        # Make POST request to /trainers
        response = self.app.post('/trainers', json=data)

        # Assert the response status and error message
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Name and skill areas are required', response.data)

    @patch('microservices.trainer_service.app.trainers_table.delete_item')
    def test_delete_trainer_success(self, mock_delete_item):
        # Mock successful delete_item
        mock_delete_item.return_value = {}

        # Make DELETE request to /trainers/1
        response = self.app.delete('/trainers/1')

        # Assert the response status and success message
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'trainer deleted successfully', response.data)

    # @patch('microservices.trainer_service.app.trainers_table.delete_item')
    # def test_delete_trainer_error(self, mock_delete_item):
    #     # Mock DynamoDB ClientError
    #     mock_delete_item.side_effect = Exception('Error deleting trainer')

    #     # Make DELETE request to /trainers/1
    #     response = self.app.delete('/trainers/1')

    #     # Assert the response status and error message
    #     self.assertEqual(response.status_code, 500)
    #     self.assertIn(b'Error deleting trainer', response.data)

if __name__ == '__main__':
    unittest.main()
