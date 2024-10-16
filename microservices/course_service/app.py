from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

courses = {
    1: {'name': 'Python Basics', 'duration': '4 weeks', 'skills': ['Python', 'APIs']},
    2: {'name': 'Java Fundamentals', 'duration': '6 weeks', 'skills': ['Java', 'OOP']}
}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)