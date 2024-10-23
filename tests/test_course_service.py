import unittest
from unittest.mock import patch, MagicMock
from flask import json
from microservices.course_service.app import app

class CourseServiceTestCase(unittest.TestCase):

    def setUp(self):
        # Set up Flask test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('course_service.app.courses_table')
    def test_create_course(self, mock_courses_table):
        # Mock DynamoDB scan response
        mock_courses_table.scan.return_value = {'Items': []}

        # Data to send in POST request
        course_data = {
            'name': 'Python Basics',
            'duration': '4 weeks',
            'skills': ['Python', 'Programming'],
            'price': '199'
        }

        # Simulate POST request to create a course
        response = self.app.post('/courses', data=json.dumps(course_data), content_type='application/json')

        # Check if the response is correct
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Course created', response.data)

        # Check if put_item was called with the correct arguments
        mock_courses_table.put_item.assert_called_once()

    @patch('course_service.app.courses_table')
    def test_create_course_missing_fields(self, mock_courses_table):
        # Data with missing 'price'
        course_data = {
            'name': 'Python Basics',
            'duration': '4 weeks',
            'skills': ['Python', 'Programming']
        }

        # Simulate POST request with missing fields
        response = self.app.post('/courses', data=json.dumps(course_data), content_type='application/json')

        # Check if the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Name, duration, skills, and price are required', response.data)

        # Ensure put_item was never called
        mock_courses_table.put_item.assert_not_called()

    @patch('course_service.app.courses_table')
    def test_get_courses(self, mock_courses_table):
        # Mock DynamoDB scan response
        mock_courses_table.scan.return_value = {
            'Items': [
                {'course_id': 1, 'name': 'Python Basics', 'duration': '4 weeks', 'skills': ['Python'], 'price': '199'}
            ]
        }

        # Simulate GET request to retrieve all courses
        response = self.app.get('/courses')

        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Python Basics', response.data)

    @patch('course_service.app.courses_table')
    def test_get_course(self, mock_courses_table):
        # Mock DynamoDB get_item response
        mock_courses_table.get_item.return_value = {
            'Item': {'course_id': 1, 'name': 'Python Basics', 'duration': '4 weeks', 'skills': ['Python'], 'price': '199'}
        }

        # Simulate GET request for a specific course
        response = self.app.get('/courses/1')

        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Python Basics', response.data)

    @patch('course_service.app.courses_table')
    def test_get_course_not_found(self, mock_courses_table):
        # Mock DynamoDB get_item response with no course found
        mock_courses_table.get_item.return_value = {}

        # Simulate GET request for a non-existing course
        response = self.app.get('/courses/99')

        # Check if the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Course not found', response.data)

    @patch('course_service.app.courses_table')
    def test_delete_course(self, mock_courses_table):
        # Mock successful delete response
        mock_courses_table.delete_item.return_value = {}

        # Simulate DELETE request
        response = self.app.delete('/courses/1')

        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Course deleted successfully', response.data)

        # Check if delete_item was called with the correct arguments
        mock_courses_table.delete_item.assert_called_once_with(Key={'course_id': 1})

    @patch('course_service.app.courses_table')
    def test_delete_course_error(self, mock_courses_table):
        # Mock an error during deletion
        mock_courses_table.delete_item.side_effect = Exception('DynamoDB error')

        # Simulate DELETE request for a non-existing course
        response = self.app.delete('/courses/99')

        # Check if the response is correct
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Error deleting course', response.data)

if __name__ == '__main__':
    unittest.main()
