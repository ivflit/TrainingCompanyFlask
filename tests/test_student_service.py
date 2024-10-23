import unittest
from unittest.mock import patch, MagicMock
from flask import json
from microservices.student_service.app import app

class StudentServiceTestCase(unittest.TestCase):

    def setUp(self):
        # Set up Flask test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('student_service.app.students_table')
    def test_register_student(self, mock_students_table):
        # Mock DynamoDB scan response
        mock_students_table.scan.return_value = {'Items': []}

        # Data to send in POST request
        student_data = {
            'name': 'John Doe',
            'age': 25,
            'company': 'Tech Co',
            'level': 'Intermediate',
            'stream': 'Engineering'
        }

        # Simulate POST request to register a student
        response = self.app.post('/students', data=json.dumps(student_data), content_type='application/json')

        # Check if the response is correct
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'student created', response.data)

        # Check if put_item was called with the correct arguments
        mock_students_table.put_item.assert_called_once()

    @patch('student_service.app.students_table')
    def test_register_student_missing_fields(self, mock_students_table):
        # Data with missing 'company'
        student_data = {
            'name': 'John Doe',
            'age': 25,
            'level': 'Intermediate',
            'stream': 'Engineering'
        }

        # Simulate POST request with missing fields
        response = self.app.post('/students', data=json.dumps(student_data), content_type='application/json')

        # Check if the response is correct
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Name, age, company, and level , stream are required', response.data)

        # Ensure put_item was never called
        mock_students_table.put_item.assert_not_called()

    @patch('student_service.app.students_table')
    def test_get_students(self, mock_students_table):
        # Mock DynamoDB scan response
        mock_students_table.scan.return_value = {
            'Items': [
                {'student_id': 1, 'name': 'John Doe', 'age': 25, 'company': 'Tech Co', 'level': 'Intermediate', 'stream': 'Engineering'}
            ]
        }

        # Simulate GET request to retrieve all students
        response = self.app.get('/students')

        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)

    @patch('student_service.app.students_table')
    def test_get_student(self, mock_students_table):
        # Mock DynamoDB get_item response
        mock_students_table.get_item.return_value = {
            'Item': {'student_id': 1, 'name': 'John Doe', 'age': 25, 'company': 'Tech Co', 'level': 'Intermediate', 'stream': 'Engineering'}
        }

        # Simulate GET request for a specific student
        response = self.app.get('/students/1')

        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)

    @patch('student_service.app.students_table')
    def test_get_student_not_found(self, mock_students_table):
        # Mock DynamoDB get_item response with no student found
        mock_students_table.get_item.return_value = {}

        # Simulate GET request for a non-existing student
        response = self.app.get('/students/99')

        # Check if the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'student not found', response.data)

    @patch('student_service.app.students_table')
    def test_delete_student(self, mock_students_table):
        # Mock successful delete response
        mock_students_table.delete_item.return_value = {}

        # Simulate DELETE request
        response = self.app.delete('/students/1')

        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'student deleted successfully', response.data)

        # Check if delete_item was called with the correct arguments
        mock_students_table.delete_item.assert_called_once_with(Key={'student_id': 1})

    @patch('student_service.app.students_table')
    def test_delete_student_error(self, mock_students_table):
        # Mock an error during deletion
        mock_students_table.delete_item.side_effect = Exception('DynamoDB error')

        # Simulate DELETE request for a non-existing student
        response = self.app.delete('/students/99')

        # Check if the response is correct
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Error deleting student', response.data)

    @patch('student_service.app.requests.post')
    def test_book_course(self, mock_post):
        # Mock the external booking service response
        mock_post.return_value.status_code = 201

        # Data to send in POST request
        booking_data = {'course_id': 101, 'date': '2024-01-01'}

        # Simulate POST request to book a course for the student
        response = self.app.post('/students/1/book', data=json.dumps(booking_data), content_type='application/json')

        # Check if the response is correct
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Course booked successfully', response.data)

        # Check if the external booking service was called with the correct arguments
        mock_post.assert_called_once_with('http://booking_service:8003/bookings', json={
            'student_id': 1,
            'course_id': 101,
            'date': '2024-01-01'
        })

    @patch('student_service.app.requests.post')
    def test_book_course_failure(self, mock_post):
        # Mock the external booking service response for failure
        mock_post.return_value.status_code = 404

        # Data to send in POST request
        booking_data = {'course_id': 101, 'date': '2024-01-01'}

        # Simulate POST request to book a course for the student
        response = self.app.post('/students/1/book', data=json.dumps(booking_data), content_type='application/json')

        # Check if the response is correct
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Course not found or fully booked', response.data)

if __name__ == '__main__':
    unittest.main()
