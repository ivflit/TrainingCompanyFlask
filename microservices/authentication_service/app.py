from flask import Flask, request, jsonify
import bcrypt
import boto3
import os
from datetime import datetime, timedelta, timezone  # Add timezone for UTC support
import jwt
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
users_table = dynamodb.Table('Users')  # DynamoDB table for user data

# JWT secret
JWT_SECRET = app.secret_key
def generate_token(email, role):
    # Ensure both email and role are strings
    print(email)
    print(role)
    if not isinstance(email, str):
        raise ValueError("Email must be a string")
    if not isinstance(role, str):
        raise ValueError("Role must be a string")
    
    expiration = datetime.now(timezone.utc) + timedelta(hours=1)
    
    # Convert expiration to UNIX timestamps
    algorithm = 'HS256'
    payload = {
    'email': email,
    'role': role,
    'exp': datetime.now(timezone.utc) + timedelta(seconds=20)
    }
    print(payload)
    print(type(payload))
    print(type(JWT_SECRET))
    print(type(algorithm))
    token = jwt.encode(payload, JWT_SECRET,algorithm)
    print(token)
    return token
# User registration
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    role = data.get('role')  # Get role from request data

    if not email or not password or not role:
        return jsonify({'message': 'Email, password, and role are required'}), 400

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    user_item = {
        'email': email,
        'password': hashed_password.decode('utf-8'),
        'role': role  # Store role in DynamoDB
    }

    try:
        users_table.put_item(Item=user_item)
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'message': f"Error registering user: {str(e)}"}), 500

# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    print("LOGIN HIT")
    try:
        # Retrieve user from DynamoDB
        response = users_table.get_item(Key={'email': email})
        user = response.get('Item')
        print
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # Successful login - generate JWT token
            print("HIT")
            print(type(email))
            print(type(user['role']))
            token = generate_token(email, user['role'])  # Include role in the token
            print("TOKEN GENERATED")
            print(token)
            return jsonify({'token': token}), 200
        else:
            return jsonify({'message': 'Invalid email or password'}), 401
    except Exception as e:
        print(e)
        return jsonify({'message': 'Login failed', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8006)

# %%