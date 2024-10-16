import requests
from flask import Flask, jsonify, render_template,request

app = Flask(__name__)

TRAINER_SERVICE_URL = 'http://localhost:8005' 


@app.route('/index')
def index_template():
    urls = {
            'manage_students_url': request.args.get('manage_students_url'),
            'manage_trainers_url': request.args.get('manage_trainers_url'),
            'view_courses_url': request.args.get('view_courses_url')
        }
    
    return render_template('index.html', **urls)


@app.route('/students')
def students_template():
    return render_template('students.html')


@app.route('/trainers')
def trainers_template():
    trainers = requests.get(f"{TRAINER_SERVICE_URL}/trainers").json()
    return render_template('trainers.html', trainers=trainers)

@app.route('/courses')
def courses_template():
    return render_template('courses.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8007)
