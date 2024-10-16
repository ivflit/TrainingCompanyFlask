from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

STUDENT_SERVICE_URL = "http://student_service:5003/students"
TRAINER_SERVICE_URL = "http://trainer_service:5004/trainers"
COURSE_SERVICE_URL = "http://course_service:5001/courses"
BOOKING_SERVICE_URL = "http://booking_service:5002/students"

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
