import requests
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session, make_response
import os
from dotenv import load_dotenv
import jwt  # For decoding JWT

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = os.getenv('SECRET_KEY')

FRONTEND_SERVICE_URL = os.getenv('FRONTEND_SERVICE_URL')
STUDENT_SERVICE_URL = os.getenv('STUDENT_SERVICE_URL')
TRAINER_SERVICE_URL = os.getenv('TRAINER_SERVICE_URL')
COURSE_SERVICE_URL = os.getenv('COURSE_SERVICE_URL')
BOOKING_SERVICE_URL = os.getenv('BOOKING_SERVICE_URL')
AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL')

# Custom Jinja filter to generate full URL for static files from the frontend service
@app.template_filter('frontend_static')
def frontend_static(filename):
    """Generate a full URL for static files served by the frontend service."""
    return f"{FRONTEND_SERVICE_URL}/static/{filename}"

# Index route, checks if user is logged in via token
@app.route('/')
def index_template():

    urls = {
        'manage_students_url': request.args.get('manage_students_url'),
        'manage_trainers_url': request.args.get('manage_trainers_url'),
        'manage_courses_url': request.args.get('manage_courses_url')
    }
    return render_template('index.html', **urls)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login_template():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Call authentication microservice to login
        data = {'email': email, 'password': password}
        response = requests.post(f"{AUTH_SERVICE_URL}/login", json=data)
        
        if response.status_code == 200:
            token = response.json().get('token')
            print("Token received from Auth Service:", token)
            flash('Login successful!', 'success')
            
            # Store the token in a cookie
            response = make_response(redirect(url_for('index_template')))
            response.set_cookie('token', token, httponly=True)  # Store JWT in a cookie
            return response
        else:
            flash('Login failed. Please check your credentials.', 'error')
            return redirect(url_for('login_template'))
    
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register_template():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']  # Include role in registration

        # Call authentication microservice to register
        data = {'email': email, 'password': password, 'role': role}
        response = requests.post(f"{AUTH_SERVICE_URL}/register", json=data)
        
        if response.status_code == 201:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login_template'))
        else:
            flash('Registration failed. Try again.', 'error')
            return redirect(url_for('register_template'))
    
    return render_template('register.html')

# Logout route
@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login_template')))
    response.set_cookie('token', '', expires=0)  # Clear the token cookie
    flash('Logged out successfully.', 'success')
    return response

# Students route
@app.route('/students', methods=['GET'])
def students_template():
    token = request.cookies.get('token')
    headers = {'Authorization': f'Bearer {token}'}  # Pass token in headers

    students = requests.get(f"{STUDENT_SERVICE_URL}/students", headers=headers).json()
    return render_template('students.html', students=students)

# Trainers route
@app.route('/trainers')
def trainers_template():

    token = request.cookies.get('token')
    headers = {'Authorization': f'Bearer {token}'}  # Pass token in headers

    trainers = requests.get(f"{TRAINER_SERVICE_URL}/trainers", headers=headers).json()
    return render_template('trainers.html', trainers=trainers)

# Courses route
@app.route('/courses')
def courses_template():

    token = request.cookies.get('token')
    headers = {'Authorization': f'Bearer {token}'}  # Pass token in headers

    courses = requests.get(f"{COURSE_SERVICE_URL}/courses", headers=headers).json()
    return render_template('courses.html', courses=courses)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8007)
