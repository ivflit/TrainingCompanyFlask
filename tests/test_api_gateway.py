import pytest
from unittest.mock import patch
from flask import session
from api_gateway.app import app

# Helper function to set up test client
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

# Mocking the environment variables
@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch):
    monkeypatch.setenv('SECRET_KEY', 'test_secret')
    monkeypatch.setenv('AUTH_SERVICE_URL', 'http://mock_auth_service')
    monkeypatch.setenv('FRONTEND_SERVICE_URL', 'http://mock_frontend_service')
    monkeypatch.setenv('STUDENT_SERVICE_URL', 'http://mock_student_service')
    monkeypatch.setenv('TRAINER_SERVICE_URL', 'http://mock_trainer_service')
    monkeypatch.setenv('COURSE_SERVICE_URL', 'http://mock_course_service')
    monkeypatch.setenv('BOOKING_SERVICE_URL', 'http://mock_booking_service')
    monkeypatch.setenv('API_GATEWAY_URL', 'http://mock_api_gateway')

# Test login page (GET and POST)
@patch('requests.post')
@patch('requests.get')
def test_login(mock_get, mock_post, client):
    # Test GET login page
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"<html>Login Page</html>"
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login Page" in response.data

    # Test POST login page with valid credentials
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {'token': 'mock_token'}
    response = client.post('/login', data={'email': 'test@test.com', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    assert 'token' in session

    # Test POST login page with invalid credentials
    mock_post.return_value.status_code = 401
    response = client.post('/login', data={'email': 'test@test.com', 'password': 'wrongpassword'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid email or password" in response.data

# Test registration page (GET and POST)
@patch('requests.post')
@patch('requests.get')
def test_register(mock_get, mock_post, client):
    # Test GET register page
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"<html>Register Page</html>"
    response = client.get('/register')
    assert response.status_code == 200
    assert b"Register Page" in response.data

    # Test POST registration page with valid data
    mock_post.return_value.status_code = 201
    response = client.post('/register', data={'email': 'test@test.com', 'password': 'password', 'role': 'student'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Registration successful" in response.data

    # Test POST registration page with invalid data
    mock_post.return_value.status_code = 400
    response = client.post('/register', data={'email': 'test@test.com', 'password': 'password', 'role': 'student'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Registration failed" in response.data

# Test logout
def test_logout(client):
    with client.session_transaction() as sess:
        sess['token'] = 'mock_token'

    response = client.get('/logout', follow_redirects=True)
    assert 'token' not in session
    assert response.status_code == 200

# Test index page
@patch('requests.get')
@patch('api_gateway.app.decode_token')
def test_index(mock_decode_token, mock_get, client):
    # Set a valid token in session
    with client.session_transaction() as sess:
        sess['token'] = 'mock_token'

    # Mock token decoding
    mock_decode_token.return_value = {'role': 'admin'}

    # Mock GET request to frontend service
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"<html>Index Page</html>"

    response = client.get('/')
    assert response.status_code == 200
    assert b"Index Page" in response.data

    # Test redirect to logout when no token
    with client.session_transaction() as sess:
        sess.pop('token', None)
    
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login Page" in response.data  # Assuming user is redirected to login page after logout

# Test manage_students page (GET and POST)
@patch('requests.get')
@patch('requests.post')
@patch('requests.delete')
@patch('api_gateway.app.decode_token')
def test_manage_students(mock_decode_token, mock_delete, mock_post, mock_get, client):
    # Set a valid token in session
    with client.session_transaction() as sess:
        sess['token'] = 'mock_token'

    # Mock token decoding
    mock_decode_token.return_value = {'role': 'admin'}

    # Test GET request
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"<html>Students Page</html>"
    response = client.get('/students')
    assert response.status_code == 200
    assert b"Students Page" in response.data

    # Test POST request to add a student
    mock_post.return_value.status_code = 201
    response = client.post('/students', data={
        'name': 'John Doe',
        'age': '25',
        'company': 'ABC Corp',
        'level': 'Intermediate',
        'stream': 'Engineering'
    }, follow_redirects=True)
    assert response.status_code == 200

    # Test POST request to delete a student
    mock_delete.return_value.status_code = 200
    response = client.post('/students', query_string={'student_id': 1}, follow_redirects=True)
    assert response.status_code == 200

# Additional tests for manage_trainers and manage_courses can be written in a similar way
