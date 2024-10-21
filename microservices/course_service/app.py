from flask import Flask, jsonify, request
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
courses_table = dynamodb.Table('Courses')  # Use the actual table name

@app.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json()

    # Validate input data
    if not all(key in data for key in ['name', 'duration', 'skills', 'price']):
        return jsonify({'message': 'Name, duration, skills, and price are required.'}), 400

    # Generate a new course ID (you might want to use UUID or a better ID generation strategy)
    try:
        response = courses_table.scan()  # Scan to get existing courses
        courses = response.get('Items', [])
        course_id = len(courses) + 1  # This is a simple way to get the next ID
    except ClientError as e:
        return jsonify({'message': f"Error retrieving courses: {e.response['Error']['Message']}"}), 500

    # Create a new course item
    new_course = {
        'course_id': course_id,
        'name': data['name'],
        'duration': data['duration'],
        'skills': data['skills'],
        'price': data['price']
    }

    try:
        courses_table.put_item(Item=new_course)  # Add the new course to DynamoDB
        return jsonify({'message': 'Course created', 'course_id': course_id}), 201
    except ClientError as e:
        return jsonify({'message': f"Error creating course: {e.response['Error']['Message']}"}), 500

@app.route('/courses', methods=['GET'])
def get_courses():
    try:
        response = courses_table.scan()  # Get all courses from DynamoDB
        courses = response.get('Items', [])
        return jsonify(courses), 200
    except ClientError as e:
        return jsonify({'message': f"Error retrieving courses: {e.response['Error']['Message']}"}), 500

@app.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    try:
        response = courses_table.get_item(Key={'course_id': course_id})  # Retrieve course by course_id
        course = response.get('Item')
        if not course:
            return jsonify({'message': 'Course not found'}), 404
        return jsonify(course), 200
    except ClientError as e:
        return jsonify({'message': f"Error retrieving course: {e.response['Error']['Message']}"}), 500

@app.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    try:
        print("This got hit")
        response = courses_table.delete_item(Key={'course_id': course_id})  # Delete the course
        return jsonify({'message': 'Course deleted successfully.'}), 200
    except ClientError as e:
        return jsonify({'message': f"Error deleting course: {e.response['Error']['Message']}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8004)
