import pytest
from unittest.mock import patch, MagicMock
import microservices
from microservices.authentication_service.app import app, generate_token
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone

# Setup the Flask test client and environment
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test user registration
@patch('microservices.authentication_service.app.users_table.put_item')
def test_register_user(mock_put_item, client):
    # Mock successful user registration
    mock_put_item.return_value = {}

    response = client.post('/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'role': 'student'
    })

    assert response.status_code == 201
    assert b'User registered successfully' in response.data

    # Test registration with missing data
    response = client.post('/register', json={
        'email': '',
        'password': '',
        'role': ''
    })
    assert response.status_code == 400
    assert b'Email, password, and role are required' in response.data

    # Test failed registration due to DynamoDB error
    mock_put_item.side_effect = Exception('DynamoDB Error')
    response = client.post('/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'role': 'student'
    })
    assert response.status_code == 500
    assert b'Error registering user' in response.data

# Test user login
@patch('microservices.authentication_service.app.users_table.get_item')
def test_login(mock_get_item, client):
    # Mock a user in DynamoDB
    hashed_password = bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    mock_get_item.return_value = {
        'Item': {
            'email': 'test@example.com',
            'password': hashed_password,
            'role': 'student'
        }
    }

    # Test successful login
    response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'token' in json_data

    # Test login with invalid credentials
    mock_get_item.return_value = {'Item': None}
    response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert b'Invalid email or password' in response.data

    # Test login with DynamoDB failure
    mock_get_item.side_effect = Exception('DynamoDB Error')
    response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 500
    assert b'Login failed' in response.data

# Test JWT token generation
def test_generate_token():
    email = 'test@example.com'
    role = 'student'

    # Generate a token
    token = generate_token(email, role)
    decoded = jwt.decode(token, app.secret_key, algorithms=["HS256"])

    # Verify the token contents
    assert decoded['email'] == email
    assert decoded['role'] == role
    assert isinstance(decoded['exp'], int)  # Check if the expiration is a valid timestamp

    # Test invalid token generation (non-string inputs)
    with pytest.raises(ValueError):
        generate_token(123, role)  # Email must be a string

    with pytest.raises(ValueError):
        generate_token(email, 123)  # Role must be a string
