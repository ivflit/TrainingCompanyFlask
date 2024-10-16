from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

students = {}
student_id_counter = 1

@app.route('/students', methods=['POST'])
def register_student():
    global student_id_counter
    data = request.get_json()
    
    student_id = student_id_counter
    students[student_id] = {
        'name': data['name'],
        'age': data['age'],
        'company': data['company'],
        'level': data['level'],
        'stream': data['stream']
    }
    
    student_id_counter += 1
    return jsonify({'message': 'Student registered', 'student_id': student_id}), 201

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students), 200

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = students.get(student_id)
    if student:
        return jsonify(student), 200
    return jsonify({'message': 'Student not found'}), 404

@app.route('/students/<int:student_id>/book', methods=['POST'])
def book_course(student_id):
    data = request.get_json()
    course_id = data.get('course_id')
    course_date = data.get('date')

    booking_service_url = "http://booking_service:5003/bookings"
    booking_data = {
        'student_id': student_id,
        'course_id': course_id,
        'date': course_date
    }
    
    # Send booking request to the booking service
    response = requests.post(booking_service_url, json=booking_data)

    if response.status_code == 201:
        return jsonify({'message': 'Course booked successfully'}), 201
    elif response.status_code == 404:
        return jsonify({'message': 'Course not found or fully booked'}), 404
    return jsonify({'message': 'Could not process the booking'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)