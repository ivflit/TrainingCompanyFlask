import requests
from flask import Flask, jsonify, render_template,request
import os

app = Flask(__name__)

FRONTEND_SERVICE_URL = os.environ.get('FRONTEND_SERVICE_URL')
STUDENT_SERVICE_URL = os.environ.get('STUDENT_SERVICE_URL')
TRAINER_SERVICE_URL = os.environ.get('TRAINER_SERVICE_URL')
COURSE_SERVICE_URL = os.environ.get('COURSE_SERVICE_URL')
BOOKING_SERVICE_URL = os.environ.get('BOOKING_SERVICE_URL')


@app.route('/index')
def index_template():
    urls = {
            'manage_students_url': request.args.get('manage_students_url'),
            'manage_trainers_url': request.args.get('manage_trainers_url'),
            'view_courses_url': request.args.get('view_courses_url')
        }
    
    return render_template('index.html', **urls)


@app.route('/students')
def students_template():
    students = requests.get(f"{STUDENT_SERVICE_URL}/students").json()
    return render_template('students.html', students=students)


@app.route('/trainers')
def trainers_template():
    trainers = requests.get(f"{TRAINER_SERVICE_URL}/trainers").json()
    return render_template('trainers.html', trainers=trainers)

@app.route('/courses')
def courses_template():
    urls = {
        'book_course': request.args.get('book_course')
    }
    courses = requests.get(f"{COURSE_SERVICE_URL}/courses").json()
    return render_template('courses.html', courses=courses, **urls)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8007)
