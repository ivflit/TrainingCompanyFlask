from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

FRONTEND_SERVICE_URL = "http://127.0.0.1:8007"
STUDENT_SERVICE_URL = "http://127.0.0.1:8002"
TRAINER_SERVICE_URL = "http://127.0.0.1:8005"
COURSE_SERVICE_URL = "http://127.0.0.1:8004"
BOOKING_SERVICE_URL = "http://127.0.0.1:8003"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students', methods=['GET', 'POST'])
def manage_students():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'age': request.form['age'],
            'company': request.form['company'],
            'level': request.form['level'],
            'stream': request.form['stream']
        }
        response = requests.post(STUDENT_SERVICE_URL, json=data)
        if response.status_code == 201:
            return redirect(url_for('manage_students'))
    
    students = requests.get(STUDENT_SERVICE_URL).json()
    return render_template('students.html', students=students)

@app.route('/trainers', methods=['GET', 'POST'])
def manage_trainers():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'preferred_cities': request.form['preferred_cities'].split(','),
            'skills': request.form['skills'].split(',')
        }
        response = requests.post(TRAINER_SERVICE_URL, json=data)
        if response.status_code == 201:
            return redirect(url_for('manage_trainers'))
    
    trainers = requests.get(TRAINER_SERVICE_URL).json()
    return render_template('trainers.html', trainers=trainers)

@app.route('/courses', methods=['GET'])
def view_courses():
    courses = requests.get(COURSE_SERVICE_URL).json()
    return render_template('courses.html', courses=courses)

@app.route('/students/<int:student_id>/book', methods=['POST'])
def book_course(student_id):
    data = {
        'course_id': request.form['course_id'],
        'date': request.form['date']
    }
    response = requests.post(f"{BOOKING_SERVICE_URL}/{student_id}/book", json=data)
    if response.status_code == 201:
        return redirect(url_for('manage_students'))
    return "Booking failed!", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8007)
