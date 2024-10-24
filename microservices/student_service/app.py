from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
import boto3
from botocore.exceptions import ClientError
import os 
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
CORS(app)


# Initialize DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_DEFAULT_REGION')
)
students_table = dynamodb.Table('Students') 

@app.route('/students', methods=['POST'])
def register_student():
    # data = request.get_json()

    # # Create a new student entry with a unique ID
    # student_id = student_id_counter
    # students[student_id] = {
    #     'name': data['name'],
    #     'age': data['age'],
    #     'company': data['company'],
    #     'level': data['level'],
    #     'stream': data['stream']
    # }

    # student_id_counter += 1  # Increment the student ID counter
    # return jsonify({'message': 'Student registered', 'student_id': student_id}), 201
    data = request.get_json()

    # Validate input data
    if not all(key in data for key in ['name', 'age', 'company', 'level', 'stream']):
        return jsonify({'message': 'Name, age, company, and level , stream are required.'}), 400

    # Generate a new course ID (you might want to use UUID or a better ID generation strategy)
    try:
        response = students_table.scan()  # Scan to get existing students
        students = response.get('Items', [])
        student_id = len(students) + 1  # This is a simple way to get the next ID
    except ClientError as e:
        return jsonify({'message': f"Error retrieving students: {e.response['Error']['Message']}"}), 500

    # Create a new student item
    new_student = {
        'student_id': student_id,
        'name': data['name'],
        'age': data['age'],
        'company': data['company'],
        'level': data['level'],
        'stream': data['stream']
    }

    try:
        students_table.put_item(Item=new_student)  # Add the new student to DynamoDB
        return jsonify({'message': 'student created', 'student_id': student_id}), 201
    except ClientError as e:
        return jsonify({'message': f"Error creating student: {e.response['Error']['Message']}"}), 500

@app.route('/students', methods=['GET'])
def get_students():
    try:
        response = students_table.scan()  # Get all students from DynamoDB
        students = response.get('Items', [])
        return jsonify(students), 200
    except ClientError as e:
        return jsonify({'message': f"Error retrieving students: {e.response['Error']['Message']}"}), 500


@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    try:
        response = students_table.get_item(Key={'student_id': student_id})  # Retrieve student by student_id
        student = response.get('Item')
        if not student:
            return jsonify({'message': 'student not found'}), 404
        return jsonify(student), 200
    except ClientError as e:
        return jsonify({'message': f"Error retrieving student: {e.response['Error']['Message']}"}), 500

@app.route('/students/<int:student_id>/book', methods=['POST'])
def book_course(student_id):
    data = request.get_json()
    course_id = data.get('course_id')
    course_date = data.get('date')

    booking_service_url = "http://booking_service:8003/bookings"
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

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        response = students_table.delete_item(Key={'student_id': student_id})  # Delete the student
        return jsonify({'message': 'student deleted successfully.'}), 200
    except ClientError as e:
        return jsonify({'message': f"Error deleting student: {e.response['Error']['Message']}"}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)