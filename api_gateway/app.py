from flask import Flask, jsonify, request, redirect
import requests

app = Flask(__name__)


FRONTEND_SERVICE_URL = "http://127.0.0.1:8007"
STUDENT_SERVICE_URL = "http://127.0.0.1:8002"
TRAINER_SERVICE_URL = "http://127.0.0.1:8005"
COURSE_SERVICE_URL = "http://127.0.0.1:8004"
BOOKING_SERVICE_URL = "http://127.0.0.1:8003"

@app.route('/', methods=['GET'])
def get_homepage():
   return redirect(f"{FRONTEND_SERVICE_URL}/")

# STUDENTS
@app.route('/students', methods=['GET','POST'])
def manage_students():
    if request.method == 'POST':
        data = request.json
        response = requests.post(f"{STUDENT_SERVICE_URL}/students", json=data)
        return jsonify(response.json()), response.status_code

    return redirect(f"{FRONTEND_SERVICE_URL}/students")

@app.route('/students/<student_id>', methods=['GET'])
def get_student(student_id):
    response = requests.get(f"{STUDENT_SERVICE_URL}/students/{student_id}")
    return jsonify(response.json()), response.status_code

# TRAINERS
@app.route('/trainers', methods=['GET', 'POST'])
def manage_trainers():
    if request.method == 'POST':
        data = request.json
        response = requests.post(f"{TRAINER_SERVICE_URL}/trainers", json=data)
        return jsonify(response.json()), response.status_code

    return redirect(f"{FRONTEND_SERVICE_URL}/trainers")

# COURSES
@app.route('/courses', methods=['POST'])
def register_course():
    data = request.json
    response = requests.post(f"{COURSE_SERVICE_URL}/courses", json=data)
    return jsonify(response.json()), response.status_code

@app.route('/courses', methods=['GET'])
def get_courses():
    return redirect(f"{FRONTEND_SERVICE_URL}/courses")

# BOOK COURSE
@app.route('/booking', methods=['POST'])
def book_course():
    data = request.json
    response = requests.post(f"{BOOKING_SERVICE_URL}/booking", json=data)
    return jsonify(response.json()), response.status_code

# CHECK COURSE AVAILABILTIY
@app.route('/courses/<course_id>/availability', methods=['GET'])
def check_availability(course_id):
    response = requests.get(f"{BOOKING_SERVICE_URL}/courses/{course_id}/availability")
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)