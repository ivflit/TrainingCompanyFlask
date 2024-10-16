from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import requests
import os

app = Flask(__name__)


FRONTEND_SERVICE_URL = os.getenv('FRONTEND_SERVICE_URL')
STUDENT_SERVICE_URL = os.getenv('STUDENT_SERVICE_URL')
TRAINER_SERVICE_URL = os.getenv('TRAINER_SERVICE_URL')
COURSE_SERVICE_URL = os.getenv('COURSE_SERVICE_URL')
BOOKING_SERVICE_URL = os.getenv('BOOKING_SERVICE_URL')


@app.route('/')
def index():
    context = {
        'manage_students_url': url_for('manage_students', _external=True),
        'manage_trainers_url': url_for('manage_trainers', _external=True),
        'view_courses_url': url_for('view_courses', _external=True)
    }

    # Send the context (URLs) as query parameters to the frontend service
    response = requests.get(f"{FRONTEND_SERVICE_URL}/index", params=context)
    
    # Return the HTML from the frontend service
    return Response(response.content, content_type='text/html')


@app.route('/students', methods=['GET', 'POST'])
def manage_students():
    if request.method == 'POST':
        # Send the data to the Student Service
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
    
    response = requests.get(f"{FRONTEND_SERVICE_URL}/students")
    
    return Response(response.content, content_type='text/html')


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

    response = requests.get(f"{FRONTEND_SERVICE_URL}/trainers")
    return Response(response.content, content_type='text/html')



@app.route('/courses', methods=['GET'])
def view_courses():
    # context = {
    #     'book_course': url_for('book_course', _external=True),
    # }
    response = requests.get(f"{FRONTEND_SERVICE_URL}/courses")
    return Response(response.content, content_type='text/html')


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
    app.run(host='0.0.0.0', port=8000)
