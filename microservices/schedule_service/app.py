from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

COURSE_SERVICE_URL = 'http://course_service:5001/courses'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)