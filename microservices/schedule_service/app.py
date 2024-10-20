from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

FRONTEND_SERVICE_URL = os.getenv('FRONTEND_SERVICE_URL')
STUDENT_SERVICE_URL = os.getenv('STUDENT_SERVICE_URL')
TRAINER_SERVICE_URL = os.getenv('TRAINER_SERVICE_URL')
COURSE_SERVICE_URL = os.getenv('COURSE_SERVICE_URL')
BOOKING_SERVICE_URL = os.getenv('BOOKING_SERVICE_URL')

course_runs = {
    1: {'course_id': 1, 'date': '2024-10-01', 'capacity': 30, 'registered_students': []},
    2: {'course_id': 1, 'date': '2024-10-18', 'capacity': 30, 'registered_students': []},
    3: {'course_id': 2, 'date': '2024-10-08', 'capacity': 28, 'registered_students': []},
    4: {'course_id': 2, 'date': '2024-10-20', 'capacity': 28, 'registered_students': []}
}

@app.route('/schedule', methods=['POST'])
def create_course_run():
    data = request.get_json()
    course_id = data.get('course_id')
    date = data.get('date')
    capacity = data.get('capacity')

    response = requests.get(f"{COURSE_SERVICE_URL}/{course_id}")
    
    if response.status_code != 200:
        return jsonify({'error': 'Course not found'}), 404

    run_id = len(course_runs) + 1
    course_runs[run_id] = {
        'course_id': course_id,
        'date': date,
        'capacity': capacity,
        'registered_students': []
    }
    
    return jsonify({'message': 'Course run created', 'run_id': run_id}), 201

@app.route('/schedule/<int:run_id>', methods=['GET'])
def get_course_run(run_id):
    course_run = course_runs.get(run_id)
    
    if not course_run:
        return jsonify({'error': 'Course run not found'}), 404
    
    return jsonify(course_run), 200

@app.route('/schedule', methods=['GET'])
def list_course_runs():
    return jsonify(course_runs), 200

@app.route('/schedule/<int:run_id>/register', methods=['POST'])
def register_student(run_id):
    course_run = course_runs.get(run_id)
    
    if not course_run:
        return jsonify({'error': 'Course run not found'}), 404

    if len(course_run['registered_students']) >= course_run['capacity']:
        return jsonify({'error': 'Course run is fully booked'}), 400
    
    student_id = request.get_json().get('student_id')
    
    course_run['registered_students'].append(student_id)
    
    return jsonify({'message': 'Student registered', 'run_id': run_id}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)