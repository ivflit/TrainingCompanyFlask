from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

bookings = []

COURSES_SERVICE_URL = "http://courses_service:5001/courses"

@app.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    course_id = data.get('course_id')
    
    course_response = requests.get(COURSES_SERVICE_URL)
    
    if course_response.status_code != 200:
        return jsonify({'error': 'Failed to retrieve course information'}), 500

    courses = course_response.json()
    course = next((c for c in courses if c['id'] == course_id), None)

    if not course:
        return jsonify({'error': 'Course not found'}), 404

    booking_id = len(bookings) + 1
    bookings[booking_id] = {
        'student_id': data.get('student_id'),
        'course_id': course_id,
        'course_name': course['name'],
        'date': data.get('date')
    }
    
    return jsonify({'message': 'Booking created', 'booking_id': booking_id}), 201

@app.route('/bookings', methods=['GET'])
def get_bookings():
    return jsonify(bookings), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)