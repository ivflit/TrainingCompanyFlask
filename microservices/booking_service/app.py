from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

bookings = []

COURSES_SERVICE_URL = "http://courses_service:5001/courses"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)