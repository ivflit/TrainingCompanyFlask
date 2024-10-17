import requests
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = 'your_secret_key'  # For flash messages

FRONTEND_SERVICE_URL = os.getenv('FRONTEND_SERVICE_URL')
STUDENT_SERVICE_URL = os.getenv('STUDENT_SERVICE_URL')
TRAINER_SERVICE_URL = os.getenv('TRAINER_SERVICE_URL')
COURSE_SERVICE_URL = os.getenv('COURSE_SERVICE_URL')
BOOKING_SERVICE_URL = os.getenv('BOOKING_SERVICE_URL')


@app.template_filter('frontend_static')
def frontend_static(filename):
    """Generate a full URL for static files served by the frontend service."""
    return f"{FRONTEND_SERVICE_URL}/static/{filename}"

@app.route('/')
def index_template():
    urls = {
            'manage_students_url': request.args.get('manage_students_url'),
            'manage_trainers_url': request.args.get('manage_trainers_url'),
            'manage_courses_url': request.args.get('manage_courses_url')
        }
    return render_template('index.html', **urls)
    

@app.route('/students', methods=['GET'])
def students_template():
    students_dict = requests.get(f"{STUDENT_SERVICE_URL}/students").json()
    students = list(students_dict.values())
    return render_template('students.html', students=students)


@app.route('/trainers')
def trainers_template():
    trainers = requests.get(f"{TRAINER_SERVICE_URL}/trainers").json()
    return render_template('trainers.html', trainers=trainers)


@app.route('/courses')
def courses_template():
    courses = requests.get(f"{COURSE_SERVICE_URL}/courses").json()
    return render_template('courses.html', courses=courses)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8007)
