from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

STUDENT_SERVICE_URL = "http://student_service:5000"
TRAINER_SERVICE_URL = "http://trainer_service:5001"
COURSE_SERVICE_URL = "http://course_service:5002"
BOOKING_SERVICE_URL = "http://booking_service:5003"

@app.route('/students', methods=['POST'])
def register_student():
    data = request.json
    response = requests.post(f"{STUDENT_SERVICE_URL}/students", json=data)
    return jsonify(response.json()), response.status_code

@app.route('/students/<student_id>', methods=['GET'])
def get_student(student_id):
    response = requests.get(f"{STUDENT_SERVICE_URL}/students/{student_id}")
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)