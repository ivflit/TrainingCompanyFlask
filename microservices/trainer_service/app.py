from flask import Flask, jsonify, request
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
trainers_table = dynamodb.Table('Trainers') 

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/trainers', methods=['GET'])
def get_trainers():
    try:
        response = trainers_table.scan()  # Get all items from DynamoDB
        trainers = response.get('Items', [])
        logger.debug(f"Trainers found: {trainers}")
        return jsonify(trainers), 200
    except ClientError as e:
        logger.error(f"Error: {e.response['Error']['Message']}")
        return jsonify({'message': f"Error retrieving trainers: {e.response['Error']['Message']}"}), 500

# Retrieve a specific trainer by ID
@app.route('/trainers/<int:trainer_id>', methods=['GET'])
def get_trainer(trainer_id):
    try:
        response = trainers_table.get_item(Key={'trainer_id': trainer_id})
        trainer = response.get('Item')
        if not trainer:
            return jsonify({'message': 'Trainer not found'}), 404
        return jsonify(trainer), 200
    except ClientError as e:
        return jsonify({'message': f"Error retrieving trainer: {e.response['Error']['Message']}"}), 500

# Register a new trainer
@app.route('/trainers', methods=['POST'])
def register_trainer():
    data = request.get_json()
    name = data.get('name')
    preferred_cities = data.get('preferred_cities', [])
    skill_areas = data.get('skills', [])

    if not name or not skill_areas:
        return jsonify({'message': 'Name and skill areas are required.'}), 400

    # Generate a new trainer ID
    response = trainers_table.scan()
    trainers = response.get('Items', [])
    trainer_id = len(trainers) + 1

    # Add new trainer to DynamoDB
    trainer = {
        'trainer_id': trainer_id,
        'name': name,
        'preferred_cities': preferred_cities,
        'skill_areas': skill_areas
    }

    try:
        trainers_table.put_item(Item=trainer)
        return jsonify({'message': 'Trainer registered successfully', 'trainer_id': trainer_id}), 201
    except ClientError as e:
        logger.error(f"Error registering trainer: {e.response['Error']}")
        return jsonify({'message': f"Error registering trainer: {e.response['Error']['Message']}"}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8005)
