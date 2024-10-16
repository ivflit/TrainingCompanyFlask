from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

STUDENT_SERVICE_URL = "http://student_service:5000"
TRAINER_SERVICE_URL = "http://trainer_service:5001"
COURSE_SERVICE_URL = "http://course_service:5002"
BOOKING_SERVICE_URL = "http://booking_service:5003"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)