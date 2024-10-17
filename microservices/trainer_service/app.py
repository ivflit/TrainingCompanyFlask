from flask import Flask, jsonify, request

app = Flask(__name__)

trainers = {
    1: {
        'id': 1,
        'name': 'Alice Smith',
        'preferred_cities': ['New York', 'Los Angeles'],
        'skill_areas': ['Python', 'Data Science']
    },
    2: {
        'id': 2,
        'name': 'Bob Johnson',
        'preferred_cities': ['Chicago', 'San Francisco'],
        'skill_areas': ['Java', 'Web Development']
    },
    3: {
        'id': 3,
        'name': 'Charlie Brown',
        'preferred_cities': ['Miami', 'Seattle'],
        'skill_areas': ['C++', 'Machine Learning']
    }
}

trainer_id_counter = len(trainers) + 1 

@app.route('/trainers', methods=['POST'])
def register_trainer():
    global trainer_id_counter
    data = request.get_json()
    name = data.get('name')
    preferred_cities = data.get('preferred_cities', [])
    skill_areas = data.get('skills', [])

    if not name or not skill_areas:
        return jsonify({'message': 'Name and skill areas are required.'}), 400

    trainer_id = trainer_id_counter
    trainers[trainer_id] = {
        'id': trainer_id,
        'name': name,
        'preferred_cities': preferred_cities,
        'skill_areas': skill_areas
    }

    trainer_id_counter += 1
    return jsonify({'message': 'Trainer registered successfully', 'trainer_id': trainer_id}), 201

@app.route('/trainers', methods=['GET'])
def get_trainers():
    return jsonify(list(trainers.values())), 200

@app.route('/trainers/<int:trainer_id>', methods=['GET'])
def get_trainer(trainer_id):
    trainer = trainers.get(trainer_id)
    if not trainer:
        return jsonify({'message': 'Trainer not found'}), 404
    return jsonify(trainer), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8005) 