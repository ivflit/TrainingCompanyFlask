import pytest
from unittest.mock import patch
from flask import session, request, url_for
from ..frontend.app import app

# Setup test client and environment variables
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch):
    monkeypatch.setenv('SECRET_KEY', 'test_secret')
    monkeypatch.setenv('FRONTEND_SERVICE_URL', 'http://mock_frontend_service')
    monkeypatch.setenv('STUDENT_SERVICE_URL', 'http://mock_student_service')
    monkeypatch.setenv('TRAINER_SERVICE_URL', 'http://mock_trainer_service')
    monkeypatch.setenv('COURSE_SERVICE_URL', 'http://mock_course_service')
    monkeypatch.setenv('AUTH_SERVICE_URL', 'http://mock_auth_service')

# Test the index route
def test_index_template(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Index" in response.data  # Assuming the word "Index" exists on the page

# Test the login route (GET and POST)
@patch('requests.post')
def test_login_template(mock_post, client):
    # Test GET login page
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data

    # Test POST login with correct credentials
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {'token': 'mock_token'}

    response = client.post('/login', data={'email': 'test@test.com', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    assert 'token' in response.headers.get('Set-Cookie')  # Check if token is in cookie

    # Test POST login with incorrect credentials
    mock_post.return_value.status_code = 401
    response = client.post('/login', data={'email': 'test@test.com', 'password': 'wrongpassword'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Login failed" in response.data

# Test the register route (GET and POST)
@patch('requests.post')
def test_register_template(mock_post, client):
    # Test GET register page
    response = client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data

    # Test POST registration with valid data
    mock_post.return_value.status_code = 201
    response = client.post('/register', data={'email': 'test@test.com', 'password': 'password', 'role': 'student'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Registration successful" in response.data

    # Test POST registration with invalid data
    mock_post.return_value.status_code = 400
    response = client.post('/register', data={'email': 'test@test.com', 'password': 'password', 'role': 'student'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Registration failed" in response.data

# Test the logout route
def test_logout(client):
    # Mock setting a token in the cookie
    with client.session_transaction() as sess:
        sess['token'] = 'mock_token'

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert 'token' not in request.cookies  # Check that the token was cleared
    assert b"Logged out successfully" in response.data

# Test the students route
@patch('requests.get')
def test_students_template(mock_get, client):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{'name': 'John Doe', 'age': 25, 'stream': 'Engineering'}]

    response = client.get('/students', headers={'Authorization': 'Bearer mock_token'})
    assert response.status_code == 200
    assert b"John Doe" in response.data  # Ensure the student's name is in the response

# Test the trainers route
@patch('requests.get')
def test_trainers_template(mock_get, client):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{'name': 'Jane Smith', 'skills': ['Python', 'Data Science']}]

    response = client.get('/trainers', headers={'Authorization': 'Bearer mock_token'})
    assert response.status_code == 200
    assert b"Jane Smith" in response.data  # Ensure the trainer's name is in the response

# Test the courses route
@patch('requests.get')
def test_courses_template(mock_get, client):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{'name': 'Intro to Python', 'duration': '4 weeks'}]

    response = client.get('/courses', headers={'Authorization': 'Bearer mock_token'})
    assert response.status_code == 200
    assert b"Intro to Python" in response.data  # Ensure the course name is in the response
