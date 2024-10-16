from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

courses = {
    1: {'name': 'Python Basics', 'duration': '4 weeks', 'skills': ['Python', 'APIs']},
    2: {'name': 'Java Fundamentals', 'duration': '6 weeks', 'skills': ['Java', 'OOP']}
}

@app.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json()
    course_id = max(courses.keys()) + 1
    courses[course_id] = {
        'name': data['name'],
        'duration': data['duration'],
        'skills': data['skills']
    }
    return jsonify({'message': 'Course created', 'course_id': course_id}), 201

@app.route('/courses', methods=['GET'])
def get_courses():
    return jsonify(courses), 200

@app.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = courses.get(course_id)
    if course:
        return jsonify(course), 200
    return jsonify({'message': 'Course not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)