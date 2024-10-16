import requests
from flask import Flask, jsonify, render_template,request

app = Flask(__name__)

FRONTEND_SERVICE_URL = "http://127.0.0.1:8007"
STUDENT_SERVICE_URL = "http://127.0.0.1:8002"
TRAINER_SERVICE_URL = "http://127.0.0.1:8005"
COURSE_SERVICE_URL = "http://127.0.0.1:8004"
BOOKING_SERVICE_URL = "http://127.0.0.1:8003"


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
