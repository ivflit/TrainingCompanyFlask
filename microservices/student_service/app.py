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