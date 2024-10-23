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

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_DEFAULT_REGION')
)
print(dynamodb)
users_table = dynamodb.Table('Users')  # DynamoDB table for user data
print(users_table)

# JWT secret
JWT_SECRET = app.secret_key
def generate_token(email, role):
    # Ensure both email and role are strings
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
    'exp': datetime.now(timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(payload, JWT_SECRET,algorithm)
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
    try:
        # Retrieve user from DynamoDB
        response = users_table.get_item(Key={'email': email})
        print(f"RESPONSE FROM USERS.GET: {response}")
        user = response.get('Item')
        print(f"USER: {user}")
        print(f"PASSWORD FROM TEST: {password}")
        encodepass = password.encode('utf-8')
        print(f"PASSWORD ENCODED FROM TEST: {encodepass}")
        print(f"PASSWORD FROM DB: {user['password']}")
        print(f"PASSWORD ENCODED FROM DB: {user['password'].encode('utf-8')}")
        print(f"PASSWORD CHECK: {bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8'))}")
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # Successful login - generate JWT token
            print(f"USER ROLE: {user['role']}")
            token = generate_token(email, user['role'])  # Include role in the token
            return jsonify({'token': token}), 200
        else:
            return jsonify({'message': 'Invalid email or password'}), 401
    except Exception as e:
        print(e)
        return jsonify({'message': 'Login failed', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8006)

# %%
