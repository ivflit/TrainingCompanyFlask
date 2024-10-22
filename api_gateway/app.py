from flask import Flask, render_template, request, redirect, url_for, jsonify, Response, flash, session
import requests
import os
import jwt
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

FRONTEND_SERVICE_URL = os.getenv('FRONTEND_SERVICE_URL')
STUDENT_SERVICE_URL = os.getenv('STUDENT_SERVICE_URL')
TRAINER_SERVICE_URL = os.getenv('TRAINER_SERVICE_URL')
COURSE_SERVICE_URL = os.getenv('COURSE_SERVICE_URL')
BOOKING_SERVICE_URL = os.getenv('BOOKING_SERVICE_URL')
API_GATEWAY_URL = os.getenv('API_GATEWAY_URL')
AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL')

# Helper function to decode JWT token
def decode_token(token):
    try:
        decoded = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        data = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        response = requests.post(f"{AUTH_SERVICE_URL}/login", json=data)
        if response.status_code == 200:
            token = response.json().get('token')
            print(token)
            print("SUCCESCEICBE")
            session['token'] = token
            print(session)
            print(session['token'])
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login'))
    
    response = requests.get(f"{FRONTEND_SERVICE_URL}/login")
    return Response(response.content, content_type='text/html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        data = {
            'email': request.form['email'],
            'password': request.form['password'],
            'role': request.form['role']
        }

        response = requests.post(f"{AUTH_SERVICE_URL}/register", json=data)

        if response.status_code == 201:
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Please try again.', 'danger')
            return redirect(url_for('register'))

    response = requests.get(f"{FRONTEND_SERVICE_URL}/register")
    return Response(response.content, content_type='text/html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('token', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'token' not in session or decode_token(session['token']) is None:
        return redirect(url_for('logout'))

    context = {
        'manage_students_url': url_for('manage_students', _external=True),
        'manage_trainers_url': url_for('manage_trainers', _external=True),
        'manage_courses_url': url_for('manage_courses', _external=True),
        'role': decode_token(session['token'])['role']
    }
    response = requests.get(f"{FRONTEND_SERVICE_URL}/", params=context)
    return Response(response.content, content_type='text/html')

@app.route('/students', methods=['GET', 'POST'])
def manage_students():
    if 'token' not in session or decode_token(session['token']) is None:
        return redirect(url_for('logout'))
    context = {
        'role': decode_token(session['token'])['role']
    }

    # IF DELETION OR NEW STUDENT
    if request.method == 'POST':
        if request.args.get('student_id'):
            # DELETING STUDENT
            response = requests.delete(f"{STUDENT_SERVICE_URL}/students/{request.args.get('student_id')}")
            return redirect(url_for('manage_students'))
        

        data = {
            'name': request.form['name'],
            'age': request.form['age'],
            'company': request.form['company'],
            'level': request.form['level'],
            'stream': request.form['stream']
        }
        response = requests.post(f"{STUDENT_SERVICE_URL}/students", json=data)
        if response.status_code == 201:
            return redirect(url_for('manage_students'))

    #  GET
    response = requests.get(f"{FRONTEND_SERVICE_URL}/students", params=context)
    return Response(response.content, content_type='text/html')

@app.route('/trainers', methods=['GET', 'POST'])
def manage_trainers():
    if 'token' not in session or decode_token(session['token']) is None:
        return redirect(url_for('logout'))
    context = {
        'role': decode_token(session['token'])['role']
    }

    # DELETE OR CREATE NEW TRAINER
    if request.method == 'POST':
        if request.args.get('trainer_id'):
            # Trainer deletion -> only done by admin
            response = requests.delete(f"{TRAINER_SERVICE_URL}/trainers/{request.args.get('trainer_id')}")
            return redirect(url_for('manage_trainers'))
        

        data = {
            'name': request.form['name'],
            'preferred_cities': request.form['preferred_cities'].split(','),
            'skills': request.form['skills'].split(',')
        }
        response = requests.post(f"{TRAINER_SERVICE_URL}/trainers", json=data)
        if response.status_code == 201:
            return redirect(url_for('manage_trainers'))

    # GET
    response = requests.get(f"{FRONTEND_SERVICE_URL}/trainers", params=context)
    return Response(response.content, content_type='text/html')

@app.route('/courses', methods=['GET', 'POST'])
def manage_courses():
    if 'token' not in session or decode_token(session['token']) is None:
        return redirect(url_for('logout'))
    context = {
        'role': decode_token(session['token'])['role']
    }

    # DELETE OR CREATE NEW COURSE
    if request.method == 'POST':
        if request.args.get('course_id'):
            # DELETION
            response = requests.delete(f"{COURSE_SERVICE_URL}/courses/{request.args.get('course_id')}")
            return redirect(url_for('manage_courses'))

        data = {
            'name': request.form['name'],
            'duration': request.form['duration'],
            'skills': request.form['skills'].split(','),
            'price': request.form['price']
        }
        response = requests.post(f"{COURSE_SERVICE_URL}/courses", json=data)
        if response.status_code == 201:
            return redirect(url_for('manage_courses'))

    # GET
    response = requests.get(f"{FRONTEND_SERVICE_URL}/courses", params=context)
    return Response(response.content, content_type='text/html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
